import pandas as pd

class Campeonato:

    def __init__(self, partidas_df):

        self.partidas_df =  partidas_df
        self.partidas_processadas = self._processar_partidas()

    def _processar_partidas(self):

        df_validas = self.partidas_df[
            (self.partidas_df["Resultado"] == "Relatório da Partida") &
            (self.partidas_df["Ntas"] != "Partida adiada")
        ]

        resultados = df_validas["Resultado"].str.split("-", expand=True).astype(int)
        df_validas["mandante_gol"] = resultados[0]
        df_validas["visitante_gol"] = resultados[1]

        return df_validas
    
    def calcular_pontos(self):

        df = self.partidas_processadas
        df["pontos_mandante"] = (df['mandante_gol'] > df['visitante_gol']).astype(int) * 3
        df["pontos_visitante"] =  (df['mandante_gol'] < df['visitante_gol']).astype(int) * 3

        return df
    def gerar_tabela(self):
        
        df = self.calcular_pontos()
        tabela = df.groupby("mandante").agg({"ponto_mandante": "sum"}).reset_index()

        return tabela
    
    