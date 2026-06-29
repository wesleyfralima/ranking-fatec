import json
import logging
import math

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ranking_fatec.dados import GABARITO
from ranking_fatec.db import Base, engine, get_db
from ranking_fatec.models import Candidato, Oferta

# Inicializa as tabelas físicas se elas não existirem
# (fallback amigável se o Alembic ainda não rodou)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ranking FATEC Oficial")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic schemas para validação de dados recebidos
class CandidatoInput(BaseModel):
    nome: str = Field(..., max_length=30)
    faculdade: str = Field(..., max_length=100)
    curso: str = Field(..., max_length=100)
    periodo: str = Field(..., max_length=20)
    redacao: float = Field(..., ge=0, le=100)
    nota_enem: float | None = Field(None, ge=0, le=100)
    is_afro: bool
    is_publica: bool
    respostas: dict[int, str]


def calcular_nota_final(
    respostas: dict[int, str],
    nota_enem: float | None,
    redacao: float,
    is_afro: bool,
    is_publica: bool,
) -> tuple[float, int]:
    """
    Executa os passos de cálculo do edital da FATEC baseando-se em 60 questões.
    Retorna uma tupla contendo (nfc, acertos).
    """

    # 1. Contagem automática de acertos (NPC)
    npc = 0
    for q_num, alternativa_correta in GABARITO.items():
        resposta_usuario = respostas.get(q_num)
        if resposta_usuario and resposta_usuario.upper() == alternativa_correta.upper():
            npc += 1

    # 2. Nota das questões objetivas (P)
    p = (100 * npc) / 60

    # 3. Nota final da parte objetiva considerando o ENEM (N)
    n = p
    if nota_enem is not None:
        enem = nota_enem
        if enem > p:
            n = ((4 * p) + (1 * enem)) / 5

    # 4. Nota final sem bônus (NF)
    r = redacao
    nf = ((8 * n) + (2 * r)) / 10

    # 5. Sistema de Pontuação Acrescida -> Nota Final do Candidato (NFC)
    if is_afro and is_publica:
        nfc = nf * 1.13
    elif not is_afro and is_publica:
        nfc = nf * 1.10
    elif is_afro and not is_publica:
        nfc = nf * 1.03
    else:
        nfc = nf

    return nfc, npc


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def calcular_probabilidade_aprovacao(
    nfc: float,
    vagas: int,
    rank: int,
    cv: float,
    nota_corte: float | None = None,
    usar_nota_corte: bool = False,
) -> float:
    """
    Estima a probabilidade de aprovação utilizando um modelo logístico.

    Variáveis utilizadas:
        - NFC do candidato
        - Relação candidato/vaga
        - Ranking atual
        - Nota de corte (opcional)

    Retorna:
        Probabilidade entre 1,0 e 99,9 (%)

    OBS:
        Os coeficientes foram escolhidos empiricamente e podem ser
        calibrados futuramente com dados reais.
    """

    score: float = 0.0

    # ----------------------------
    # 1) Ranking (principal fator)
    # ----------------------------
    if rank > 0:
        posicao_relativa = (vagas - rank) / max(vagas, 1)

        # varia aproximadamente de -∞ até 1
        score += 2.8 * posicao_relativa

    # ----------------------------
    # 2) Nota de corte (opcional)
    # ----------------------------
    if usar_nota_corte and nota_corte is not None:
        diff = nfc - nota_corte

        # Cursos muito concorridos exigem margem maior
        fator = 1 / (1 + math.log1p(max(cv - 1, 0)))

        score += diff * 0.09 * fator

    else:
        #
        # Sem nota de corte:
        # Usa apenas a NFC como um leve indicativo.
        #
        score += (nfc - 700) * 0.01

    # ----------------------------
    # 3) Concorrência
    # ----------------------------
    #
    # Penaliza cursos extremamente concorridos.
    #
    score -= math.log1p(cv) * 0.35

    # ----------------------------
    # 4) Probabilidade
    # ----------------------------
    prob = sigmoid(score)

    porcentagem = min(max(prob * 100, 1.0), 99.9)

    return round(porcentagem, 2)


def recalcular_probabilidades(
    db: Session,
    faculdade: str,
    curso: str,
    periodo: str,
) -> None:
    """
    Recalcula o ranking e a probabilidade de TODOS os candidatos
    de um mesmo curso.

    Deve ser chamada sempre que um candidato for inserido ou atualizado.
    """

    oferta = (
        db.query(Oferta)
        .filter(
            Oferta.campus == faculdade,
            Oferta.curso == curso,
            Oferta.periodo == periodo,
        )
        .first()
    )

    if oferta is None:
        return

    candidatos = (
        db.query(Candidato)
        .filter(
            Candidato.faculdade == faculdade,
            Candidato.curso == curso,
            Candidato.periodo == periodo,
        )
        .order_by(
            Candidato.nfc.desc(),
            Candidato.acertos.desc(),
        )
        .all()
    )

    usar_corte = oferta.nota_corte_historica is not None

    for rank, candidato in enumerate(candidatos, start=1):
        candidato.probabilidade = calcular_probabilidade_aprovacao(
            nfc=candidato.nfc,
            vagas=oferta.vagas,
            rank=rank,
            cv=oferta.cand_vaga_historico,
            nota_corte=oferta.nota_corte_historica,
            usar_nota_corte=usar_corte,
        )


