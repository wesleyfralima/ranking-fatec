import sqlalchemy as sa
import sqlalchemy.orm as so

from ranking_fatec.db import Base


class Oferta(Base):
    __tablename__ = "ofertas"

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True, index=True)
    campus: so.Mapped[str] = so.mapped_column(sa.String, index=True)
    periodo: so.Mapped[str] = so.mapped_column(sa.String, index=True)
    curso: so.Mapped[str] = so.mapped_column(sa.String, index=True)

    vagas: so.Mapped[int | None] = so.mapped_column(sa.Integer)
    nota_corte_historica: so.Mapped[float | None] = so.mapped_column(sa.Float)
    cand_vaga_historico: so.Mapped[float | None] = so.mapped_column(sa.Float)

    __table_args__ = (
        sa.UniqueConstraint(
            "campus",
            "periodo",
            "curso",
            name="uix_campus_periodo_curso",
        ),
    )


class Candidato(Base):
    __tablename__ = "ranking"

    # O nome é utilizado como chave única
    # para evitar duplicidades (UPSERT)
    nome: so.Mapped[str] = so.mapped_column(
        sa.String(100),
        primary_key=True,
        index=True,
    )

    faculdade: so.Mapped[str] = so.mapped_column(sa.String(100))
    curso: so.Mapped[str] = so.mapped_column(sa.String(100))
    periodo: so.Mapped[str] = so.mapped_column(sa.String(20))
    acertos: so.Mapped[int] = so.mapped_column(sa.Integer)
    redacao: so.Mapped[float] = so.mapped_column(sa.Float)
    nota_enem: so.Mapped[float | None] = so.mapped_column(sa.Float)
    is_afro: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    is_publica: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    nfc: so.Mapped[float] = so.mapped_column(sa.Float)

    probabilidade: so.Mapped[float | None] = so.mapped_column(sa.Float)

    # Armazenado no formato JSON
    respostas: so.Mapped[str] = so.mapped_column(sa.String(60))
