class Reserva:
    def __init__(self, aluno, horario, topico):
        self.aluno = aluno
        self.horario = horario
        self.topico = topico
    
    def __str__(self):
        return f"Reserva de {self.aluno.nome} para {self.horario.materia.nome} no dia {self.horario.data.strftime('%d/%m/%Y %H:%M')} sobre o tópico '{self.topico}'"
