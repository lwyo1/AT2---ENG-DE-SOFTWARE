import unittest
from datetime import datetime

from materia import Materia
from horario import Horario
from usuarios import Aluno, Monitor

class CenarioBase(unittest.TestCase):
    """Monta uma matéria e um monitor novos antes de cada teste."""
    def setUp(self):
        self.calculo = Materia("Cálculo 1", ["Limites", "Derivadas"])
        self.monitor = Monitor("a1", "Monitor", self.calculo)

    def novo_horario(self, hora, capacidade=1):
        h = Horario(self.calculo, self.monitor, datetime(2026, 10, 19, hora, 0), capacidade)
        self.calculo.adicionar_horario(h)
        return h
    
class TestCriterio1HorariosLivres(CenarioBase):
    def test_lista_apenas_horarios_livres_da_disciplina(self): ...
    def test_horario_lotado_nao_aparece(self):
        # Preparar: horário individual que já tem 1 reserva (lotado)
        lotado = Horario(self.calculo, self.monitor, datetime(2026, 10, 19, 14, 0))
        lotado.adicionar_reserva("reserva qualquer")   # simula a reserva, Reserva ainda não existe
        self.calculo.adicionar_horario(lotado)

        # Executar
        livres = self.calculo.horarios_livres()

        # Conferir
        self.assertNotIn(lotado, livres)
    

class TestCriterio6HorarioCancelado(CenarioBase):
    def test_horario_cancelado_nao_aparece(self): ...


if __name__ == "__main__":
    unittest.main()