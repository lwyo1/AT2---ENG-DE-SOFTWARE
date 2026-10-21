from datetime import datetime, time, timedelta
from horario import DURACAO

INICIO = time(8, 0)
FIM = time(22, 0)
DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex"]

def horarios_do_dia(dia):
    atual = datetime.combine(dia, INICIO)
    fim = datetime.combine(dia, FIM)
    while atual < fim:
        yield atual
        atual += DURACAO

def desenhar_grade(segunda, marcas):
    """marcas: {datetime: texto}. Horário sem marca aparece como '.'"""
    dias = [segunda + timedelta(days=i) for i in range(5)]
    print("Hora  | " + " | ".join(f"{DIAS[i]} {d.day:02}" for i, d in enumerate(dias)))
    print("-" * 50)
    for h in horarios_do_dia(segunda):
        linha = []
        for d in dias:
            momento = datetime.combine(d, h.time())
            linha.append(f"{marcas.get(momento, '.'):^6}")
        print(f"{h:%H:%M} | " + " | ".join(linha))