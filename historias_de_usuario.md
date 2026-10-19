# Histórias de Usuário

Sistema de Agendamento de Monitorias. Histórias em ordem de prioridade.

---

## 1. Marcar horário

Como **aluno**, eu quero selecionar uma das disciplinas e marcar um horário de monitoria para tirar minhas dúvidas sem necessidade de entrar em contato por mensagem.

**Critérios de aceitação:**

- Só aparecem horários livres da disciplina escolhida.
- Em horário individual, depois de reservado ele não aceita outra reserva.
- Em horário de grupo, aceita reservas até a capacidade definida pelo monitor.
- O aluno pode ter no máximo 3 reservas por semana na mesma disciplina.
- A reserva exige a seleção de um dos tópicos do conteúdo.
- Horário cancelado não pode ser reservado.

**Prioridade:** Alta

**Justificativa:** É o problema central, a superlotação de horários.

**Trecho do e-mail:** "um monitor de Cálculo tinha três alunos marcados no mesmo horário"

---

## 2. Cadastrar disponibilidade

Como **monitor**, eu quero cadastrar meus horários de atendimento para que os alunos possam reservá-los.

**Critérios de aceitação:**

- Cada horário tem duração de 30 minutos.
- O monitor define se o horário é individual ou em grupo e, se for em grupo, a capacidade.
- Não é possível cadastrar dois horários sobrepostos para o mesmo monitor.

**Prioridade:** Alta

**Justificativa:** Sem horários cadastrados, a reserva não existe.

**Trecho do e-mail:** "cada monitor informa os horários em que pode atender"

---

## 3. Cancelar horário e avisar alunos

Como **monitor**, eu quero cancelar um horário para que os alunos saibam antes de ir até a sala.

**Critérios de aceitação:**

- O horário cancelado deixa de aparecer como livre.
- Todos os alunos com reserva naquele horário recebem um aviso.
- As reservas do horário cancelado não contam no limite semanal do aluno.

**Prioridade:** Média

**Justificativa:** Resolve uma reclamação direta dos alunos.

**Trecho do e-mail:** "só descobrem o cancelamento quando chegam na sala"

---

## 4. Relatório mensal de horas

Como **coordenação**, eu quero gerar um relatório mensal com as horas atendidas por monitor para calcular a bolsa.

**Critérios de aceitação:**

- Só contam atendimentos em que o monitor registrou o comparecimento.
- Cada atendimento conta 30 minutos (atendimento em grupo conta uma vez só).
- Apenas usuários com perfil de coordenação acessam o relatório.

**Prioridade:** Média

**Justificativa:** Importante para o pagamento, mas depende da reserva funcionando.

**Trecho do e-mail:** "relatório mensal com as horas atendidas por cada monitor"

---

## 5. Ver tópicos com mais dúvidas

Como **professor**, eu quero ver quais tópicos da minha disciplina tiveram mais reservas para reforçar esses conteúdos em aula.

**Critérios de aceitação:**

- O professor vê apenas as disciplinas dele.
- Os tópicos aparecem ordenados pela quantidade de reservas.
- O relatório não mostra dados de bolsa nem de horas dos monitores.

**Prioridade:** Baixa

**Justificativa:** Traz benefício, mas não é urgente para o funcionamento.

**Trecho do e-mail:** "gostariam de saber quais conteúdos geram mais dúvidas"
