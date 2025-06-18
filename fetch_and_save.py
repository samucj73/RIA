import requests
import json
import os
import logging

API_URL = "https://api.casinoscores.com/svc-evolution-game-events/api/xxxtremelightningroulette/latest"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_latest_result():
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Lança erro para status != 200
        data = response.json()
        game_data = data.get("data", {})
        result = game_data.get("result", {})
        outcome = result.get("outcome", {})
        lucky_list = result.get("luckyNumbersList", [])

        number = outcome.get("number")
        color = outcome.get("color", "-")
        timestamp = game_data.get("startedAt")
        lucky_numbers = [item["number"] for item in lucky_list]

        return {
            "number": number,
            "color": color,
            "timestamp": timestamp,
            "lucky_numbers": lucky_numbers
        }
    except Exception as e:
        logging.error(f"Erro ao buscar resultado da API: {e}")
        return None

def salvar_resultado_em_arquivo(history, caminho="historico_resultados.json"):
    dados_existentes = []

    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            try:
                dados_existentes = json.load(f)
            except json.JSONDecodeError:
                logging.warning("Arquivo JSON vazio ou corrompido. Recriando arquivo.")
                dados_existentes = []

    timestamps_existentes = {item['timestamp'] for item in dados_existentes}

    novos_filtrados = [item for item in history if item['timestamp'] not in timestamps_existentes]

    if novos_filtrados:
        logging.info(f"Adicionando {len(novos_filtrados)} novos resultados ao arquivo.")
    else:
        logging.info("Nenhum novo resultado para adicionar.")

    dados_existentes.extend(novos_filtrados)
    dados_existentes.sort(key=lambda x: x['timestamp'])

    with open(caminho, "w") as f:
        json.dump(dados_existentes, f, indent=2)
