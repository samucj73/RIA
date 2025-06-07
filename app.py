import streamlit as st
import json
import time
import os
from fetch_and_save import fetch_latest_result, salvar_resultado_em_arquivo
from roleta_ia import RoletaIA

HISTORICO_PATH = "historico_resultados.json"

st.set_page_config(page_title="Roleta IA", layout="wide")
st.title("🎯 Previsão Inteligente de Roleta")

# Inicializar histórico
if "historico" not in st.session_state:
    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, "r") as f:
            st.session_state.historico = json.load(f)
    else:
        st.session_state.historico = []

# Captura automática do novo resultado
with st.empty():
    resultado = fetch_latest_result()

    if resultado:
        ultimo_timestamp = (
            st.session_state.historico[-1]["timestamp"]
            if st.session_state.historico else None
        )

        if resultado["timestamp"] != ultimo_timestamp:
            novo_resultado = {
                "number": resultado["number"],
                "color": resultado["color"],
                "timestamp": resultado["timestamp"],
                "lucky_numbers": resultado["lucky_numbers"]
            }
            st.session_state.historico.append(novo_resultado)
            salvar_resultado_em_arquivo([novo_resultado])
            st.rerun()
        else:
            st.write("🔍 Aguardando novo sorteio...")
            time.sleep(5)
            st.rerun()

# Exibir últimos sorteios
st.subheader("Últimos Sorteios")
st.write([h["number"] for h in st.session_state.historico[-10:]])

# Previsão baseada em IA
st.subheader("🔮 Previsão de Próximos 4 Números Mais Prováveis")

ia = RoletaIA()
previsoes = ia.prever_numeros(st.session_state.historico)

if previsoes:
    st.success(f"Números Prováveis: {previsoes}")
else:
    st.warning("Aguardando pelo menos 20 sorteios válidos para iniciar previsões.")

# Mostrar histórico completo opcional
with st.expander("📜 Ver histórico completo"):
    st.json(st.session_state.historico)
