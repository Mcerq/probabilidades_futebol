from controllers.campeonato_controller import CampeonatoController

if __name__ == "__main__":
    url = 'https://fbref.com/pt/comps/24/cronograma/Serie-A-Resultados-e-Calendarios'
    controller = CampeonatoController(url)
    controller.executar_analises()
