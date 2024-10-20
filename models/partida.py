class Partida:

    def __init__(self,mandante,visitante, resultado, notas):
    
        self.mandante = mandante
        self.visitante = visitante
        self.resultado = resultado
        self.notas = notas

    def parse_resultado(self):
    
        gols_mandante, gols_visitante = map(int, self.resultado.split("-"))
        return gols_mandante, gols_visitante


    def partida_valida(self):

        return self.notas != "Partida adiada"