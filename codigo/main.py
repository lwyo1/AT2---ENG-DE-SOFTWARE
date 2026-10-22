import csv
from datetime import datetime, time, timedelta
from pathlib import Path

from agendamento import marcar_horario
from horario import Horario
from materia import carregar_materias
from menu import fazer_login, criar_usuario, menu
from persistencia import carregar_horarios, salvar_horarios
from usuarios import Aluno

PASTA_CODIGO = Path(__file__).resolve().parent


def adicionar_horarios_demo(materias, arquivo_usuarios):
    materia = next(materia for materia in materias if materia.nome == "Cálculo 1")
    with open(arquivo_usuarios, "r", encoding="utf-8") as arquivo:
        dados_monitor = next(
            linha
            for linha in csv.reader(arquivo)
            if len(linha) >= 5 and linha[3] == "monitor" and linha[4] == materia.nome
        )
    monitor = criar_usuario(dados_monitor, materias)

    hoje = datetime.now().date()
    proxima_segunda = hoje + timedelta(days=7 - hoje.weekday())
    horarios_demo = [
        Horario(
            materia,
            monitor,
            datetime.combine(proxima_segunda, time(9, 0)),
        ),
        Horario(
            materia,
            monitor,
            datetime.combine(proxima_segunda + timedelta(days=1), time(10, 0)),
            capacidade=3,
        ),
        Horario(
            materia,
            monitor,
            datetime.combine(proxima_segunda + timedelta(days=2), time(11, 0)),
        ),
        Horario(
            materia,
            monitor,
            datetime.combine(proxima_segunda + timedelta(days=3), time(13, 0)),
        ),
    ]
    for horario in horarios_demo:
        materia.adicionar_horario(horario)

    horarios_demo[2].cancelar()
    aluno_demo = Aluno("demo", "Aluno da demonstração")
    marcar_horario(aluno_demo, horarios_demo[3], materia.topicos[0])


def main():
    print("Bem vindo ao sistema de agendamento de monitorias!\n")
    print("Faça login no sistema para continuar.")
    dados = fazer_login(PASTA_CODIGO / "usuarios.csv")

    arquivo_usuarios = PASTA_CODIGO / "usuarios.csv"
    arquivo_horarios = PASTA_CODIGO / "horarios.csv"
    arquivo_reservas = PASTA_CODIGO / "reservas.csv"
    materias = carregar_materias(PASTA_CODIGO / "disciplinas.csv")
    usuario = criar_usuario(dados, materias)
    horarios_carregados = carregar_horarios(
        materias,
        arquivo_horarios,
        arquivo_reservas,
        arquivo_usuarios,
        usuario,
    )
    if not horarios_carregados:
        adicionar_horarios_demo(materias, arquivo_usuarios)
    salvar_horarios(materias, arquivo_horarios, arquivo_reservas)

    menu(
        usuario,
        materias,
        salvar_estado=lambda: salvar_horarios(
            materias,
            arquivo_horarios,
            arquivo_reservas,
        ),
    )



if __name__ == "__main__":
    main()
