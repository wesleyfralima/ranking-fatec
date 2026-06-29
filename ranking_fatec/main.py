import json
import logging
import math

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from sqlalchemy import and_
from sqlalchemy.orm import Session

from ranking_fatec.dados import GABARITO
from ranking_fatec.db import Base, engine, get_db
from ranking_fatec.models import Candidato, Oferta

# Inicializa as tabelas físicas se elas não existirem
# (fallback amigável se o Alembic ainda não rodou)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ranking FATEC", root_path="/apps/ranking-fatec")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic schemas para validação de dados recebidos
class CandidatoInput(BaseModel):
    nome: str = Field(..., min_length=5, max_length=30)
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
    cv: float | None,
    acertos: int,
    redacao: float,
    nota_corte: float | None = None,
) -> float:
    """
    Estima a probabilidade de aprovação utilizando um modelo logístico.

    Regras aplicadas:
        - Redação zero ou zero acertos nas objetivas descarta o candidato (0%).
        - Relação C/V menor ou igual a 1 é aprovação certa (quando não desclassificado).
        - Ranking atenuado devido à amostragem baixa.
        - Foco principal na diferença da nota de corte histórica e concorrência.
    """

    # --------------------------------------
    # 1) Desclassificação Direta pelo Edital
    # --------------------------------------
    if redacao == 0.0 or acertos == 0:
        return 0.0

    score: float = 0.0

    if cv is None:
        cv = 3.5

    if cv <= 1:
        return 100

    # --------------------------------------
    # 2) Nota de Corte (Maior carga de cálculo)
    # --------------------------------------
    if nota_corte is not None:
        diff = nfc - nota_corte

        # Se a nota é maior que o corte histórico, o ganho tem que ser limpo.
        # Peso 0.40 significa que ficar 5 pontos acima
        # do corte dá +2,0 no score (chance de ~88%)
        score += diff * 0.40
    else:
        # Se não houver nota de corte disponível,
        # usa a NFC ponderada de forma mais branda
        score += (nfc - 60) * 0.25

    # --------------------------------------
    # 3) Concorrência (Peso aumentado no cálculo)
    # --------------------------------------
    # Penaliza e equilibra o score baseando-se no tamanho da disputa do curso
    score -= math.log1p(cv) * 0.30

    # --------------------------------------
    # 4) Ranking (Peso atenuado por conta da amostragem baixa)
    # --------------------------------------
    if rank > 0:
        posicao_relativa = (vagas - rank) / max(vagas, 1)
        # Reduzido drasticamente de 2,8 para 0,50 para
        # não distorcer o cálculo nesta fase amostral
        score += 0.50 * posicao_relativa

    # --------------------------------------
    # 5) Conversão para Porcentagem
    # --------------------------------------
    prob = sigmoid(score)

    # Mantemos uma margem para quem não foi desclassificado direto
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
    do mesmo curso, local (faculdade) e período específico.
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

    # O ranking já é gerado isolado por Curso, Local e Período
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

    for rank, candidato in enumerate(candidatos, start=1):
        candidato.probabilidade = calcular_probabilidade_aprovacao(
            nfc=candidato.nfc,
            vagas=oferta.vagas,
            rank=rank,
            cv=oferta.cand_vaga_historico,
            acertos=candidato.acertos,
            redacao=candidato.redacao,
            nota_corte=None,  # oferta.nota_corte_historica,
        )


def recalcular_todos_os_candidatos_do_banco(db: Session) -> dict:
    """
    Busca apenas as combinações de faculdade/curso/período que possuem
    pelo menos um candidato cadastrado e força o recálculo do grupo.
    """
    try:
        # Busca apenas os grupos (chaves compostas) que possuem candidatos ativos
        grupos_ativos = (
            db.query(Candidato.faculdade, Candidato.curso, Candidato.periodo)
            .distinct()
            .all()
        )

        contador_grupos = 0

        # Varre apenas os grupos que realmente têm trabalho a ser feito
        for faculdade, curso, periodo in grupos_ativos:
            recalcular_probabilidades(
                db=db, faculdade=faculdade, curso=curso, periodo=periodo
            )
            contador_grupos += 1

        db.commit()

        return {
            "status": "sucesso",
            "mensagem": (
                f"Probabilidades atualizadas com sucesso para "
                f"{contador_grupos} grupos de candidatos ativos."
            ),
        }

    except Exception as e:
        db.rollback()
        logging.error(f"Erro ao rodar recálculo geral otimizado: {str(e)}")
        raise e


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
    data = (
        db.query(Candidato, Oferta)
        .join(
            Oferta,
            and_(
                Candidato.faculdade == Oferta.campus,
                Candidato.periodo == Oferta.periodo,
                Candidato.curso == Oferta.curso,
            ),
        )
        .order_by(Candidato.nfc.desc(), Candidato.acertos.desc())
        .all()
    )
    return [
        {
            "nome": candidato.nome,
            "faculdade": candidato.faculdade,
            "curso": candidato.curso,
            "periodo": candidato.periodo,
            "acertos": candidato.acertos,
            "redacao": candidato.redacao,
            "nfc": candidato.nfc,
            "probabilidade": candidato.probabilidade,
            "vagas": oferta.vagas,
            "nota_corte": oferta.nota_corte_historica,
            "candidato_vaga": oferta.cand_vaga_historico,
        }
        for candidato, oferta in data
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


@app.get("/api/admin/recalcular")
def disparar_recalculo_geral(db: Session = Depends(get_db)):
    return recalcular_todos_os_candidatos_do_banco(db)


@app.get("/api/candidato/{nome}")
def obter_candidato_por_nome(nome: str, db: Session = Depends(get_db)):
    candidato = db.query(Candidato).filter(Candidato.nome == nome.strip()).first()

    if not candidato:
        raise HTTPException(
            status_code=404, detail="Candidato não encontrado no ranking atual."
        )

    # Como as respostas são salvas como String JSON no banco,
    # precisamos converter de volta para dicionário antes de enviar
    try:
        respostas_dict = json.loads(candidato.respostas) if candidato.respostas else {}
    except Exception:
        respostas_dict = {}

    return {
        "nome": candidato.nome,
        "faculdade": candidato.faculdade,
        "curso": candidato.curso,
        "periodo": candidato.periodo,
        "redacao": candidato.redacao,
        "nota_enem": candidato.nota_enem,
        "is_afro": candidato.is_afro,
        "is_publica": candidato.is_publica,
        "respostas": respostas_dict,
    }


@app.get("/", response_class=HTMLResponse)
def index():
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()