# --- Endpoints da API ---


@app.get("/api/gabarito")
def obter_gabarito():
    return GABARITO


@app.get("/api/campuses")
def obter_campuses(db: Session = Depends(get_db)):
    campuses = db.query(Oferta.campus).distinct().order_by(Oferta.campus).all()
    return [c[0] for c in campuses]


@app.get("/api/periods")
def obter_periodos(campus: str, db: Session = Depends(get_db)):
    periodos = (
        db.query(Oferta.periodo)
        .filter(Oferta.campus == campus)
        .distinct()
        .order_by(Oferta.periodo)
        .all()
    )
    return [p[0] for p in periodos]


@app.get("/api/courses")
def obter_cursos(campus: str, periodo: str, db: Session = Depends(get_db)):
    cursos = (
        db.query(Oferta.curso)
        .filter(Oferta.campus == campus, Oferta.periodo == periodo)
        .distinct()
        .order_by(Oferta.curso)
        .all()
    )
    return [c[0] for c in cursos]


@app.get("/api/ranking")
def obter_ranking(db: Session = Depends(get_db)):
    candidatos = (
        db.query(Candidato)
        .order_by(Candidato.nfc.desc(), Candidato.acertos.desc())
        .all()
    )
    return [
        {
            "nome": c.nome,
            "faculdade": c.faculdade,
            "curso": c.curso,
            "periodo": c.periodo,
            "acertos": c.acertos,
            "redacao": c.redacao,
            "nfc": c.nfc,
            "probabilidade": c.probabilidade,
        }
        for c in candidatos
    ]


@app.post("/api/ranking")
def adicionar_nota(candidato_in: CandidatoInput, db: Session = Depends(get_db)):
    try:
        # Executa o cálculo isolado na nova função
        nfc, npc = calcular_nota_final(
            respostas=candidato_in.respostas,
            nota_enem=candidato_in.nota_enem,
            redacao=candidato_in.redacao,
            is_afro=candidato_in.is_afro,
            is_publica=candidato_in.is_publica,
        )
    except Exception as calc_err:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao processar cálculo das notas: {str(calc_err)}",
        )

    try:
        # Lógica de UPSERT amigável do SQLAlchemy
        candidato_db = (
            db.query(Candidato)
            .filter(Candidato.nome == candidato_in.nome.strip())
            .first()
        )

        if candidato_db:
            # Atualiza o registro existente
            candidato_db.faculdade = candidato_in.faculdade
            candidato_db.curso = candidato_in.curso
            candidato_db.periodo = candidato_in.periodo
            candidato_db.acertos = npc
            candidato_db.redacao = candidato_in.redacao
            candidato_db.nota_enem = candidato_in.nota_enem
            candidato_db.is_afro = candidato_in.is_afro
            candidato_db.is_publica = candidato_in.is_publica
            candidato_db.nfc = nfc
            candidato_db.probabilidade = 0
            candidato_db.respostas = json.dumps(candidato_in.respostas)
        else:
            # Cria novo registro
            candidato_db = Candidato(
                nome=candidato_in.nome.strip(),
                faculdade=candidato_in.faculdade,
                curso=candidato_in.curso,
                periodo=candidato_in.periodo,
                acertos=npc,
                redacao=candidato_in.redacao,
                nota_enem=candidato_in.nota_enem,
                is_afro=candidato_in.is_afro,
                is_publica=candidato_in.is_publica,
                nfc=nfc,
                probabilidade=0,
                respostas=json.dumps(candidato_in.respostas),
            )
            db.add(candidato_db)

        db.flush()

        recalcular_probabilidades(
            db=db,
            faculdade=candidato_in.faculdade,
            curso=candidato_in.curso,
            periodo=candidato_in.periodo,
        )

        db.commit()

        db.refresh(candidato_db)

        return {
            "status": "sucesso",
            "nfc": nfc,
            "acertos": npc,
            "probabilidade": candidato_db.probabilidade,
        }

    except Exception as db_err:
        logging.error(db_err)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=(
                "Erro de persistência no banco de dados. "
                "Verifique os dados e tente novamente.",
            ),
        )


@app.get("/", response_class=HTMLResponse)
def index():
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()
