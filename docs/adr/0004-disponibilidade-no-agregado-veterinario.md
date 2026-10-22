# ADR 0004 — Disponibilidade gerenciada pelo agregado Veterinário

- **Autor:** Carlos Victor dos Santos Dantas (@VictorSantosD)
- **Status:** Aceita. Decisão implementada na Fase 1 e registrada retrospectivamente no checkpoint 1 da Fase 2.
- **Data do registro:** 21/10/2026

## Contexto

O sistema permite cadastrar um veterinário e adicionar suas disponibilidades semanais. Uma disponibilidade informa o dia da semana e o intervalo entre hora inicial e final. O mesmo veterinário não deve receber dois intervalos sobrepostos no mesmo dia quando a inclusão é feita pela operação do domínio.

Era necessário escolher onde manter essa regra: nos endpoints, no serviço, em operações independentes de disponibilidade ou na entidade que reúne os horários do profissional. A regra precisa continuar utilizável sem iniciar a API ou acessar o banco.

Na revisão `5ea0f32`, `Disponibilidade.__post_init__()` valida o valor de `DiaSemana` e exige início anterior ao fim. `Veterinario` mantém a coleção `disponibilidades`, e seu método `adicionar_disponibilidade()` rejeita sobreposição no mesmo dia. Intervalos adjacentes não satisfazem a condição de sobreposição, pois as comparações são estritas.

O caso de uso `adicionar_disponibilidade_veterinario()` recebe o repositório, recupera o veterinário, rejeita um identificador inexistente, cria a disponibilidade e delega a inclusão à raiz. O serviço não importa Flask ou SQLAlchemy. O endpoint converte o JSON para dia e horários, chama o serviço e controla a sessão e a transação.

O ORM mapeia as classes imperativamente, usando uma chave estrangeira da tabela de disponibilidades para veterinários e um relacionamento com `cascade="all, delete-orphan"`. Há repositórios SQLAlchemy e fake de Veterinário; não há repositório independente de Disponibilidade.

## Decisão

Manter a inclusão das disponibilidades por meio de `Veterinario.adicionar_disponibilidade()` e usar o repositório da raiz para recuperar e persistir o conjunto. A entidade Disponibilidade valida seu próprio intervalo; a raiz valida a relação entre os intervalos.

A camada de serviço coordena o caso de uso, enquanto a API converte dados e respostas HTTP e confirma ou desfaz a transação. Esta decisão registra a organização existente, sem introduzir uma refatoração no checkpoint 1.

## Alternativas consideradas

### Validar conflitos somente no endpoint Flask

Reduz a separação inicial e coloca a validação perto dos dados recebidos. Em contrapartida, outra entrada teria de repetir a regra, e a chamada direta ao serviço ou ao domínio poderia ignorá-la. Não foi escolhida porque a sobreposição é uma regra de negócio reutilizável.

### Validar conflitos somente na camada de serviço

Permite reutilização entre endpoints e testes sem HTTP. Entretanto, a entidade poderia aceitar um intervalo conflitante quando usada diretamente. Não foi escolhida porque a raiz já reúne as disponibilidades e dispõe dos dados necessários para a verificação.

### Tratar Disponibilidade como raiz independente

Oferece consultas e operações diretas sobre horários e pode evitar carregar toda a coleção em determinados fluxos. Acrescenta repositório e coordenação entre registros para assegurar a regra por veterinário. Não há necessidade atual demonstrada de um ciclo de vida independente que compense essa separação.

## Consequências

### Ganhos

- A regra de sobreposição fica localizada na operação do domínio e pode ser exercitada sem Flask ou banco de dados.
- O serviço pode usar `FakeVeterinarioRepository` ou `SqlAlchemyVeterinarioRepository` pelo comportamento `add/get`, sem conhecer a implementação concreta.
- A persistência do relacionamento é configurada no ORM, mantendo imports de infraestrutura fora do domínio.
- A operação é verificada em diferentes níveis: domínio, serviço com fake, repositório real e API com persistência.

### Custos e limites

- A verificação percorre os intervalos carregados: o custo de uma inclusão cresce com a quantidade de disponibilidades do veterinário.
- A tabela, o relacionamento, os repositórios, o serviço e o endpoint acrescentam código e indireção em comparação com uma solução de lógica concentrada nas rotas.
- A coleção é pública e Disponibilidade é mutável. Manipular a lista ou os intervalos diretamente pode contornar a operação que valida a regra.
- A verificação em memória não garante proteção entre requisições concorrentes. Duas sessões podem validar coleções desatualizadas; o esquema atual não demonstra uma restrição que proíba sobreposições entre linhas.
- O fake não reproduz todas as restrições do banco. Por exemplo, sua operação `add()` substitui uma entrada de mesmo identificador em um dicionário, enquanto a chave primária do banco pode rejeitar a duplicação.
- Os fakes estão em `adapters/repository.py`, que importa SQLAlchemy. Os testes de serviço dispensam banco, mas não dispensam a instalação desse pacote.
- Os três testes E2E de Veterinário cobrem sucesso; a presença de testes de erro no serviço não comprova os códigos HTTP de erro.

### Reavaliação

Se houver exigência de concorrência real na edição dos horários, será necessário avaliar controle transacional e testes com sessões independentes. Caso as consultas e a quantidade de disponibilidades cresçam, também será necessário avaliar a carga da coleção. Essas necessidades são riscos e caminhos de evolução, não funcionalidades já implementadas neste registro.

## Evidências do repositório

- `6a51da4` — casos de uso de Veterinário e testes: dois arquivos modificados.
- `627f5f6` — testes de veterinário inexistente e disponibilidade conflitante na camada de serviço.
- `e1430d3` — endpoints e testes E2E: três arquivos modificados.
- `tests/unit/test_veterinario.py`: cinco testes, incluindo intervalos conflitantes, contidos e em dias diferentes.
- `tests/unit/test_disponibilidade.py`: cinco testes de validação da disponibilidade.
- `tests/unit/test_services_veterinario.py`: seis testes com repositório fake.
- `tests/integration/test_repository_veterinario.py`: persiste o veterinário com disponibilidade, faz `expunge_all()` e recupera o relacionamento.
- `tests/e2e/test_veterinario_api.py`: três testes; após adicionar uma disponibilidade por POST, consulta o veterinário por GET e verifica a coleção persistida.

## Referências de código

- `src/sistema_veterinario/domain/model.py`
- `src/sistema_veterinario/service_layer/services.py`
- `src/sistema_veterinario/adapters/repository.py`
- `src/sistema_veterinario/adapters/orm.py`
- `src/sistema_veterinario/entrypoints/flask_app.py`
