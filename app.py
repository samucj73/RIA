import streamlit as st
import time
import os
import json
from fetch_and_save import fetch_latest_result, salvar_resultado_em_arquivo

HISTORICO_PATH = "historico_resultados.json"

st.set_page_config(page_title="Roleta IA", layout="wide")
st.title("🎯 Previsão Inteligente de Roleta")

# Inicializar histórico na sessão
if "historico" not in st.session_state:
    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, "r") as f:
            try:
                st.session_state.historico = json.load(f)
            except:
                st.session_state.historico = []
    else:
        st.session_state.historico = []

def salvar_historico_unico(history, caminho=HISTORICO_PATH):
    dados_existentes = []
    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            try:
                dados_existentes = json.load(f)
            except:
                dados_existentes = []
    todos = dados_existentes + history
    seen = {}
    for item in todos:
        seen[item["timestamp"]] = item
    dados_unicos = list(seen.values())
    dados_unicos.sort(key=lambda x: x["timestamp"])
    with open(caminho, "w") as f:
        json.dump(dados_unicos, f, indent=2)

# Função para buscar resultado e atualizar se houver novidade
def atualizar_resultado():
    resultado = fetch_latest_result()
    ultimo_timestamp = st.session_state.historico[-1]["timestamp"] if st.session_state.historico else None

    if resultado and resultado["timestamp"] != ultimo_timestamp:
        novo_resultado = {
            "number": resultado["number"],
            "color": resultado["color"],
            "timestamp": resultado["timestamp"],
            "lucky_numbers": resultado["lucky_numbers"]
        }
        st.session_state.historico.append(novo_resultado)
        salvar_historico_unico([novo_resultado])
        st.experimental_rerun()

# Loop de atualização automática (polling a cada 5 segundos)
atualizar_resultado()
st.info("🔄 Aguardando novo sorteio... (a página vai atualizar automaticamente)")

# Exibir últimos 10 números sorteados
st.subheader("🧾 Últimos Sorteios (números)")
st.write([h["number"] for h in st.session_state.historico[-10:]])

# Mostrar data/hora do último sorteio
if st.session_state.historico:
    ultimo = st.session_state.historico[-1]
    st.caption(f"⏰ Último sorteio registrado: {ultimo['timestamp']}")

# Aqui você pode colocar a parte da previsão da IA se quiser

# Pausa para aguardar próximo fetch (controla a velocidade do polling)
time.sleep(5)
st.experimental_rerun()
