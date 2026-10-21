from abc import ABC, abstractmethod
class Estudante(ABC):
    #Classe abstrata para Aluno e Monitor
    
    def __init__(self,ra,nome):
        self.ra = ra
        self.nome = nome
        self.reservas = []
        
    def adicionar_reserva(self, reservas):
        self.reservas.append(reservas) 
    #alimenta a lista de reservas
    
    def reserva_Semana(self, materia, data):
        ano, semana, _ = data.isocalendar()
        total = 0
        
        for reserva in self.reservas:
            horario = reserva.horario
            if horario.cancelado or horario.materia is not materia:
                continue
            ano_r, semana_r, _ = horario.data.isocalendar()
            if (ano_r, semana_r) == (ano, semana):
                total +=1
        return total
        
    @abstractmethod
    def pode_reservar(self, horario):
        pass
        
class Aluno(Estudante):
    def pode_reservar(self, horario):
        return True

class Monitor(Estudante):
    #aluno com a materia da monitoria
    
    def __init__(self, ra, nome, materia):
        super().__init__(ra, nome)
        self.materia = materia
        
    def pode_reservar(self, horario):
        return horario.materia is not self.materia