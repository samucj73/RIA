import streamlit as st
import json
import os
from fetch_and_save import fetch_latest_result, salvar_resultado_em_arquivo
from roleta_ia import RoletaIA
from streamlit_autorefresh import st_autorefresh

HISTORICO_PATH = "historico_resultados.json"

st.set_page_config(page_title="Roleta IA", layout="wide")
st.title("🎯 Previsão Inteligente de Roleta")

# Autorefresh a cada 40 segundos (40000 ms)
count = st_autorefresh(interval=40000, limit=None, key="auto_refresh")

# Inicializar histórico
if "historico" not in st.session_state:
    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, "r") as f:
            try:
                st.session_state.historico = json.load(f)
            except json.JSONDecodeError:
                st.session_state.historico = []
    else:
        st.session_state.historico = []

# Buscar resultado mais recente da API
resultado = fetch_latest_result()

ultimo_timestamp = (
    st.session_state.historico[-1]["timestamp"] if st.session_state.historico else None
)

if resultado:
    if resultado["timestamp"] != ultimo_timestamp:
        novo_resultado = {
            "number": resultado["number"],
            "color": resultado["color"],
            "timestamp": resultado["timestamp"],
            "lucky_numbers": resultado["lucky_numbers"]
        }
        st.session_state.historico.append(novo_resultado)
        salvar_resultado_em_arquivo([novo_resultado])

        st.toast(f"🆕 Novo número capturado: **{novo_resultado['number']}** ({novo_resultado['color']})", icon="🎲")
    else:
        st.info("⏳ Aguardando novo sorteio...")
else:
    st.error("❌ Falha ao obter dados da API.")

# Mostrar últimos sorteios
st.subheader("🧾 Últimos Sorteios (números)")
st.write([h["number"] for h in st.session_state.historico[-10:]])

# Mostrar data/hora do último sorteio
if st.session_state.historico:
    ultimo = st.session_state.historico[-1]
    st.caption(f"⏰ Último sorteio registrado: {ultimo['timestamp']}")

# Previsão baseada em IA
st.subheader("🔮 Previsão de Próximos 4 Números Mais Prováveis")
ia = RoletaIA()
previsoes = ia.prever_numeros(st.session_state.historico)

if previsoes:
    st.success(f"Números Prováveis: {previsoes}")
else:
    st.warning("Aguardando pelo menos 20 sorteios válidos para iniciar previsões.")

# Histórico completo opcional
with st.expander("📜 Ver histórico completo"):
    st.json(st.session_state.historico)

# Exibir conteúdo do arquivo salvo, pra facilitar debug
with st.expander("📂 Ver conteúdo bruto salvo (JSON)"):
    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, "r") as f:
            st.code(f.read(), language="json")
    else:
        st.info("Nenhum histórico salvo ainda.")

# Rodapé
st.markdown("---")
st.caption("🔁 Atualiza automaticamente a cada 40 segundos.")
st.caption("🤖 Desenvolvido com aprendizado de máquina online via `SGDClassifier`.")
