import streamlit as st
import time
from fetch_and_save import fetch_latest_result, salvar_resultado_em_arquivo
from roleta_ia import RoletaIA
import json
import os

st.set_page_config(page_title="Roleta IA", layout="centered")

st.title("🎰 Previsor de Roleta com IA em Tempo Real")

# Inicializa IA
ia = RoletaIA()

HIST_PATH = "historico_resultados.json"

# Carrega histórico salvo (se houver)
if os.path.exists(HIST_PATH):
    with open(HIST_PATH, "r") as f:
        try:
            historico = json.load(f)
            ia.alimentar(historico)
        except json.JSONDecodeError:
            historico = []
else:
    historico = []

# Inicia coleta contínua
placeholder = st.empty()

while True:
    with placeholder.container():
        novo_resultado = fetch_latest_result()
        if novo_resultado and (not historico or novo_resultado["timestamp"] != historico[-1]["timestamp"]):
            historico.append(novo_resultado)
            salvar_resultado_em_arquivo([novo_resultado], HIST_PATH)
            ia.alimentar([novo_resultado])

        st.subheader("📌 Últimos 10 resultados")
        ultimos = historico[-10:]
        st.write([item["number"] for item in reversed(ultimos)])

        if ia.ativo():
            st.subheader("🔮 Previsão de IA (Top 4)")
            previsao = ia.prever()
            st.success(f"🎯 Números prováveis: {previsao}")
        else:
            st.warning(f"Aguardando pelo menos 20 sorteios... ({len(historico)}/20)")

        st.subheader("📊 Estatísticas (frequência dos últimos números)")
        st.write(ia.estatisticas())

    time.sleep(15)
