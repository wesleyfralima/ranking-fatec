import json
import logging

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy import and_
from sqlalchemy.orm import Session

from ranking_fatec.core import (
    CandidatoInput,
    calcular_nota_final,
    recalcular_probabilidades,
    recalcular_todas_as_notas,
    recalcular_todos_os_candidatos_do_banco,
)
from ranking_fatec.dados import GABARITO
from ranking_fatec.db import get_db
from ranking_fatec.models import Candidato, Oferta

app = FastAPI(title="Ranking FATEC", root_path="/apps/ranking-fatec")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
def muito_obrigado():
    raise HTTPException(
        status_code=400,
        detail=(
            "Obrigado por usar esse site! "
            "No momento não estamos mais recebendo respostas.",
        ),
    )


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
    recalcular_todas_as_notas(db)
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
