import csv
from datetime import timedelta

from agendamento import ReservaInvalida, marcar_horario
from tela import desenhar_grade
from usuarios import Aluno, Monitor

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

def menu(usuario, materias):
    while True:
        print(f"\nOlá, {usuario.nome}!")
        print("1 - Ver horários livres de uma matéria")
        print("2 - Reservar horário")
        print("3 - Minhas reservas")
        print("0 - Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            ...
        elif opcao == "2":
            reservar_horario(usuario, materias)
        elif opcao == "3":
            ...
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def reservar_horario(usuario, materias):
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
        marcar_horario(usuario, horario, topico)
    except ReservaInvalida as erro:
        print(f"Não foi possível marcar o horário: {erro}")
        return

    print("Horário marcado com sucesso.")


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