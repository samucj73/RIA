sklearn.preprocessing import StandardScaler
from collections import deque, Counter
import numpy as np

class RoletaIA:
    def __init__(self):
        self.modelo = SGDClassifier(loss="log_loss", max_iter=1000)
        self.scaler = StandardScaler()
        self.historico = deque(maxlen=200)
        self.X = []
        self.y = []
        self.treinado = False

    def _extrair_features(self, ultimo_n):
        return [ultimo_n % 2, ultimo_n % 3, 1 if 1 <= ultimo_n <= 18 else 0, 1 if ultimo_n in {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36} else 0]

    def alimentar(self, dados):
        for item in dados:
            n = item["number"]
            if n is None or n == 0:
                continue
            self.historico.append(n)

            if len(self.historico) > 5:
                X_i = self._extrair_features(self.historico[-2])
                self.X.append(X_i)
                self.y.append(n)

                if len(self.X) >= 20:
                    X_np = np.array(self.X)
                    y_np = np.array(self.y)
                    self.scaler.fit(X_np)
                    X_scaled = self.scaler.transform(X_np)
                    self.modelo.partial_fit(X_scaled, y_np, classes=np.arange(1, 37))
                    self.X.clear()
                    self.y.clear()
                    self.treinado = True

    def prever(self):
        if not self.ativo():
            return []
        ultimo = self.historico[-1]
        X_test = [self._extrair_features(ultimo)]
        X_scaled = self.scaler.transform(X_test)
        probs = self.modelo.predict_proba(X_scaled)[0]
        top = np.argsort(probs)[-4:][::-1]
        return list(top + 1)

    def estatisticas(self):
        contagem = Counter(self.historico)
        return contagem.most_common(10)

    def ativo(self):
        return self.treinado
