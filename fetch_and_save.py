import requests
import json
import os

API_URL = "https://api.casinoscores.com/svc-evolution-game-events/api/xxxtremelightningroulette/latest"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_latest_result():
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=10)
        if response.status_code == 200:
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
    except:
        return None

def salvar_resultado_em_arquivo(history, caminho="historico_resultados.json"):
    dados_existentes = []

    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            try:
                dados_existentes = json.load(f)
            except json.JSONDecodeError:
                dados_existentes = []

    novos = list(reversed(history))
    dados_existentes.extend(novos)

    with open(caminho, "w") as f:
        json.dump(dados_existentes, f, indent=2)
