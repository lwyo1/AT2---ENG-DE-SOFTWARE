from datetime import timedelta
from uuid import uuid4

DURACAO = timedelta(minutes=30)

class Horario:
    #atendimento de 30 min
    
    def __init__(self, materia, monitor, data, capacidade=1):
        if capacidade<1:
            raise ValueError("A capacidade deve ser pelo menos 1")
        
        self.materia = materia
        self.monitor = monitor
        self.id = uuid4().hex
        self.data = data
        self.capacidade = capacidade
        self.cancelado = False
        self.reservas = []
        
    @property
    def tipo(self):
        if self.capacidade ==1:
            return "Individual"
        return "Grupo"
            
    @property
    def fim(self):
        return self.data + DURACAO
    
    def vagas_restantes(self):
        return self.capacidade - len(self.reservas)
    
    def tem_vaga(self):
        return self.vagas_restantes() > 0
    
    def esta_livre(self):
        """Livre = nao cancelado e com vaga. Usado na listagem da materia."""
        return not self.cancelado and self.tem_vaga()

    
    def adicionar_reserva(self, reserva):
        self.reservas.append(reserva)
        
    def cancelar(self):
        self.cancelado = True
        
    