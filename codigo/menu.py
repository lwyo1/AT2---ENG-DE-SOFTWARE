import csv

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


def fazer_login():
    while True:
        ra = input("Digite seu RA: ")
        senha = input("Digite sua senha: ")
        dados = login(ra, senha)
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
            ...
        elif opcao == "3":
            ...
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
        