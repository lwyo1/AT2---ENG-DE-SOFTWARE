import unittest
from datetime import datetime

from agendamento import marcar_horario, ReservaInvalida
from materia import Materia
from horario import Horario
from usuarios import Aluno, Monitor

class CenarioBase(unittest.TestCase):
    """Monta uma matéria e um monitor novos antes de cada teste."""
    def setUp(self):
        self.calculo = Materia("Cálculo 1", ["Limites", "Derivadas"])
        self.monitor = Monitor("a1", "Monitor", self.calculo)
        self.aluno = Aluno("a2", "Aluno")

    def novo_horario(self, hora, capacidade=1):
        h = Horario(self.calculo, self.monitor, datetime(2026, 10, 19, hora, 0), capacidade)
        self.calculo.adicionar_horario(h)
        return h
    
class TestCriterio1HorariosLivres(CenarioBase):
    def test_lista_apenas_horarios_livres_da_disciplina(self):
        # Preparar: 3 horários, 1 cancelado, 1 lotado, 1 livre
        cancelado = self.novo_horario(10)
        cancelado.cancelar()
        lotado = self.novo_horario(11)
        marcar_horario(self.aluno, lotado, "Limites")
        livre = self.novo_horario(12)

        # Executar
        livres = self.calculo.horarios_livres()

        # Conferir
        self.assertIn(livre, livres)
        self.assertNotIn(cancelado, livres)
        self.assertNotIn(lotado, livres)
        
    def test_horario_lotado_nao_aparece(self):
        # Preparar: horário individual já reservado (lotado)
        lotado = self.novo_horario(14)
        marcar_horario(self.aluno, lotado, "Limites")

        # Executar
        livres = self.calculo.horarios_livres()

        # Conferir
        self.assertNotIn(lotado, livres)

        
class TestCriterio2ReservaIndividualNaoAceitaMaisDeUma(CenarioBase):
    def test_individual_aceita_primeira_reserva(self):
        # Preparar: horário individual livre
        h = self.novo_horario(13)

        # Executar
        reserva = marcar_horario(self.aluno, h, "Limites")

        # Conferir: reserva criada e horário lotado
        self.assertIn(reserva, h.reservas)
        self.assertFalse(h.tem_vaga())

    def test_individual_recusa_segunda_reserva(self):
        # Preparar: horário individual já reservado por outro aluno
        h = self.novo_horario(14)
        outro = Aluno("a3", "Outro aluno")
        marcar_horario(outro, h, "Limites")

        # Executar e conferir: segunda reserva é recusada
        with self.assertRaises(ReservaInvalida):
            marcar_horario(self.aluno, h, "Derivadas")
        self.assertEqual(len(h.reservas), 1)


class TestCriterio3ReservaGrupoAceitaAteCapacidade(CenarioBase):
    def test_grupo_aceita_ate_capacidade(self):
        #horario em grupo com capacidade 3
        h = self.novo_horario(15, capacidade=3)
        outro = Aluno("a3", "Outro aluno")
        outro2 = Aluno("a4", "Outro aluno 2")
        
        #Executar: marcar 3 reservas
        reserva1 = marcar_horario(self.aluno, h, "Limites")
        reserva2 = marcar_horario(outro, h, "Limites")
        reserva3 = marcar_horario(outro2, h, "Limites")
        
        # Conferir: as 3 reservas entraram e o horário lotou
        self.assertEqual(len(h.reservas), 3)
        self.assertIn(reserva1, h.reservas)
        self.assertIn(reserva2, h.reservas)
        self.assertIn(reserva3, h.reservas)
        self.assertFalse(h.tem_vaga())
    
    def test_grupo_recusa_acima_da_capacidade(self):
        #horario em grupo com capacidade 2
        h = self.novo_horario(16, capacidade=2)
        outro = Aluno("a3", "Outro aluno")
        outro2 = Aluno("a4", "Outro aluno 2")
        
        #Executar: marcar 2 reservas
        marcar_horario(self.aluno, h, "Limites")
        marcar_horario(outro, h, "Limites")
        
        # Conferir: terceira reserva é recusada
        with self.assertRaises(ReservaInvalida):
            marcar_horario(outro2, h, "Limites")
        self.assertEqual(len(h.reservas), 2)

class TestCriterio6HorarioCancelado(CenarioBase):
    def test_horario_cancelado_nao_aparece(self):
        # Preparar: horário cancelado
        cancelado = self.novo_horario(15)
        cancelado.cancelar()

        # Executar
        livres = self.calculo.horarios_livres()

        # Conferir
        self.assertNotIn(cancelado, livres)
    
    def test_horario_cancelado_recusa_reserva(self):
        # Preparar: horário cancelado
        cancelado = self.novo_horario(16)
        cancelado.cancelar()

        # Executar e conferir
        with self.assertRaises(ReservaInvalida):
            marcar_horario(self.aluno, cancelado, "Limites")
        self.assertEqual(len(cancelado.reservas), 0)


if __name__ == "__main__":
    unittest.main()