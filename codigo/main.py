from materia import carregar_materias
from menu import fazer_login, criar_usuario, menu

def main():
    print("Bem vindo ao sistema de agendamento de monitorias!\n")
    print("Faça login no sistema para continuar.")
    dados = fazer_login()

    materias = carregar_materias("disciplinas.csv")
    usuario = criar_usuario(dados, materias)
    menu(usuario, materias)



if __name__ == "__main__":
    main()
