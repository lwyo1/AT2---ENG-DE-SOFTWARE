from reserva import Reserva

LIMITE_SEMANAL = 3

class ReservaInvalida(Exception):
    pass

def marcar_horario(aluno, horario, topico):
    if not aluno.pode_reservar(horario):
        raise ReservaInvalida("Monitor não pode reservar horário da própria matéria")
    if horario.cancelado:
        raise ReservaInvalida("O horário está cancelado.")
    if not horario.tem_vaga():
        raise ReservaInvalida("O horário não tem vagas disponíveis.")
    if not horario.materia.tem_topico(topico):
        raise ReservaInvalida("O tópico não pertence à matéria do horário.")
    if aluno.reserva_Semana(horario.materia, horario.data) >= LIMITE_SEMANAL:
        raise ReservaInvalida("O aluno já atingiu o limite de reservas semanais.")
    
    nova = Reserva(aluno, horario, topico)
    horario.adicionar_reserva(nova)
    aluno.adicionar_reserva(nova)
    
    return nova