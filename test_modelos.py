import math

import sqlalchemy as sa
from sqlalchemy.orm import Session

from ranking_fatec.db import get_db
from ranking_fatec.models import Candidato, Oferta

# =====================================================================
# 1. OS DOIS MODELOS DE CÁLCULO
# =====================================================================


def sigmoid_1000(score: float) -> float:
    x = (score - 500) * 0.025
    return 1.0 / (1.0 + math.exp(-x))


def converter_probabilidade(score: float) -> float:
    score_final = min(max(score, 0.0), 1000.0)
    prob = sigmoid_1000(score_final)
    return round(min(max(prob * 100, 1.0), 99.9), 2)


def modelo_v1_estatico(nfc: float, nota_corte: float) -> float:
    """Modelo Atual: Pesos fixos sem influência do C/V na nota de corte."""
    score = 500.0
    nota_corte_ajustada = nota_corte * 0.965
    diff = nfc - nota_corte_ajustada

    if diff >= 0:
        score += min(diff * 20.0, 450.0)
    else:
        score -= min(abs(diff) * 35.0, 500.0)

    return converter_probabilidade(score)


def modelo_v2_dinamico_cv(nfc: float, cv: float, nota_corte: float) -> float:
    """Novo Modelo: O C/V atual do curso dita a rigidez da nota de corte."""
    score = 500.0
    nota_corte_ajustada = nota_corte * 0.965
    diff = nfc - nota_corte_ajustada

    # C/V padrão ancorado em 3.5. Ajusta a sensibilidade da reta.
    fator_cv = math.log1p(cv) / math.log1p(3.5)

    if diff >= 0:
        score += min(diff * (20.0 * fator_cv), 450.0)
    else:
        score -= min(abs(diff) * (35.0 * fator_cv), 500.0)

    return converter_probabilidade(score)


# =====================================================================
# 2. QUERY COM JOIN POR IDENTIFICADORES E ANÁLISE
# =====================================================================


def analisar_variacoes_no_bd(db: Session):
    print("=" * 80)
    print("   RELATÓRIO DE IMPACTO: MODELO ESTÁTICO VS DINÂMICO (PESO C/V)   ")
    print("=" * 80)

    # Cria o select unindo as tabelas pelos identificadores equivalentes
    stmt = sa.select(Candidato, Oferta).join(
        Oferta,
        sa.and_(
            Candidato.faculdade == Oferta.campus,
            Candidato.periodo == Oferta.periodo,
            Candidato.curso == Oferta.curso,
        ),
    )

    resultados = db.execute(stmt).all()

    total_analisado = 0
    mudancas_significativas = 0

    for cand, oferta in resultados:
        # Filtros básicos de segurança (pula desclassificados do edital)
        if cand.redacao == 0.0 or cand.acertos == 0:
            continue

        # Pula se a oferta não tiver dados históricos preenchidos
        if oferta.nota_corte_historica is None or oferta.cand_vaga_historico is None:
            continue

        nfc = cand.nfc
        cv = oferta.cand_vaga_historico
        corte = oferta.nota_corte_historica
        corte_ajustado = corte * 0.965

        # Se o C/V for de vaga sobrando (<= 1.0), pula porque ambos dariam 100%
        if cv <= 1.0:
            continue

        total_analisado += 1

        # Executa as duas variantes para comparação
        prob_v1 = modelo_v1_estatico(nfc, corte)
        prob_v2 = modelo_v2_dinamico_cv(nfc, cv, corte)
        diff = round(prob_v2 - prob_v1, 2)

        # Mostra apenas mudanças onde a diferença de probabilidade seja perceptível (>= 1.0%)
        if abs(diff) >= 1.0:
            mudancas_significativas += 1
            status_corte = "ACIMA" if nfc >= corte_ajustado else "ABAIXO"

            print(f"\n👤 Candidato: {cand.nome}")
            print(
                f"🎓 {oferta.campus} • {oferta.curso} ({oferta.periodo}) | Vagas: {oferta.vagas} | C/V: {cv}"
            )
            print(
                f"📝 Nota NFC: {nfc} | Corte Projetado: {round(corte_ajustado, 2)} ({status_corte})"
            )
            print(f"   ↳ [V1 Estático]: {prob_v1}%")
            print(f"   ↳ [V2 C/V Dinâmico]: {prob_v2}% (Variação: {diff:+}%)")

            if diff < 0:
                print("   ⚠️ Alta concorrência aumentou o rigor: a chance caiu.")
            else:
                print("   ✅ Baixa concorrência suavizou a régua: a chance subiu.")

    print("\n" + "=" * 80)
    print(f"📊 RESUMO DO IMPACTO:")
    print(f"Total de candidatos válidos cruzados: {total_analisado}")
    print(
        f"Candidatos afetados pela concorrência (diff >= 1%): {mudancas_significativas}"
    )
    if total_analisado > 0:
        percentual = round((mudancas_significativas / total_analisado) * 100, 1)
        print(f"Percentual de alteração na base: {percentual}%")
    print("=" * 80)


if __name__ == "__main__":
    # Roda utilizando o generator padrão do get_db
    with next(get_db()) as session:
        analisar_variacoes_no_bd(session)
