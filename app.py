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

# Inicializar variáveis de sessão
if "historico" not in st.session_state:
    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, "r") as f:
            try:
                st.session_state.historico = json.load(f)
            except json.JSONDecodeError:
                st.session_state.historico = []
    else:
        st.session_state.historico = []

if "acertos" not in st.session_state:
    st.session_state.acertos = []

if "previsoes" not in st.session_state:
    st.session_state.previsoes = []

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

        # Recalcula previsões SOMENTE se houver novo número
        ia = RoletaIA()
        st.session_state.previsoes = ia.prever_numeros(st.session_state.historico)

        # Verifica se houve acerto nas previsões
        if st.session_state.previsoes and resultado["number"] in st.session_state.previsoes:
            if resultado["number"] not in st.session_state.acertos:
                st.session_state.acertos.append(resultado["number"])
                st.toast(f"🎯 Acerto! Número {resultado['number']} estava na previsão!", icon="✅")
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
if st.session_state.previsoes:
    st.success(f"Números Prováveis: {st.session_state.previsoes}")
else:
    st.warning("Aguardando pelo menos 20 sorteios válidos para iniciar previsões.")

# Mostrar acertos registrados
st.subheader("🏅 Números Acertados pela IA")
col1, col2 = st.columns([4, 1])

with col1:
    if st.session_state.acertos:
        st.success(f"Números acertados até agora: {st.session_state.acertos}")
    else:
        st.info("Nenhum acerto registrado ainda.")

with col2:
    if st.button("🔄 Resetar Acertos"):
        st.session_state.acertos = []
        st.toast("Acertos resetados com sucesso!", icon="🧹")

# Taxa de acertos da IA
st.subheader("📈 Taxa de Acertos da IA")
total_previsoes_possiveis = len([
    h for h in st.session_state.historico if h["number"] not in (None, 0)
]) - 18  # só a partir do 19º sorteio há previsão

total_acertos = len(st.session_state.acertos)

if total_previsoes_possiveis > 0:
    taxa_acerto = (total_acertos / total_previsoes_possiveis) * 100
    st.info(f"🎯 Taxa de acerto da IA: **{taxa_acerto:.2f}%** ({total_acertos} acertos em {total_previsoes_possiveis} previsões)")
else:
    st.warning("🔎 Taxa de acertos será exibida após 20 sorteios.")

# Histórico completo opcional
with st.expander("📜 Ver histórico completo"):
    st.json(st.session_state.historico)

# Exibir conteúdo do arquivo salvo
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
