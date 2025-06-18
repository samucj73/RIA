import streamlit as st
import json
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

# Capturar resultado mais recente da API
resultado = fetch_latest_result()
ultimo_timestamp = (
    st.session_state.historico[-1]["timestamp"] if st.session_state.historico else None
)

# Se chegou novo resultado, adiciona ao histórico e para execução para forçar rerun
if resultado and resultado["timestamp"] != ultimo_timestamp:
    novo_resultado = {
        "number": resultado["number"],
        "color": resultado["color"],
        "timestamp": resultado["timestamp"],
        "lucky_numbers": resultado["lucky_numbers"]
    }
    st.session_state.historico.append(novo_resultado)
    salvar_resultado_em_arquivo([novo_resultado])
    st.experimental_rerun()
    st.stop()  # ⛔️ Impede renderização com dados desatualizados

# Exibir últimos sorteios
st.subheader("🧾 Últimos Sorteios (números)")
st.write([h["number"] for h in st.session_state.historico[-10:]])

# Exibir timestamp
if st.session_state.historico:
    ultimo = st.session_state.historico[-1]
    st.caption(f"⏰ Último sorteio registrado: {ultimo['timestamp']}")

# Previsão com IA
st.subheader("🔮 Previsão de Próximos 4 Números Mais Prováveis")
ia = RoletaIA()
previsoes = ia.prever_numeros(st.session_state.historico)

if previsoes:
    st.success(f"Números Prováveis: {previsoes}")
else:
    st.warning("Aguardando pelo menos 20 sorteios válidos para iniciar previsões.")

# Histórico completo
with st.expander("📜 Ver histórico completo"):
    st.json(st.session_state.historico)

# Rodapé
st.markdown("---")
st.caption("🔁 Atualização automática instantânea sempre que novo número for sorteado.")
st.caption("🤖 Desenvolvido com aprendizado de máquina online via `SGDClassifier`.")
