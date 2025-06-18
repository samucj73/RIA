from collections import Counter
from sklearn.linear_model import SGDClassifier
import numpy as np

def get_color(n):
    if n == 0:
        return -1  # Verde
    return 1 if n in {
        1, 3, 5, 7, 9, 12, 14, 16, 18,
        19, 21, 23, 25, 27, 30, 32, 34, 36
    } else 0

def get_coluna(n):
    return (n - 1) % 3 + 1 if n != 0 else 0

def get_linha(n):
    return ((n - 1) // 3) + 1 if n != 0 else 0

def extrair_features(numero, freq):
    return [
        numero % 2,                      # Par/Ímpar
        numero % 3,                      # Resto por 3
        1 if 19 <= numero <= 36 else 0, # Alto/Baixo
        get_color(numero),              # Cor
        get_coluna(numero),             # Coluna
        get_linha(numero),              # Linha
        freq.get(numero, 0)             # Frequência histórica
    ]

def construir_entrada(janela, freq):
    features = []
    for n in janela:
        features.extend(extrair_features(n, freq))
    return features

class ModeloIA:
    def __init__(self):
        self.modelo = SGDClassifier(loss="log_loss")
        self.classes_ = np.array(list(range(37)))
        self.iniciado = False

    def treinar(self, entradas, saidas):
        X = np.array(entradas)
        y = np.array(saidas)
        if not self.iniciado:
            self.modelo.partial_fit(X, y, classes=self.classes_)
            self.iniciado = True
        else:
            self.modelo.partial_fit(X, y)

    def prever(self, entrada):
        if not self.iniciado:
            return []
        proba = self.modelo.predict_proba([entrada])[0]
        top_indices = np.argsort(proba)[::-1][:4]
        return list(top_indices)

class RoletaIA:
    def __init__(self):
        self.modelo = ModeloIA()

    def prever_numeros(self, historico):
        # Filtra números válidos (diferentes de 0)
        numeros = [item["number"] for item in historico if item["number"] != 0]

        if len(numeros) < 20:
            return []

        entradas = []
        saidas = []

        for i in range(18, len(numeros) - 1):
            janela = numeros[i-18:i]
            saida = numeros[i]
            freq = Counter(numeros[:i])  # Frequência até a posição atual
            entrada = construir_entrada(janela, freq)
            entradas.append(entrada)
            saidas.append(saida)

        if entradas and saidas:
            self.modelo.treinar(entradas, saidas)

        # Prever com os últimos 18 números
        janela_recente = numeros[-18:]
        freq_final = Counter(numeros[:-1])  # Exclui o último para não "vazar" no treino
        entrada = construir_entrada(janela_recente, freq_final)
        return self.modelo.prever(entrada)
