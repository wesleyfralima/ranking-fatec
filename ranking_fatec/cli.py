import logging

from sqlalchemy import Row
from sqlalchemy.orm import Session

from ranking_fatec.dados import DADOS_OFERTAS_INICIAIS
from ranking_fatec.db import get_db
from ranking_fatec.main import recalcular_probabilidades
from ranking_fatec.models import Candidato, Oferta


def buscar_grupos_de_candidatos_ativos(db: Session) -> list[Row[tuple[str, str, str]]]:
    """
    Busca as combinações distintas de campus/curso/período preenchidas por candidatos.
    """
    return (
        db.query(Candidato.faculdade, Candidato.curso, Candidato.periodo)
        .distinct()
        .all()
    )


def recalcular_todas_as_probabilidades(db: Session) -> int:
    """
    Identifica os grupos ativos de candidatos e dispara o recálculo
    lógico das posições e chances de aprovação de cada um.
    """

    try:
        grupos_ativos = buscar_grupos_de_candidatos_ativos(db)
        contador_grupos = 0

        for faculdade, curso, periodo in grupos_ativos:
            recalcular_probabilidades(
                db=db, faculdade=faculdade, curso=curso, periodo=periodo
            )
            contador_grupos += 1

        db.commit()
        return contador_grupos

    except Exception as e:
        db.rollback()
        logging.error(f"Erro ao rodar recálculo geral: {str(e)}")
        raise e


def sincronizar_oferta_individual(db: Session, dados_oferta: tuple) -> bool:
    """
    Insere uma nova oferta ou atualiza seus parâmetros históricos (vagas, corte, C/V)
    caso ela já exista no banco de dados. Retorna True se for uma inserção (New).
    """

    campus, periodo, curso, vagas, corte, cv = dados_oferta

    oferta = (
        db.query(Oferta)
        .filter(
            Oferta.campus == campus,
            Oferta.periodo == periodo,
            Oferta.curso == curso,
        )
        .first()
    )

    if oferta is None:
        db.add(
            Oferta(
                campus=campus,
                periodo=periodo,
                curso=curso,
                vagas=vagas,
                nota_corte_historica=corte,
                cand_vaga_historico=cv,
            )
        )
        return True  # Inserido
    else:
        oferta.vagas = vagas
        oferta.nota_corte_historica = corte
        oferta.cand_vaga_historico = cv
        return False  # Atualizado


def processar_carga_de_ofertas(db: Session) -> tuple[int, int]:
    """Varre a lista de dados brutos salvando e estruturando as ofertas no banco."""

    inseridos = 0
    atualizados = 0

    for dados in DADOS_OFERTAS_INICIAIS:
        foi_inserido = sincronizar_oferta_individual(db, dados)
        if foi_inserido:
            inseridos += 1
        else:
            atualizados += 1

    db.commit()
    return inseridos, atualizados


def sincronizar_sistema() -> None:
    """Controlador principal do script CLI que coordena a carga e os recálculos."""

    db = next(get_db())

    try:
        print("🚀 Iniciando sincronização de ofertas...")
        inseridos, atualizados = processar_carga_de_ofertas(db)
        print(
            f"✓ Ofertas atualizadas. "
            f"Inseridas: {inseridos} | Atualizadas: {atualizados}"
        )

        print("🔮 Atualizando probabilidades com base nos novos parâmetros...")
        grupos_afetados = recalcular_todas_as_probabilidades(db)
        print(
            f"✓ Sucesso! "
            f"{grupos_afetados} grupos de candidatos ativos foram recalculados."
        )

    finally:
        db.close()


if __name__ == "__main__":
    sincronizar_sistema()
