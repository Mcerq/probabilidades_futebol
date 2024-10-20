import pandas as pd

class WebDataRepository:


    @staticmethod
    def carregar_partidas_web(url):

        try:

            webpage_df = pd.read_html(url)[0]
            return webpage_df
        except Exception as e:

            print(f"Erro ao carregar os dados: {e}")
            return pd.DataFrame()
        
