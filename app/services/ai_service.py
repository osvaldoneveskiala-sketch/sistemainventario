from sklearn.linear_model import LinearRegression
import numpy as np


class AIService:

    @staticmethod
    def prever_stock(quantidade):

        X = np.array([
            [1],
            [5],
            [10],
            [20],
            [30],
            [50]
        ])

        y = np.array([
            0,
            0,
            1,
            1,
            2,
            2
        ])

        modelo = LinearRegression()

        modelo.fit(X, y)

        previsao = modelo.predict(
            [[quantidade]]
        )[0]

        if previsao < 0.5:
            return "Stock Baixo"

        elif previsao < 1.5:
            return "Stock Médio"

        else:
            return "Stock Alto"