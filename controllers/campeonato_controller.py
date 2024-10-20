from repositories.web_data_repository import WebDataRepository
from models.campeonato import Campeonato
from models.probabilidade import Probabilidade
import pandas as pd

class CampeonatoController:
    """Controlador que lida com as operações do campeonato."""

    def __init__(self, url):
        self.partidas_df = WebDataRepository.carregar_partidas_da_web(url)
        self.campeonato = Campeonato(self.partidas_df)

    def executar_analises(self):
        # Operações de análise de partidas realizadas
        jogos_mandante = self.campeonato.partidas_processadas.groupby("mandante")
        jogos_visitante = self.campeonato.partidas_processadas.groupby("visitante")
        tabela_final = self.campeonato.gerar_tabela()

        # Cálculo de probabilidades
        matriz_probabilidade = Probabilidade.calcular_probabilidades(
            self.partidas_df, jogos_mandante, jogos_visitante, tabela_final
        )

        # Operações para jogos não realizados
        df_nao_realizado = self.jogos_nao_realizados()
        dframe = self.jogos_nao_realizados_rodadas(df_nao_realizado)
        numero_rodadas = dframe.shape[0]

        # Criação dos dataframes necessários
        df_new_match = pd.DataFrame(columns=[
            'mandante', 'visitante', 'ponto_mandante', 'vitorias_mandante',
            'empate_mandante', 'derrota_mandante', 'ponto_visitante',
            'vitorias_visitante', 'empate_visitante', 'derrota_visitante'
        ])
        tabela_final_new = pd.DataFrame(columns=[
            'Clubes', 'J', 'P', 'V', 'E', 'D'
        ])

        # Simulação da próxima rodada
        rand = 50000
        results_proxima_rodada = self.probabilidade_proxima_rodada(
            df_nao_realizado, dframe.iloc[0, 0], matriz_probabilidade, rand
        )
        df1 = self.tabela_previsao(results_proxima_rodada)

        # Combinar dataframes e exibir resultados
        df_new_match = pd.concat([self.partidas_df, df1])
        print(f"rodada {dframe.iloc[0, 0]:.0f} ok.")

    def jogos_nao_realizados(self):
        """Retorna DataFrame com partidas não realizadas."""
        return self.partidas_df[self.partidas_df["Notas"] == "Partida não realizada"]

    def jogos_nao_realizados_rodadas(self, df):
        """Agrupa partidas não realizadas por rodada."""
        return df.groupby("Rodada").size().reset_index()

    def probabilidade_proxima_rodada(self, df_nao_realizado, rodada, matriz_probabilidade, rand):
        """Simula a próxima rodada com base em probabilidades."""
        # Implementação da simulação...
        df_nextmatchs = df_input[df_input['Sem'] == rodada]
        df_nextmatchs = df_nextmatchs.reset_index(drop=True)
        df_final_results = pd.DataFrame(columns=['mandante',
               'prob_vitoria_mandante',
               'prob_empate',
               'prob_vitoria_visite',
               'visitante'
           ])

        for index, row in df_nextmatchs.iterrows():
        
          mandante = row['mandante']
          visitante = row['visitante']
          df_mand = probabilidades_algoritmo[probabilidades_algoritmo['clubes'] == mandante]
          df_visit = probabilidades_algoritmo[probabilidades_algoritmo['clubes'] == visitante]

          vitoria_mandante = (df_mand.iloc[0,1]+df_visit.iloc[0,6])/2
          empate = (df_mand.iloc[0,3]+df_visit.iloc[0,4])/2
          derrota_mandante = (df_mand.iloc[0,2]+df_visit.iloc[0,5])/2

          df_game = pd.DataFrame(columns=['mandante',
                     'vitorias_mandante',
                     'empates',
                     'vitorias_visitante',
                     'visitante'
                 ])


          for loop in range(numero_simulacoes):

            x = random.random()
            if(x<= vitoria_mandante):
            
              vitoria_do_mandante = 1
              vitoria_visitante = 0
              empate_mandante = 0

            elif(x<= vitoria_mandante + empate):
            
              empate_mandante = 1
              vitoria_do_mandante = 0
              vitoria_visitante = 0

            else:
            
              vitoria_do_mandante = 0
              vitoria_visitante = 1
              empate_mandante = 0

            subjects = [{'mandante': mandante,
                     'vitorias_mandante': vitoria_do_mandante,
                     'empates': empate_mandante,
                     'vitorias_visitante': vitoria_visitante,
                     'visitante': visitante
                 }]

            df_game2 = pd.DataFrame.from_records(subjects)

            if loop == 0:
              df_game = df_game2
            else:
              df_game = pd.concat([df_game, df_game2], ignore_index=True)


          df_game_1 = df_game.groupby(['mandante','visitante']).agg({'vitorias_mandante':'sum', 'empates':'sum', 'vitorias_visitante':'sum'})
          df_game_1 = df_game_1.reset_index()
          df_game_1['prob_vitoria_mandante'] = (df_game_1.iloc[0,2] / numero_simulacoes)*100
          df_game_1['prob_empate']  = (df_game_1.iloc[0,3] / numero_simulacoes)*100
          df_game_1['prob_vitoria_visitante'] = (df_game_1.iloc[0,4] / numero_simulacoes)*100

          subjects2 = [{'mandante': mandante,
                     'prob_vitoria_mandante': (df_game_1.iloc[0,2] / numero_simulacoes)*100 ,
                     'prob_empate': (df_game_1.iloc[0,3] / numero_simulacoes)*100,
                     'prob_vitoria_visite': (df_game_1.iloc[0,4] / numero_simulacoes)*100,
                     'visitante': visitante
                 }]
          df_final_results_2 = pd.DataFrame.from_records(subjects2)
          if index == 0:
            df_final_results = df_final_results_2
          else:
            df_final_results = pd.concat([df_final_results, df_final_results_2], ignore_index=True)

