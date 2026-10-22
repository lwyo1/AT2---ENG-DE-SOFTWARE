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

## Documentação

O projeto inicial, o relatório de execução e a documentação técnica estão no PDF da entrega, neste repositório.
