class Probabilidade:

    @staticmethod
    def calcular_probabilidades(df, clube):

        total_jogos = len(df)
        if total_jogos == 0:
            return 0,0,0
    
        prob_vitoria = (df['mandante_gol'] > df['visitante_gol']).mean()
        prob_empate = (df['mandante_gol'] == df['visitante_gol']).mean()
        prob_derrota = (df['mandante_gol'] < df['visitante_gol']).mean()


        return prob_vitoria, prob_empate, prob_derrota