#          print("Jogo "+ {index+1}+ " calculado! Jogo foi entre "+ {mandante} +" e "+ {visitante} +".")
#          print("   Vitoria Mandante: "+ str(df_final_results.iloc[index,1])+ "%. Empate: "+ str(df_final_results.iloc[index,2]) +"%. Vitória visitante: "+str(df_final_results.iloc[index,3])+"%.")
          print(f"Jogo {index + 1} calculado! Jogo foi entre {mandante} e {visitante}.")
          print(f"   Vitória Mandante: {df_final_results.iloc[index, 1]:.2f}%")
          print(f"   Empate: {df_final_results.iloc[index, 2]:.2f}%")
          print(f"   Vitória Visitante: {df_final_results.iloc[index, 3]:.2f}%")
          print(" ")

        return df_final_results

    def tabela_previsao(self, resultados_proxima_rodada):
        """Gera a tabela de previsão para a próxima rodada."""
        df_final_results_new = pd.DataFrame(columns=['mandante',
              'visitante',
              'ponto_mandante',
              'vitorias_mandante',
              'empate_mandante',
              'derrota_mandante',
              'ponto_visitante',
              'vitorias_visitante',
              'empate_visitante',
              'derrota_visitante',
             ])

        for index, row in df_input.iterrows():
        
          if((df_input.iloc[index,1] > df_input.iloc[index,2]) & (df_input.iloc[index,1] > df_input.iloc[index,3])):
            
            pontos_mandante = 3
            vitorias_mandante = 1
            empates_mandante = 0
            derrotas_mandante = 0
            pontos_visitante = 0
            vitorias_visitante = 0
            empates_visitante = 0
            derrotas_visitante = 1
        
          elif((df_input.iloc[index,2] > df_input.iloc[index,1]) & (df_input.iloc[index,2] > df_input.iloc[index,3])):
            
            pontos_mandante = 1
            vitorias_mandante = 0
            empates_mandante = 1
            derrotas_mandante = 0
            pontos_visitante = 1
            vitorias_visitante = 0
            empates_visitante = 1
            derrotas_visitante = 0
        
          elif((df_input.iloc[index,3] > df_input.iloc[index,1]) & (df_input.iloc[index,3] > df_input.iloc[index,2])):
            
            pontos_mandante = 0
            vitorias_mandante = 0
            empates_mandante = 0
            derrotas_mandante = 1
            pontos_visitante = 3
            vitorias_visitante = 0
            empates_visitante = 0
            derrotas_visitante = 3
        
        
        
          subjects = [{'mandante': df_input.iloc[index,0],
                    'visitante': df_input.iloc[index,4],
                    'ponto_mandante': pontos_mandante,
                    'vitorias_mandante': vitorias_mandante,
                    'empate_mandante': empates_mandante,
                    'derrota_mandante': derrotas_mandante,
                    'ponto_visitante': pontos_visitante,
                    'vitorias_visitante': vitorias_visitante,
                    'empate_visitante': empates_visitante,
                    'derrota_visitante': derrotas_visitante,
                 }]
        
          df_final_results_teste = pd.DataFrame.from_records(subjects)
        
          if index == 0:
            df_final_results_new = df_final_results_teste
          else:
            df_final_results_new = pd.concat([df_final_results_new, df_final_results_teste], ignore_index=True)
        
        
        
        return df_final_results_new