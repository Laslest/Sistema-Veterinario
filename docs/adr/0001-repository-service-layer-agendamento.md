# ADR 0001 — Separação entre caso de uso, domínio e persistência de Agendamento

- **Autor:** Davi Gesteira dos Anjos Paula (@Laslest)
- **Status:** Aceita. A decisão foi tomada na Fase 1 e está sendo registrada e reavaliada no Checkpoint 1 da Fase 2.
- **Data do registro:** 20/10/2026

## Contexto

O agregado Agendamento precisa validar que a data do atendimento é futura e controlar as transições de estado (`AGENDADO → CONFIRMADO → CONCLUIDO` e `AGENDADO → CANCELADO`). Essas operações são expostas pela API HTTP e os objetos são persistidos com SQLAlchemy. Se a validação e as transições ficassem em cada rota, a regra dependeria da interface HTTP e teria de ser duplicada caso surgissem outros pontos de entrada. Além disso, a proposta prevê regras futuras mais complexas para o agregado (duração dos atendimentos, deslocamento e conflitos de horário).

Na implementação atual:

- `domain/model.py` mantém as regras da entidade `Agendamento` (`__init__`, `confirmar()`, `cancelar()`, `concluir()`) e não importa SQLAlchemy;
- `service_layer/services.py` coordena os casos de uso `criar_agendamento()` e `cancelar_agendamento()`, recebendo o repositório por parâmetro;
- `entrypoints/flask_app.py` traduz as requisições HTTP, cria a sessão e o `SqlAlchemyAgendamentoRepository` e faz `commit`/`rollback`;
- `adapters/repository.py` define `AbstractRepository` e as implementações `SqlAlchemyAgendamentoRepository` e `FakeAgendamentoRepository`;
- `adapters/orm.py` mapeia a classe para a tabela `agendamentos` por mapeamento imperativo.

## Decisão

Manter as regras de negócio na entidade de domínio, coordenar as ações em casos de uso na Service Layer e acessar a persistência por meio do contrato de repositório (`add`/`get`). A API traduz o protocolo HTTP e delega às camadas apropriadas, sem reproduzir regras do agregado nos endpoints. O repositório falso é usado nos testes unitários dos casos de uso; o repositório SQLAlchemy é verificado pelos testes de integração e, junto com a API, pelos testes E2E.

As principais vantagens são testes unitários rápidos e isolados, regras sem duplicação e a substituição do banco pelo fake nos testes de serviço. O preço é mais módulos e indireção; além disso, `flask_app.py` ainda constrói o repositório concreto e inicializa o ORM, e a abstração e os fakes ficam em `adapters/repository.py`, junto das implementações reais.

## Alternativas consideradas

### 1. Toda a lógica nos endpoints Flask (Transaction Script)

Cada rota validaria a data, verificaria o estado, alteraria o agendamento e usaria a sessão diretamente.

- **Vantagens:** menos arquivos e fluxo inicial mais direto.
- **Desvantagens:** mistura HTTP, regra de negócio e persistência; tende a duplicar regras e torna o teste da regra dependente da API e do banco.
- **Por que não:** as transições de estado pertencem ao domínio e precisam ter o mesmo comportamento independentemente de como a operação é chamada.

### 2. Active Record (por exemplo, Flask-SQLAlchemy com `db.Model`)

A entidade herdaria do modelo do ORM, com colunas e regras na mesma classe, e as rotas consultariam e salvariam por meio dela.

- **Vantagens:** menos indireção e implementação direta para CRUD.
- **Desvantagens:** acopla o modelo de domínio ao ORM; instanciar a entidade passa a exigir o ORM configurado, e testar regras tende a exigir sessão ou banco.
- **Por que não:** a separação permite testar as regras de Agendamento sem iniciar o SQLAlchemy.

## Consequências

**Positivas**

- As regras de data e estado ficam apenas em `Agendamento`; nenhuma rota as reimplementa.
- Os casos de uso são testados com `FakeAgendamentoRepository`. Esses testes continuam passando mesmo quando a configuração do ORM está quebrada: com SQLAlchemy 2.0.55, os 85 testes unitários passam, enquanto os de integração e E2E falham (ver `docs/arquitetura.md`, seção 6).
- `services.py` não importa nada de `adapters`, apenas `domain.model`.

**Negativas**

- Cada agregado precisa de entidade, tabela, mapeamento, dois repositórios, caso de uso e rota; o commit `59789a8` criou a API com 138 linhas, cerca de 100 delas nos dois endpoints, contra 35 linhas dos casos de uso em `b8749b6`.
- O fake não reproduz restrições do banco: aceita um `id_agendamento` repetido, enquanto o SQLAlchemy lança `IntegrityError`. Os testes de integração continuam indispensáveis.
- Como a tabela `agendamentos` não tem chaves estrangeiras e o caso de uso não verifica referências, é possível criar um agendamento para paciente, veterinário ou unidade inexistentes.
- O endpoint de cancelamento escolhe entre 404 e 400 comparando o texto da exceção lançada pelo caso de uso; mudar a mensagem altera o contrato HTTP sem que algum teste falhe, pois os testes E2E de agendamento cobrem apenas os casos de sucesso.

**Evolução prevista**

- Substituir a comparação por texto por uma exceção específica (por exemplo, `AgendamentoNaoEncontrado`) e acrescentar testes E2E de 400, 404 e 409.
- Validar as referências de paciente, veterinário e unidade ao criar um agendamento.
- Tornar explícita a composição das dependências e rever a posição de `AbstractRepository` e dos fakes, reforçando a direção das dependências.

## Evidências relacionadas

- `b8749b6` — `feat: adiciona casos de uso de agendamento`: 2 arquivos, 91 linhas (caso de uso e testes unitários).
- `59789a8` — `feat: adiciona API de agendamento`: 138 linhas em `entrypoints/flask_app.py`.
- `38f857c` — `test: adiciona testes e2e de agendamento`: 69 linhas, criação e cancelamento com sucesso via HTTP.
- `4e4c080` — `fix: evita mapeamento ORM duplicado`: protege os mapeamentos para que `start_mappers()` possa ser chamado mais de uma vez.
- `9a6c4de` — `test: adiciona fake repository de agendamento`.
