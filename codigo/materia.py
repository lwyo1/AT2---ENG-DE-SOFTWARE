import csv

class Materia:
    def __init__(self, nome, topicos):
        self.nome = nome
        self.topicos = topicos
        self.horarios = []

    def tem_topico(self, topico):
        return topico in self.topicos

    def horarios_livres(self):
        return [h for h in self.horarios if h.esta_livre()]
    
    def adicionar_horario(self, horario):
        self.horarios.append(horario)

def carregar_materias(arq):
    with open(arq, 'r', encoding='utf-8') as file:
        return [Materia(linha[0], linha[1:]) for linha in csv.reader(file) if linha]
    
    
    