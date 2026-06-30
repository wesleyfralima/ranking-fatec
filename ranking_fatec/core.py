import json
import logging
import math

from pydantic import BaseModel, Field
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from ranking_fatec.dados import GABARITO
from ranking_fatec.models import Candidato, Oferta


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

    # 5. Sistema de Pontuação Acrescida → Nota Final do Candidato (NFC)
    if is_afro and is_publica:
        nfc = nf * 1.13
    elif not is_afro and is_publica:
        nfc = nf * 1.10
    elif is_afro and not is_publica:
        nfc = nf * 1.03
    else:
        nfc = nf

    return nfc, npc


def recalcular_todas_as_notas(db: Session):
    stmt = select(Candidato)
    result = db.execute(stmt)
    candidatos = result.scalars().all()

    for c in candidatos:
        notas_dict = {int(k): v for k, v in json.loads(c.respostas).items()}
        nfc, npc = calcular_nota_final(
            respostas=notas_dict,
            nota_enem=c.nota_enem,
            redacao=c.redacao,
            is_afro=c.is_afro,
            is_publica=c.is_publica,
        )
        c.acertos = npc
        c.nfc = nfc

    db.commit()


def sigmoid_1000(score: float) -> float:
    """
    Sigmoide adaptada para receber um score positivo de 0 a 1000.
    O ponto de inflexão (50%) é exatamente em 500.
    O fator 0.025 garante uma transição firme e clara perto do corte.
    """
    x = (score - 500) * 0.025
    return 1.0 / (1.0 + math.exp(-x))


def calcular_probabilidade_aprovacao(
    nfc: float,
    vagas: int,
    rank: int | None,
    cv: float | None,
    acertos: int,
    redacao: float,
    nota_corte: float | None = None,
) -> float:
    """
    Estima a probabilidade de aprovação utilizando
    um modelo logístico baseado em 1000 pontos.

    Regras absolutas aplicadas:
        - Redação zero ou zero acertos nas objetivas descarta o candidato (0%).
        - Relação C/V menor ou igual a 1,0 garante aprovação automática (100%).
        - Nota de corte ajustada é o ponto neutro (Score 500 = 50% de chance).
        - Sem nota de corte, o modelo usa a relação C/V
            para penalizar ou bonificar a nota base (60).
    """

    # --------------------------------------
    # 1) Desclassificação Direta pelo Edital
    # --------------------------------------
    if redacao == 0.0 or acertos == 0:
        return 0.0

    # Tratamento e priorização da relação Candidato/Vaga (C/V)
    if cv is None:
        cv = 3.5

    # --------------------------------------
    # 2) Aprovação certa: relação C/V menor ou igual a 1
    # --------------------------------------
    if cv <= 1.0:
        return 100.0

    score: float = 500.0

    # --------------------------------------
    # 3) Nota de Corte (Prioridade máxima no cálculo)
    # --------------------------------------
    if nota_corte is not None:
        # Cenário A: Temos nota de corte
        # (C/V é ignorado, pois o corte já o absorveu)

        # Ponderação histórica: Considera que a prova foi
        # levemente mais difícil do que a do 1º semestre de 2026
        # Ex: 84,00 * 0,98 = 82,32
        nota_corte_ajustada = nota_corte * 0.98
        diff = nfc - nota_corte_ajustada

        if diff >= 0:
            # Acumula pontos normalmente para quem passou do corte histórico
            score += min(diff * 20.0, 450.0)
        else:
            # PENALIZAÇÃO EM DOBRO: Se está abaixo do corte ajustado,
            # o score despenca mais rápido para
            # refletir a realidade dos cortes.
            score += max(diff * 35.0, -500.0)
    else:
        # Cenário B: SEM nota de corte
        # (O C/V assume o controle do risco)

        # Assumimos 60 como uma nota média neutra
        # para um C/V padrão (por volta de 3,5)
        diff_media = nfc - 60.0

        if diff_media >= 0:
            score += min(diff_media * 12.0, 450.0)
        else:
            score += max(diff_media * 25.0, -500.0)

        # Modificador de Concorrência: Se não há corte,
        # o tamanho do C/V molda o score.
        # Um C/V de 3,5 zera o modificador.
        # C/V de 20 subtrai ~140 pontos (exige nota maior).
        # Um C/V de 1,7 soma ~53 pontos (ajuda o candidato).
        modificador_cv = (math.log1p(3.5) - math.log1p(cv)) * 80.0
        score += modificador_cv

    # --------------------------------------
    # 4) Ranking Opcional (Modo Amostragem Alta)
    # -------------------------------------
    # Só interfere se explicitamente ativado e se o rank for válido
    if rank is not None and rank > 0:
        posicao_relativa = (vagas - rank) / max(vagas, 1)
        score += 30 * posicao_relativa

    # Trava de segurança do modelo de 0 a 1000
    score_final = min(max(score, 0.0), 1000.0)

    # --------------------------------------
    # 6) Conversão para Porcentagem
    # --------------------------------------
    prob = sigmoid_1000(score_final)

    # Mantém a margem de segurança entre
    # 1% e 99.9% para candidatos ativos
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
    stmt = (
        select(Candidato)
        .where(
            and_(
                Candidato.faculdade == faculdade,
                Candidato.curso == curso,
                Candidato.periodo == periodo,
            )
        )
        .order_by(
            Candidato.nfc.desc(),
            Candidato.acertos.desc(),
        )
    )

    result = db.execute(stmt)
    candidatos = result.scalars().all()

    for rank, candidato in enumerate(candidatos, start=1):
        candidato.probabilidade = calcular_probabilidade_aprovacao(
            nfc=candidato.nfc,
            vagas=oferta.vagas,
            rank=None,
            cv=oferta.cand_vaga_historico,
            acertos=candidato.acertos,
            redacao=candidato.redacao,
            nota_corte=oferta.nota_corte_historica,
        )


def recalcular_todos_os_candidatos_do_banco(db: Session) -> dict:
    """
    Busca apenas as combinações de faculdade/curso/período que possuem
    pelo menos um candidato cadastrado e força o recálculo do grupo.
    """
    try:
        from ranking_fatec.cli import recalcular_todas_as_probabilidades

        contador_grupos = recalcular_todas_as_probabilidades(db)

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
