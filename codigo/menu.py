import csv
from datetime import datetime, timedelta

from agendamento import ReservaInvalida, marcar_horario
from horario import Horario
from tela import desenhar_grade
from usuarios import Aluno, Monitor
import sys


def login(ra, senha, arq="usuarios.csv"):
    """Confere ra e senha no csv. Retorna a linha do usuario, ou None se nao encontrar."""
    with open(arq, 'r', encoding='utf-8') as file:
        for linha in csv.reader(file):
            if not linha:
                continue
            ra_csv, senha_csv = linha[0], linha[2]
            if ra_csv == ra and senha_csv == senha:
                return linha
    return None #caso nao encontrar ra/senha, ele mostra que o login falhou.


def fazer_login(arq="usuarios.csv"):
    while True:
        ra = input("Digite seu RA: ")
        senha = input("Digite sua senha: ")
        dados = login(ra, senha, arq)
        if dados is not None:
            return dados
        print("RA ou senha incorretos.\n")

def criar_usuario(dados, materias):
    """Monta Aluno ou Monitor a partir da linha do csv. Monitor recebe o objeto Materia."""
    ra, nome, _, tipo, nome_materia = dados
    if tipo == "monitor":
        materia = next(m for m in materias if m.nome == nome_materia)
        return Monitor(ra, nome, materia)
    return Aluno(ra, nome)

def menu(usuario, materias, salvar_estado=None):
    while True:
        print(f"\nOlá, {usuario.nome}!")
        print("1 - Ver horários livres de uma matéria")
        print("2 - Reservar horário")
        print("3 - Minhas reservas")
        if isinstance(usuario, Monitor):
            print("4 - Cadastrar horário de monitoria")
            print("5 - Fechar o programa")
        else:
            print("4 - Fechar o programa")
        print("0 - Trocar usuario")
        opcao = input("Escolha: ")

        if opcao == "1":
            ver_horarios_livres(materias)
        elif opcao == "2":
            reservar_horario(usuario, materias, salvar_estado)
        elif opcao == "3":
            mostrar_reservas(usuario)
        elif opcao == "4" and isinstance(usuario, Monitor):
            cadastrar_horario_monitoria(usuario, salvar_estado)
        elif (opcao == "4" and isinstance(usuario, Aluno)) or (opcao == "5" and isinstance(usuario, Monitor)):
            print("Saindo do programa...")
            sys.exit()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def ver_horarios_livres(materias):
    if not materias:
        print("Nenhuma disciplina disponível.")
        return

    print("\nDisciplinas:")
    for indice, materia in enumerate(materias, start=1):
        print(f"{indice} - {materia.nome}")

    materia = _escolher_opcao(materias, "Escolha a disciplina: ")
    horarios = sorted(materia.horarios_livres(), key=lambda horario: horario.data)
    if not horarios:
        print(f"Não há horários livres para {materia.nome}.")
        return

    print(f"\nHorários livres para {materia.nome}:")
    for horario in horarios:
        print(f"{horario.data:%d/%m/%Y %H:%M} ({horario.tipo})")


def mostrar_reservas(usuario):
    if not usuario.reservas:
        print("Você ainda não tem reservas.")
        return
    for reserva in usuario.reservas:
        print(reserva)


def cadastrar_horario_monitoria(monitor, salvar_estado=None):
    while True:
        try:
            data = datetime.strptime(
                input("Data e hora (DD/MM/AAAA HH:MM): "),
                "%d/%m/%Y %H:%M",
            )
            break
        except ValueError:
            print("Data inválida. Use o formato DD/MM/AAAA HH:MM.")

    tipo = _escolher_opcao(
        ["Individual", "Grupo"],
        "Tipo de horário (1 - Individual, 2 - Grupo): ",
    )
    capacidade = 1
    if tipo == "Grupo":
        while True:
            try:
                capacidade = int(input("Capacidade do grupo (mínimo 2): "))
            except ValueError:
                print("Digite um número válido.")
                continue
            if capacidade >= 2:
                break
            print("A capacidade do grupo deve ser pelo menos 2.")

    horario = Horario(monitor.materia, monitor, data, capacidade)
    monitor.materia.adicionar_horario(horario)
    if salvar_estado is not None:
        salvar_estado()
    print(
        f"Horário de monitoria cadastrado para "
        f"{data:%d/%m/%Y %H:%M} ({horario.tipo})."
    )


def reservar_horario(usuario, materias, salvar_estado=None):
    if not materias:
        print("Nenhuma disciplina disponível.")
        return

    print("\nDisciplinas:")
    for indice, materia in enumerate(materias, start=1):
        print(f"{indice} - {materia.nome}")

    materia = _escolher_opcao(materias, "Escolha a disciplina: ")
    horarios = sorted(materia.horarios_livres(), key=lambda horario: horario.data)
    if not horarios:
        print(f"Não há horários livres para {materia.nome}.")
        return

    horarios_por_semana = {}
    for indice, horario in enumerate(horarios, start=1):
        segunda = horario.data.date() - timedelta(days=horario.data.weekday())
        horarios_por_semana.setdefault(segunda, {})[horario.data] = str(indice)

    print("\nHorários livres (use o número marcado na grade):")
    for segunda, marcas in sorted(horarios_por_semana.items()):
        desenhar_grade(segunda, marcas)

    for indice, horario in enumerate(horarios, start=1):
        print(f"{indice} - {horario.data:%d/%m/%Y %H:%M} ({horario.tipo})")

    horario = _escolher_opcao(horarios, "Escolha o horário: ")

    print("\nTópicos:")
    for indice, topico in enumerate(materia.topicos, start=1):
        print(f"{indice} - {topico}")
    topico = _escolher_opcao(materia.topicos, "Escolha o tópico: ")

    try:
        reserva = marcar_horario(usuario, horario, topico)
    except ReservaInvalida as erro:
        print(f"Não foi possível marcar o horário: {erro}")
        return

    if salvar_estado is not None:
        salvar_estado()
    print(reserva)


def _escolher_opcao(opcoes, mensagem):
    while True:
        try:
            indice = int(input(mensagem))
        except ValueError:
            print("Digite o número de uma opção válida.")
            continue

        if 1 <= indice <= len(opcoes):
            return opcoes[indice - 1]
        print("Opção inválida.")