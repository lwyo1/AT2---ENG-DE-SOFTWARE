# Sistema de Agendamento de Monitorias

Atividade Avaliativa A2 de Engenharia de Software.
Alunos: João Victor Lourenço da Silva e Luiz Bonfá dos Santos.

História implementada: **1. Marcar horário** (ver `historias_de_usuario.md`).

## Requisitos

- Python 3.14
- Nenhuma biblioteca externa (só a biblioteca padrão)

## Como executar o programa

Arquivo principal: `codigo/main.py`.

Na pasta raiz do projeto:

```
python codigo/main.py
```

Ou de dentro da pasta `codigo`:

```
cd codigo
python main.py
```

Logins de exemplo:

| Tipo | RA | Senha |
|---|---|---|
| Aluno | 2669552 | iwhbhg |
| Monitor de Cálculo 1 | 2655120 | mn42rk |

No menu, `0` troca de usuário. Para fechar o programa, use a opção "Fechar o programa" (4 para aluno, 5 para monitor).

Na primeira execução são criados horários de demonstração em Cálculo 1, salvos em `codigo/horarios.csv` e `codigo/reservas.csv`. Para voltar ao estado inicial, apague esses dois arquivos.

## Como executar os testes

Na pasta raiz do projeto:

```
python -m unittest discover codigo
```

Ou de dentro da pasta `codigo`:

```
cd codigo
python -m unittest -v
```

## Plano e execução

| Etapa | Responsável | Planejado | Realizado |
|---|---|---|---|
| Histórias de usuário | Luiz | até 17/10 | 19/10, Luiz |
| Projeto inicial | João | até 18/10 | 19/10, commit do Luiz |
| Implementação e testes | Luiz e João | até 21/10 | 20 e 21/10. Luiz: classes do domínio, `agendamento.py`, 18 testes. João: login, menu, horários de exemplo, cadastro, persistência |
| Documentação | Luiz e João | 22/10 | 22/10 |
| Autoavaliação | Luiz e João | 22/10 | 22/10 |

## Atrasos e mudanças em relação ao projeto inicial

- A princípio, não foi possível realizar nenhuma etapa nos dois primeiros dias (17 e 18/10) por situações inesperadas que ocorreram no fim de semana. No dia 19, foram feitas as etapas pendentes referentes às histórias de usuário e ao projeto inicial.
- Foram feitos outros recursos no código que não estavam no projeto inicial, como o menu, a tela da agenda, a persistência e o login, que facilitam o funcionamento e a demonstração do sistema.
- O sistema de persistência de dados em arquivo CSV não foi planejado. A princípio, o sistema realizaria todos os processos em memória, e os dados seriam perdidos ao fechar o programa. Para trazer mais consistência, decidimos salvar essas alterações em arquivo.
- O cadastro de horários não ficou na classe `Monitor`; ele virou uma opção do menu, apenas para que o sistema possa ser usado. O cadastro completo fica para a história 2.
- Foi adicionado um terceiro teste no critério 1, `test_horario_de_outra_disciplina_nao_aparece`, que verifica que um horário livre de outra disciplina não aparece na lista da disciplina escolhida. Os testes previstos no projeto inicial não cobriam a parte "da disciplina escolhida" do critério.
- O teste `test_limite_ignora_outra_semana_e_outra_disciplina` (critério 4) foi dividido em `test_limite_ignora_outra_semana` e `test_limite_ignora_outra_disciplina`, para que, se um falhar, fique claro qual regra está com erro.
- No planejamento, seria feito um sistema de notificação e confirmação para o monitor assim que um aluno realizasse um agendamento. Porém, para economizar tempo e simplificar a implementação inicial, o agendamento é realizado sem a necessidade de confirmação.
- A primeira implementação aborda a história 1 com alguns recursos de outras histórias; por isso, o usuário Professor e o sistema de relatórios ficaram de fora.
- No e-mail, é sugerido um limite de 2 reservas semanais por disciplina, porém decidimos permitir 3, já que o e-mail não exigia esse número e deixou a escolha em aberto. O valor fica na constante `LIMITE_SEMANAL`, fácil de alterar.

## Documentação

O projeto inicial, o relatório de execução e a documentação técnica estão no PDF da entrega, neste repositório.
