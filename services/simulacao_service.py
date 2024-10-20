import random

class SimulacaoService:

    def __init__(self, numero_simulacoes=1000):

        self.numero_simulcoes = numero_simulacoes

    def simular_partida(self, prob_mandante, prob_empate, prob_visitante):

        resultados = {"mandante":0, "empate":0, "visitante":0}

        for _ in range(self.numero_simulacoes):

            resultado = random.choices(
                ["mandante", "empate", "visitante"],
                [prob_mandante, prob_empate, prob_visitante]
            )[0]
            resultados[resultado] += 1
        
        return resultados