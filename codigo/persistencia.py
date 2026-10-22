import csv
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from horario import Horario
from reserva import Reserva
from usuarios import Aluno, Monitor


CABECALHO_HORARIOS = [
    "id",
    "monitor_ra",
    "materia",
    "data",
    "hora",
    "tipo",
    "capacidade",
    "status",
]
CABECALHO_RESERVAS = ["horario_id", "aluno_ra", "aluno_nome", "topico"]


def carregar_horarios(
    materias,
    arquivo_horarios,
    arquivo_reservas,
    arquivo_usuarios,
    usuario_ativo,
):
    arquivo_horarios = Path(arquivo_horarios)
    if not arquivo_horarios.exists():
        return False

    materias_por_nome = {materia.nome: materia for materia in materias}
    usuarios_por_ra = {usuario_ativo.ra: usuario_ativo}
    with open(arquivo_usuarios, "r", encoding="utf-8", newline="") as arquivo:
        for dados in csv.reader(arquivo):
            if dados and dados[0] not in usuarios_por_ra:
                usuarios_por_ra[dados[0]] = _criar_usuario(
                    dados,
                    materias_por_nome,
                )

    horarios_por_id = {}
    with open(arquivo_horarios, "r", encoding="utf-8", newline="") as arquivo:
        for dados in csv.DictReader(arquivo):
            materia = materias_por_nome[dados["materia"]]
            horario = Horario(
                materia,
                usuarios_por_ra[dados["monitor_ra"]],
                datetime.strptime(
                    f'{dados["data"]} {dados["hora"]}',
                    "%d/%m/%Y %H:%M",
                ),
                int(dados["capacidade"]),
            )
            horario.id = dados["id"]
            if dados["status"] == "cancelado":
                horario.cancelar()
            materia.adicionar_horario(horario)
            horarios_por_id[horario.id] = horario

    arquivo_reservas = Path(arquivo_reservas)
    if arquivo_reservas.exists():
        with open(arquivo_reservas, "r", encoding="utf-8", newline="") as arquivo:
            for dados in csv.DictReader(arquivo):
                aluno = usuarios_por_ra.get(dados["aluno_ra"])
                if aluno is None:
                    aluno = Aluno(dados["aluno_ra"], dados["aluno_nome"])
                    usuarios_por_ra[aluno.ra] = aluno
                horario = horarios_por_id[dados["horario_id"]]
                reserva = Reserva(aluno, horario, dados["topico"])
                horario.adicionar_reserva(reserva)
                aluno.adicionar_reserva(reserva)

    return True


def salvar_horarios(materias, arquivo_horarios, arquivo_reservas):
    linhas_horarios = []
    linhas_reservas = []
    for materia in materias:
        for horario in materia.horarios:
            if not hasattr(horario, "id"):
                horario.id = uuid4().hex
            status = (
                "cancelado"
                if horario.cancelado
                else "lotado"
                if not horario.tem_vaga()
                else "livre"
            )
            linhas_horarios.append(
                {
                    "id": horario.id,
                    "monitor_ra": horario.monitor.ra,
                    "materia": materia.nome,
                    "data": horario.data.strftime("%d/%m/%Y"),
                    "hora": horario.data.strftime("%H:%M"),
                    "tipo": horario.tipo,
                    "capacidade": horario.capacidade,
                    "status": status,
                }
            )
            linhas_reservas.extend(
                {
                    "horario_id": horario.id,
                    "aluno_ra": reserva.aluno.ra,
                    "aluno_nome": reserva.aluno.nome,
                    "topico": reserva.topico,
                }
                for reserva in horario.reservas
            )

    _salvar_csv(arquivo_horarios, CABECALHO_HORARIOS, linhas_horarios)
    _salvar_csv(arquivo_reservas, CABECALHO_RESERVAS, linhas_reservas)


def _salvar_csv(caminho, cabecalho, linhas):
    caminho = Path(caminho)
    temporario = caminho.with_suffix(caminho.suffix + ".tmp")
    with open(temporario, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=cabecalho)
        escritor.writeheader()
        escritor.writerows(linhas)
    temporario.replace(caminho)


def _criar_usuario(dados, materias_por_nome):
    ra, nome, _, tipo, nome_materia = dados
    if tipo == "monitor":
        return Monitor(ra, nome, materias_por_nome[nome_materia])
    return Aluno(ra, nome)
