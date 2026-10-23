import unittest
from datetime import datetime

from agendamento import LIMITE_SEMANAL, marcar_horario, ReservaInvalida
from materia import Materia
from horario import Horario
from usuarios import Aluno, Monitor

class CenarioBase(unittest.TestCase):
    """Monta uma matéria e um monitor novos antes de cada teste."""
    def setUp(self):
        self.calculo = Materia("Cálculo 1", ["Limites", "Derivadas"])
        self.monitor = Monitor("a1", "Monitor", self.calculo)
        self.aluno = Aluno("a2", "Aluno")

    def novo_horario(self, hora, capacidade=1, dia=19):
        h = Horario(self.calculo, self.monitor, datetime(2026, 10, dia, hora, 0), capacidade)
        self.calculo.adicionar_horario(h)
        return h
    
    def reservar_tres_horarios_mesma_semana(self):
        """Marca 3 horários na mesma semana para o aluno."""
        h1 = self.novo_horario(10, dia=19)
        h2 = self.novo_horario(11, dia=20)
        h3 = self.novo_horario(12, dia=21)
        marcar_horario(self.aluno, h1, "Limites")
        marcar_horario(self.aluno, h2, "Limites")
        marcar_horario(self.aluno, h3, "Limites")
    
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

    def test_horario_de_outra_disciplina_nao_aparece(self):
        # Preparar: 1 horário livre de Cálculo e 1 horário livre de Física
        do_calculo = self.novo_horario(15)
        fisica = Materia("Física", ["Cinemática"])
        monitor_fisica = Monitor("a5", "Monitor de Física", fisica)
        da_fisica = Horario(fisica, monitor_fisica, datetime(2026, 10, 19, 15, 0))
        fisica.adicionar_horario(da_fisica)

        # Executar
        livres = self.calculo.horarios_livres()

        # Conferir
        self.assertIn(do_calculo, livres)
        self.assertNotIn(da_fisica, livres)


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
        marcar_horario(self.aluno, h, "Limites")
        marcar_horario(outro, h, "Limites")
        
        # Executar e Conferir: terceira reserva é recusada
        with self.assertRaises(ReservaInvalida):
            marcar_horario(outro2, h, "Limites")
        self.assertEqual(len(h.reservas), 2)
        
class TestCriterio4LimiteSemanal(CenarioBase):
    def test_terceira_reserva_na_semana_aceita(self):
        #Preparar e Executar: marcar 3 reservas na mesma semana
        self.reservar_tres_horarios_mesma_semana()
        
        #Conferir: as 3 reservas entraram
        self.assertEqual(len(self.aluno.reservas), 3)

    def test_quarta_reserva_na_semana_recusada(self):
        #Preparar 4 horarios na mesma semana
        self.reservar_tres_horarios_mesma_semana()
        h4 = self.novo_horario(13, dia=22)
        
        #Executar e Conferir: quarta reserva é recusada
        with self.assertRaises(ReservaInvalida):
            marcar_horario(self.aluno, h4, "Limites")
        self.assertEqual(len(self.aluno.reservas), 3)
    
    def test_limite_ignora_outra_semana(self):
        #Preparar 3 horarios na mesma semana e 1 na semana seguinte
        self.reservar_tres_horarios_mesma_semana()
        h4 = self.novo_horario(13, dia=26)  # próxima semana
        
        #Executar: marcar reserva na próxima semana
        marcar_horario(self.aluno, h4, "Limites")
        
        #Conferir: a reserva da próxima semana foi aceita
        self.assertEqual(len(self.aluno.reservas), 4)
        
    def test_limite_ignora_outra_disciplina(self):
        #Preparar 3 horarios na mesma semana e 1 de outra disciplina
        self.reservar_tres_horarios_mesma_semana()

        
        outra_disciplina = Materia("Física", ["Cinemática"])
        h4 = Horario(outra_disciplina, self.monitor, datetime(2026, 10, 22, 13, 0))
        outra_disciplina.adicionar_horario(h4)
        
        #Executar: marcar reserva na outra disciplina
        marcar_horario(self.aluno, h4, "Cinemática")
        
        #Conferir: a reserva da outra disciplina foi aceita
        self.assertEqual(len(self.aluno.reservas), 4)
        
class TestCriterio5ReservaExigeTopico(CenarioBase):
    def test_reserva_com_topico_valido(self):
        # Preparar: horário livre
        h = self.novo_horario(17)

        # Executar: marcar reserva com tópico válido
        reserva = marcar_horario(self.aluno, h, "Limites")

        # Conferir: reserva criada com o tópico correto
        self.assertIn(reserva, h.reservas)
        self.assertEqual(reserva.topico, "Limites")
    
    def test_reserva_sem_topico_recusada(self):
        # Preparar: horário livre
        h = self.novo_horario(18)

        # Executar e Conferir: marcar reserva sem tópico é recusada
        with self.assertRaises(ReservaInvalida):
            marcar_horario(self.aluno, h, None)
        self.assertEqual(len(h.reservas), 0)
        
    def test_topico_de_outra_disciplina_recusado(self):
        # Preparar: horário livre
        h = self.novo_horario(19)

        # Executar e Conferir: marcar reserva com tópico de outra disciplina é recusada
        with self.assertRaises(ReservaInvalida):
            marcar_horario(self.aluno, h, "Cinemática")
        self.assertEqual(len(h.reservas), 0)

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
        
class TestCriterioExtraMonitorNaoReservaPropriaMateria(CenarioBase):
    def test_monitor_reserva_outra_disciplina(self):
        # Preparar: horário de Física atendido pelo monitor de Física
        outra_disciplina = Materia("Física", ["Cinemática"])
        monitor_fisica = Monitor("a5", "Monitor de Física", outra_disciplina)
        h = Horario(outra_disciplina, monitor_fisica, datetime(2026, 10, 20, 10, 0))
        outra_disciplina.adicionar_horario(h)

        # Executar: monitor marca reserva em outra disciplina
        reserva = marcar_horario(self.monitor, h, "Cinemática")

        # Conferir: reserva criada com sucesso
        self.assertIn(reserva, h.reservas)
        self.assertEqual(reserva.topico, "Cinemática")
    
    def test_monitor_nao_reserva_propria_disciplina(self):
        # Preparar: horário da própria disciplina do monitor
        h = self.novo_horario(17)

        # Executar e Conferir: monitor não pode marcar reserva na própria disciplina
        with self.assertRaises(ReservaInvalida):
            marcar_horario(self.monitor, h, "Limites")
        self.assertEqual(len(h.reservas), 0)


if __name__ == "__main__":
    unittest.main()