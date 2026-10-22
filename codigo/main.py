from pathlib import Path

from materia import carregar_materias
from menu import fazer_login, criar_usuario, menu

PASTA_CODIGO = Path(__file__).resolve().parent


def main():
    print("Bem vindo ao sistema de agendamento de monitorias!\n")
    print("Faça login no sistema para continuar.")
    dados = fazer_login(PASTA_CODIGO / "usuarios.csv")

    materias = carregar_materias(PASTA_CODIGO / "disciplinas.csv")
    usuario = criar_usuario(dados, materias)
    menu(usuario, materias)



if __name__ == "__main__":
    main()
