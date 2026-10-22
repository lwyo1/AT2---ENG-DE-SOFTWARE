# Projeto Inicial

**História escolhida (prioridade Alta):** 1. Marcar horário
Como aluno, eu quero selecionar uma das disciplinas e marcar um horário de monitoria para tirar minhas dúvidas sem necessidade de entrar em contato por mensagem.

## Classes e responsabilidades

Todo o código fica na pasta `codigo/`, em Python, sem interface gráfica. Os dados ficam em memória (listas dentro dos objetos), sem banco de dados.

- **Materia** (`materia.py`): guarda o nome da disciplina, a lista de tópicos do conteúdo a partir de um leitor de CSV com esses dados e os horários cadastrados pelo monitor. Oferece `horarios_livres()`, que devolve só os horários da disciplina que não estão cancelados nem lotados.
- **Horario** (`horario.py`): representa um atendimento de 30 minutos de um monitor em uma disciplina. Guarda data e hora de início, tipo (individual ou grupo), capacidade (1 no individual, definida pelo monitor no grupo), se está cancelado e as reservas feitas nele. Responde se ainda tem vaga (`tem_vaga()`) e permite `cancelar()`.
- **Reserva** (`reserva.py`): liga um estudante a um horário e ao tópico escolhido.
- **Estudante** (`usuario.py`, classe abstrata): guarda RA, nome e as reservas da pessoa. Conta quantas reservas ela tem em uma disciplina numa semana. Define o método abstrato `pode_reservar(horario)`.
- **Aluno** (filha de Estudante): `pode_reservar` aceita qualquer disciplina.
- **Monitor** (filha de Estudante): guarda a disciplina que monitora e cadastra seus horários. Como também é aluno, pode reservar horários de outras disciplinas, mas `pode_reservar` recusa horários da própria disciplina.
- **Agendamento** (`agendamento.py`): função `marcar_horario(estudante, horario, topico)`, que verifica todas as regras na ordem e cria a reserva. Quando alguma regra falha, lança a exceção `ReservaInvalida` com o motivo. O limite semanal fica na constante `LIMITE_SEMANAL = 3`, fácil de mudar caso o cliente decida outro valor.

## Testes de aceitação

Arquivo `codigo/test_marcar_horario.py`, com `unittest`. Cada teste monta seus próprios objetos, sem depender de entrada digitada. Comando: `python -m unittest discover codigo`.

| Critério de aceitação | Testes | Cenário |
|---|---|---|
| 1. Só aparecem horários livres da disciplina escolhida | `test_lista_apenas_horarios_livres_da_disciplina` / `test_horario_lotado_nao_aparece` | sucesso / falha |
| 2. Horário individual reservado não aceita outra reserva | `test_individual_aceita_primeira_reserva` / `test_individual_recusa_segunda_reserva` | sucesso / falha |
| 3. Horário de grupo aceita reservas até a capacidade | `test_grupo_aceita_ate_capacidade` / `test_grupo_recusa_acima_da_capacidade` | sucesso / falha |
| 4. No máximo 3 reservas por semana na mesma disciplina | `test_terceira_reserva_na_semana_aceita` / `test_quarta_reserva_na_semana_recusada` / `test_limite_ignora_outra_semana_e_outra_disciplina` | sucesso / falha / sucesso |
| 5. A reserva exige um tópico do conteúdo | `test_reserva_com_topico_valido` / `test_reserva_sem_topico_recusada` / `test_topico_de_outra_disciplina_recusado` | sucesso / falha / falha |
| 6. Horário cancelado não pode ser reservado | `test_horario_cancelado_nao_aparece` / `test_horario_cancelado_recusa_reserva` | falha / falha |

Também teremos `test_monitor_reserva_outra_disciplina` e `test_monitor_nao_reserva_propria_disciplina`, para a regra do Monitor como estudante.
