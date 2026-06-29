from ranking_fatec.dados import DADOS_OFERTAS_INICIAIS
from ranking_fatec.db import get_db
from ranking_fatec.models import Oferta


def popular_banco() -> None:
    db = next(get_db())

    try:
        inseridos = 0
        atualizados = 0

        print("Sincronizando ofertas...")

        for campus, periodo, curso, vagas, corte, cv in DADOS_OFERTAS_INICIAIS:
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
                inseridos += 1

            else:
                oferta.vagas = vagas
                oferta.nota_corte_historica = corte
                oferta.cand_vaga_historico = cv
                atualizados += 1

        db.commit()

        print(f"Concluído. Inseridos: {inseridos} | Atualizados: {atualizados}")

    finally:
        db.close()


if __name__ == "__main__":
    popular_banco()
