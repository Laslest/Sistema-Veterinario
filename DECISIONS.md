## Fase 1 - Checkpoint 1

### Davi Gesteira dos Anjos Paula

#### O que implementei

Neste checkpoint fiquei responsável pelo agregado de Agendamento.

Implementei a entidade `Agendamento` no arquivo:

`src/sistema_veterinario/domain/model.py`

A entidade possui os dados básicos necessários para representar um agendamento:

- identificador do agendamento;
- identificador do cliente;
- identificador do paciente;
- identificador do veterinário;
- data e hora;
- status.

Também implementei algumas regras de negócio relacionadas ao estado do agendamento.

Um agendamento deve ser criado para uma data futura. Caso seja informada uma data ou horário anterior ao momento atual, é lançado um `ValueError`.

O status inicial de um novo agendamento é `AGENDADO`.

Foram adicionadas as operações:

- `confirmar()`: altera o status de `AGENDADO` para `CONFIRMADO`;
- `cancelar()`: permite cancelar um agendamento que ainda está no status `AGENDADO`;
- `concluir()`: permite concluir somente um agendamento que esteja no status `CONFIRMADO`.

Também criei testes unitários no arquivo:

`tests/unit/test_agendamento.py`

Os testes implementados verificam:

- que um agendamento criado para uma data futura inicia com o status `AGENDADO`;
- que não é possível criar um agendamento com uma data passada.

#### Commits

Commits realizados neste checkpoint:

- `09a81c9` - `feat: cria entidade inicial de agendamento`
- `5871935` - `feat: adiciona regras de status e validação de data do agendamento`
- `62faea7` - `test: adiciona testes iniciais de agendamento`

#### Decisões de projeto

Decidi concentrar as mudanças de estado do agendamento dentro da própria entidade, por meio dos métodos confirmar(), cancelar() e concluir().

A intenção é manter as regras e invariantes do agregado centralizadas no domínio, evitando que outras partes do sistema alterem diretamente o estado de um agendamento sem respeitar as transições permitidas.

Também defini que todo novo agendamento começa no estado AGENDADO. A partir desse estado, as mudanças posteriores devem ocorrer exclusivamente através das operações disponibilizadas pela própria entidade.

### Carlos Victor dos Santos Dantas

#### O que implementei

Neste checkpoint fiquei responsável pelo agregado de Veterinário.

Implementei a entidade `Veterinario` e o objeto de valor `Disponibilidade` no arquivo:

`src/sistema_veterinario/domain/model.py`

A entidade `Veterinario` possui os dados básicos necessários para representar um veterinário:

- identificador do veterinário;
- nome;
- CRMV;
- lista de disponibilidades.

Também implementei o objeto de valor `Disponibilidade`, responsável por representar um intervalo de horário em que o veterinário está disponível.

Foram adicionadas regras de negócio relacionadas às disponibilidades do veterinário.

Uma disponibilidade deve possuir um horário de início anterior ao horário de término. Caso os horários sejam iguais ou o início seja posterior ao término, é lançado um `ValueError`.

Também foi implementada uma regra para impedir que um veterinário possua disponibilidades com horários conflitantes. Disponibilidades que possuem sobreposição de horários não podem ser adicionadas ao mesmo veterinário.

Disponibilidades consecutivas são permitidas quando o horário final de uma coincide com o horário inicial de outra.

Também criei testes unitários nos arquivos:

`tests/unit/test_disponibilidade.py`

`tests/unit/test_veterinario.py`

Os testes implementados verificam:

- criação de uma disponibilidade válida;
- rejeição de uma disponibilidade com horário inicial posterior ao final;
- rejeição de uma disponibilidade com horários inicial e final iguais;
- rejeição de disponibilidades conflitantes;
- aceitação de disponibilidades consecutivas;
- armazenamento correto das disponibilidades do veterinário.

#### Commits

Commits realizados neste checkpoint:

- `50bd859` - `feat: adiciona entidade Veterinario e objeto Disponibilidade`
- `a330948` - `feat: adiciona regras de disponibilidade do veterinario`
- `c9c67d5` - `test: adiciona testes de disponibilidade e veterinario`

#### Decisões de projeto

Decidi representar `Disponibilidade` como um objeto de valor imutável, contendo apenas o horário de início e o horário de término. Dessa forma, a própria disponibilidade é responsável por garantir que seu intervalo seja válido.

Também decidi concentrar na entidade `Veterinario` a regra que impede a criação de disponibilidades conflitantes. Dessa maneira, o próprio agregado mantém a consistência dos horários cadastrados para o veterinário.

As disponibilidades consecutivas são permitidas, pois o término de uma disponibilidade pode coincidir com o início de outra sem que exista sobreposição entre os intervalos.

### Cauã Raphael Santos de Paula

#### O que implementei

Neste checkpoint fiquei responsável pelo agregado de **Unidade / Local de Atendimento**.

Implementei a entidade `Unidade` e o objeto de valor `Endereco` no arquivo:

`src/sistema_veterinario/domain/model.py`

O objeto de valor `Endereco` possui os seguintes atributos:

* `rua`
* `numero`
* `bairro`
* `cidade`
* `estado`
* `cep`

Também implementei as validações:

* A rua é obrigatória.
* A cidade é obrigatória.
* O estado é obrigatório.
* O CEP deve possuir exatamente 8 caracteres numéricos.
* O objeto `Endereco` foi implementado como imutável utilizando `@dataclass(frozen=True)`.

A entidade `Unidade` possui os seguintes atributos:

* `id_unidade`
* `nome`
* `endereco`
* `atende_domicilio`

Também implementei as seguintes regras:

* O nome da unidade é obrigatório.
* Caso a unidade não realize atendimento a domicílio, ela deve possuir um endereço.
* A igualdade entre duas unidades é definida pelo `id_unidade`.
* O `id_unidade` também é utilizado para gerar o `hash` da entidade.

Também criei testes unitários no arquivo tanto para unidade quanto para endereco:

`tests/unit/test_unidade_endereco.py`

Os testes implementados verificam:

* Criação de um endereço válido.
* Erro ao criar um endereço sem rua.
* Erro ao criar um endereço com CEP inválido.
* Erro ao criar uma unidade com nome vazio.
* Erro ao criar uma unidade física sem endereço.
* Criação de uma unidade física com endereço válido.
* Duas unidades com o mesmo ID são consideradas iguais.

#### Commits

Commits realizados neste checkpoint:

* `5224767` - `feat: adiciona objeto de valor Endereco`
* `3b833f7` - `feat: adiciona entidade Unidade`
* `b400d4e` - `test: adiciona testes de endereco e unidade`

#### Decisões de projeto

O `Endereco` foi implementado como um **Objeto de Valor**, pois não possui uma identidade própria e é definido pelos seus atributos. Por isso, também foi utilizado `@dataclass(frozen=True)` para manter o endereço imutável.

A `Unidade` foi implementada como uma **Entidade**, pois possui um identificador próprio (`id_unidade`). Dessa forma, duas unidades são consideradas iguais quando possuem o mesmo ID, mesmo que seus outros atributos sejam diferentes.

O endereço é obrigatório somente para unidades que **não realizam atendimento a domicílio**, pois uma unidade física precisa informar sua localização, enquanto uma unidade que atende exclusivamente em domicílio pode não possuir um endereço físico.

A validação do CEP foi definida para aceitar somente valores com **8 dígitos numéricos**, seguindo o formato básico do CEP brasileiro.

### David Pereira Ramos

#### O que implementei

Neste checkpoint fiquei responsável pelo agregado de Cliente / Paciente.

Implementei as entidades Cliente, Paciente, Especie e Raca, além dos objetos de valor CPF e Telefone, no arquivo:

`src/sistema_veterinario/domain/model.py`

A entidade `Cliente` foi definida como a raiz do agregado e possui os seguintes atributos:

- `id_cliente`
- `nome`
- `cpf`
- `telefone`
- `endereco`
- coleção de `pacientes`

A entidade `Paciente` possui:

- `id_paciente`
- `nome`
- `data_nascimento`
- `raca_id`

Também implementei `Especie` e `Raca`, ambas com identificador próprio. A `Raca` possui também o identificador da espécie à qual pertence.

O objeto de valor `CPF` possui validação de quantidade de dígitos, rejeição de números com todos os dígitos iguais e validação dos dígitos verificadores.

O objeto de valor `Telefone` valida números com 10 ou 11 dígitos, DDD entre 11 e 99 e, para celulares, o dígito `9` na posição correspondente.

Também implementei regras de validação para `Cliente`, `Paciente`, `Especie` e `Raca`, como identificadores maiores que zero e nomes obrigatórios. A data de nascimento do paciente não pode estar no futuro.

No `Cliente`, foram adicionadas as operações:

- `adicionar_paciente()`: adiciona um paciente à coleção do cliente e impede pacientes duplicados pelo `id_paciente`;
- `buscar_paciente()`: busca um paciente pelo identificador e gera erro quando ele não pertence ao cliente;
- `remover_paciente()`: remove um paciente pelo identificador e gera erro quando ele não pertence ao cliente.

Também criei testes unitários nos arquivos:

- `tests/unit/test_cliente.py`
- `tests/unit/test_cpf.py`
- `tests/unit/test_especie.py`
- `tests/unit/test_paciente.py`
- `tests/unit/test_raca.py`
- `tests/unit/test_telefone.py`

Os testes implementados verificam:

- criação válida de `Cliente`, `Paciente`, `Especie` e `Raca`;
- validações dos objetos de valor `CPF` e `Telefone`;
- validações dos identificadores e nomes das entidades;
- validação da data de nascimento do paciente;
- igualdade das entidades pelo identificador;
- adição de pacientes ao cliente;
- rejeição de pacientes duplicados;
- busca de pacientes existentes e tratamento de pacientes inexistentes;
- remoção de pacientes existentes e tratamento de pacientes inexistentes.

#### Commits

Commits realizados neste checkpoint:

- `721c630` - `feat: adicionado os Value Objects (Objetos de Valor) CPF e Email referente ao agregado Cliente / Paciente`
- `9eb3e78` - `adicionado o Value Object Telefone referente ao agregado Cliente / Paciente`
- `275eca8` - `refactor: Reorganização na posição do código referente ao agregado Cliente / Paciente`
- `4b8674c` - `feat: remoção do Objeto de Valor Email e adicionado as Entidades auxiliares Espécie e Raça para o Agregado Cliente / Paciente`
- `ca43c8a` - `feat: adicionado a entidade Paciente a respeito do Agregado Cliente / Paciente`
- `29e37f3` - `feat: adiciona a entidade Cliente, Raiz do Agregado Cliente / Paciente`
- `e93b1f1` - `test: adiciona testes para CPF a respeito do Agregado Cliente / Paciente`
- `a57f687` - `test: adiciona testes para Telefone a respeito do Agregado Cliente / Paciente`
- `eb3a323` - `test: adiciona testes para Especie a respeito do Agregado Cliente / Paciente`
- `1747253` - `test: adiciona testes para Raca a respeito do Agregado Cliente / Paciente`
- `3a386af` - `test: adiciona testes para Paciente do Agregado Cliente / Paciente`
- `e4de5de` - `test: adiciona testes para Cliente, Raiz do Agregado Cliente / Paciente`

#### Decisões de projeto

Decidi representar `Cliente` como a **raiz do agregado Cliente / Paciente**, mantendo sob seu controle a associação com os pacientes. Por isso, as operações de adicionar, buscar e remover pacientes ficam na própria entidade `Cliente`, permitindo que o agregado mantenha a regra de não duplicidade dos pacientes associados.

Decidi representar `CPF` e `Telefone` como **Objetos de Valor**, pois não possuem identidade própria e são definidos pelos seus respectivos valores. Ambos foram implementados como imutáveis utilizando `@dataclass(frozen=True)`.

Decidi representar `Paciente`, `Especie` e `Raca` como **Entidades**, pois possuem identificadores próprios. `Especie` e `Raca` são entidades de domínio relacionadas ao agregado Cliente / Paciente e utilizadas na caracterização dos pacientes. A `Raca` possui uma referência à `Especie`, enquanto o `Paciente` mantém a referência à `Raca` por meio de seu identificador.

Inicialmente, implementei `Email` como um **Objeto de Valor**, porém, após revisar o modelo conceitual, decidi removê-lo da implementação por não fazer parte dos atributos definidos para o agregado Cliente / Paciente.

## Fase 1 - Checkpoint 2

### Carlos Victor dos Santos Dantas

#### O que implementei

Neste checkpoint continuei responsável pelo agregado de Veterinário, trabalhando principalmente na persistência de `Veterinario` e `Disponibilidade` utilizando SQLAlchemy e SQLite.

Durante o desenvolvimento, o modelo de domínio também foi atualizado para refletir melhor os requisitos atuais do sistema.

A entidade `Veterinario` passou a possuir os seguintes atributos:

- `id_veterinario`;
- `email`;
- `senha_hash`;
- `nome`;
- `crmv`;
- `especialidade`;
- coleção de `disponibilidades`.

A `Disponibilidade`, que anteriormente havia sido tratada como um objeto de valor, passou a ser representada como uma entidade com identificador próprio.

Ela possui os seguintes atributos:

- `id_disponibilidade`;
- `dia_semana`;
- `hora_inicio`;
- `hora_fim`.

Para representar os dias da semana, foi criado o `Enum` `DiaSemana`, evitando o uso de valores arbitrários para esse atributo.

Também foi atualizada a regra de conflito entre disponibilidades. Duas disponibilidades são consideradas conflitantes apenas quando pertencem ao mesmo dia da semana e possuem sobreposição de horários. Disponibilidades consecutivas continuam sendo permitidas.

Foram atualizados os testes unitários nos arquivos:

`tests/unit/test_disponibilidade.py`

`tests/unit/test_veterinario.py`

Os testes verificam, entre outros comportamentos:

- criação de disponibilidades válidas;
- rejeição de horários inválidos;
- validação do dia da semana;
- conflito de disponibilidades no mesmo dia;
- aceitação de horários consecutivos;
- aceitação de horários sobrepostos em dias diferentes;
- obrigatoriedade dos dados de `Veterinario`.

Na camada de persistência, atualizei o mapeamento ORM no arquivo:

`src/sistema_veterinario/adapters/orm.py`

A tabela de veterinários foi atualizada para armazenar os novos atributos da entidade.

A tabela de disponibilidades passou a utilizar `id_disponibilidade` como chave primária e possui uma chave estrangeira `id_veterinario`, relacionando cada disponibilidade ao veterinário correspondente.

Também foi realizado o mapeamento da entidade `Disponibilidade` e configurado o relacionamento entre `Veterinario` e sua coleção de disponibilidades.

O atributo `dia_semana` foi mapeado utilizando `Enum(DiaSemana)`, permitindo que o domínio continue trabalhando com o Enum mesmo após a persistência no banco de dados.

No arquivo:

`src/sistema_veterinario/adapters/repository.py`

implementei o `SqlAlchemyVeterinarioRepository`, seguindo a abstração definida por `AbstractRepository`.

Esse repositório possui as operações:

- `add()`: adiciona um veterinário à sessão do SQLAlchemy;
- `get()`: recupera um veterinário por meio do seu `id_veterinario`.

Também implementei o `FakeVeterinarioRepository`, que mantém os veterinários em memória utilizando um dicionário. Ele possui a mesma interface básica do repositório real, permitindo adicionar e buscar veterinários sem utilizar banco de dados.

Foi criado o teste de integração:

`tests/integration/test_repository_veterinario.py`

O teste utiliza um banco SQLite em memória e verifica:

- persistência de um `Veterinario`;
- recuperação do veterinário pelo identificador;
- persistência dos atributos `email`, `senha_hash`, `nome`, `crmv` e `especialidade`;
- persistência da coleção de disponibilidades;
- recuperação de `id_disponibilidade`;
- recuperação correta de `hora_inicio` e `hora_fim`;
- recuperação correta de `DiaSemana`.

No teste de integração foi utilizado `session.expunge_all()` antes da busca, garantindo que o objeto recuperado seja novamente carregado a partir do banco de dados e não apenas reutilizado da sessão.

Também foi criado:

`tests/unit/test_fake_repository_veterinario.py`

Os testes verificam:

- adição e recuperação de um veterinário no `FakeVeterinarioRepository`;
- retorno de `None` ao buscar um identificador inexistente.

Além disso, criei:

`tests/integration/conftest.py`

para centralizar a inicialização dos mapeamentos ORM durante os testes de integração. Com isso, o `start_mappers()` é executado uma única vez durante a sessão de testes, evitando inicializações repetidas em cada arquivo.

O teste de integração de Agendamento também foi ajustado para utilizar essa inicialização centralizada.

Ao final das alterações, os testes unitários e os testes de integração permaneceram passando.

#### Commits

Commits realizados neste checkpoint:

- `5f71a2a` - `feat: adiciona mapeamento ORM de veterinario`
- `25adb44` - `refactor: remove import desnecessario de disponibilidade`
- `df3242c` - `feat: atualiza modelo de veterinario e disponibilidade`
- `93dd80e` - `refactor: adapta mapeamento de veterinario e disponibilidade`
- `37678b3` - `feat: adiciona repositorio SQLAlchemy de veterinario`
- `a62f509` - `test: centraliza inicializacao dos mappers nos testes de integracao`
- `8b356d8` - `test: adiciona fake repository de veterinario`

#### Decisões de projeto

Durante este checkpoint, decidi alterar `Disponibilidade` de objeto de valor para entidade, pois ela passou a possuir identidade própria por meio do atributo `id_disponibilidade`. Essa mudança também tornou mais direta a sua representação e persistência no banco de dados.

Mantive `Veterinario` como responsável por controlar sua coleção de disponibilidades e pela regra que impede conflitos de horário. Dessa forma, a regra continua centralizada no agregado em vez de ser transferida para a camada de persistência.

Também decidi representar o dia da semana utilizando o `Enum` `DiaSemana`. Essa escolha restringe os valores possíveis aos dias definidos pelo domínio e evita o uso de textos arbitrários para representar um dia da semana.

No ORM, foi configurado um relacionamento entre `Veterinario` e `Disponibilidade`. Com isso, as disponibilidades associadas ao veterinário podem ser persistidas juntamente com ele, mantendo a relação existente no modelo de domínio.

Foi utilizado `cascade="all, delete-orphan"` no relacionamento, pois uma disponibilidade pertence ao veterinário ao qual está associada. Assim, a persistência acompanha o ciclo de vida dessa associação.

Também optei por implementar um `FakeVeterinarioRepository` com a mesma interface básica do repositório SQLAlchemy. O objetivo é permitir que testes que não precisam acessar o banco possam trabalhar com uma implementação simples em memória, mantendo o código desacoplado da infraestrutura.

A inicialização dos mapeamentos ORM foi centralizada em `tests/integration/conftest.py` para evitar que cada teste de integração tente executar os mesmos mapeamentos novamente.

#### Uso de IA generativa

Utilizei IA generativa durante este checkpoint para esclarecer dúvidas conceituais sobre SQLAlchemy, Repository Pattern e pytest, interpretar mensagens e resultados de testes e revisar código que escrevi durante o desenvolvimento.


### Davi Gesteira dos Anjos Paula

#### O que implementei

Neste checkpoint continuei responsável pelo agregado de Agendamento, trabalhando principalmente na persistência do agregado utilizando SQLAlchemy, na implementação do Repository Pattern e nos testes relacionados à persistência.

Na camada de persistência, implementei inicialmente o mapeamento ORM de `Agendamento` no arquivo:

`src/sistema_veterinario/adapters/orm.py`

Foi criada a tabela `agendamentos` para representar os dados persistidos do agregado.

Durante o checkpoint, o modelo de domínio de `Agendamento` também foi atualizado para ficar mais alinhado ao modelo atual do sistema.

A entidade passou a possuir os seguintes atributos:

- `id_agendamento`;
- `id_paciente`;
- `id_veterinario`;
- `id_unidade`;
- `id_tipo_agendamento`;
- `data_hora`;
- `status`.

A referência direta a `id_cliente`, utilizada anteriormente, foi removida. O paciente já pertence ao agregado Cliente / Paciente, portanto o agendamento passou a manter diretamente a referência ao paciente.

Também foram adicionadas as referências à unidade em que será realizado o atendimento e ao tipo de agendamento.

Mantive `data_hora` como um único atributo para representar conjuntamente a data e o horário do agendamento.

As regras de estado definidas anteriormente para o agregado foram mantidas:

- um novo agendamento inicia com status `AGENDADO`;
- `confirmar()` altera um agendamento de `AGENDADO` para `CONFIRMADO`;
- `cancelar()` permite cancelar um agendamento que esteja em `AGENDADO`;
- `concluir()` permite concluir somente um agendamento que esteja em `CONFIRMADO`;
- a criação continua exigindo que `data_hora` esteja no futuro.

Os testes unitários de Agendamento também foram atualizados para acompanhar as alterações realizadas no modelo.

No arquivo:

`src/sistema_veterinario/adapters/repository.py`

implementei inicialmente o repositório SQLAlchemy responsável pela persistência de Agendamento.

Durante a integração das implementações dos diferentes agregados, o `AbstractRepository` foi generalizado para funcionar como um contrato comum dos repositórios do sistema.

Para Agendamento, a implementação concreta ficou definida como:

`SqlAlchemyAgendamentoRepository`

O repositório possui as operações:

- `add()`: adiciona um agendamento à sessão do SQLAlchemy;
- `get()`: recupera um agendamento por meio de seu `id_agendamento`.

O controle de `commit()` não fica dentro do método `add()`, permitindo que o controle da transação permaneça externo ao repositório.

Também criei o teste de integração:

`tests/integration/test_repository_agendamento.py`

O teste utiliza SQLite em memória e verifica a persistência e recuperação de um objeto `Agendamento` por meio do repositório SQLAlchemy.

O teste verifica a recuperação dos seguintes dados:

- `id_agendamento`;
- `id_paciente`;
- `id_veterinario`;
- `id_unidade`;
- `id_tipo_agendamento`;
- `data_hora`;
- `status`.

Após a generalização do `AbstractRepository` e a alteração do nome da implementação concreta para `SqlAlchemyAgendamentoRepository`, o teste de integração também foi atualizado para utilizar a nova implementação.

Também implementei:

`FakeAgendamentoRepository`

no arquivo:

`src/sistema_veterinario/adapters/repository.py`

O repositório fake mantém os agendamentos em memória utilizando um dicionário, usando o `id_agendamento` como chave.

Foi criado o arquivo:

`tests/unit/test_fake_repository_agendamento.py`

Os testes verificam:

- adição de um agendamento ao `FakeAgendamentoRepository`;
- recuperação de um agendamento pelo seu identificador;
- preservação dos dados do objeto recuperado;
- retorno de `None` ao buscar um identificador inexistente.

Também atualizei o workflow de integração contínua em:

`.github/workflows/ci.yml`

para instalar o SQLAlchemy e executar todos os testes presentes no diretório `tests`, permitindo que os testes de integração também sejam executados pelo GitHub Actions.

#### Commits

Commits realizados neste checkpoint:

- `60fc017` - `feat: adiciona mapeamento ORM de agendamento`
- `9a63294` - `ci: prepara pipeline para testes de integracao`
- `72ac349` - `feat: adiciona repositorio SQLAlchemy de agendamento`
- `9fdc4d5` - `refactor: alinha agendamento ao modelo de dominio`
- `0c5187a` - `test: adiciona teste de integracao do repositorio de agendamento`
- `b70a9ce` - `refactor: generaliza contrato de repositorio`
- `5e3974b` - `refactor: generaliza contrato de repositorio`
- `9a6c4de` - `test: adiciona fake repository de agendamento`

#### Decisões de projeto

Durante este checkpoint, decidi remover a referência direta a `id_cliente` da entidade `Agendamento`. Como o paciente já está associado ao cliente dentro do agregado Cliente / Paciente, manter simultaneamente `id_cliente` e `id_paciente` no Agendamento criaria uma informação redundante. O Agendamento passou, portanto, a referenciar diretamente o paciente.

Também foram adicionadas as referências `id_unidade` e `id_tipo_agendamento`, permitindo representar no agregado onde o atendimento será realizado e qual é o tipo de agendamento.

Mantive `data_hora` como um único atributo em vez de separar data e horário dentro da entidade. Essa representação permite realizar diretamente a validação que impede a criação de agendamentos em momentos passados e mantém a informação temporal do agendamento concentrada em um único valor.

Na camada de persistência, decidi utilizar um `AbstractRepository` genérico como contrato comum para os diferentes agregados. Dessa forma, operações básicas como `add()` e `get()` possuem uma abstração comum, enquanto cada agregado mantém uma implementação concreta específica.

Para Agendamento, foi utilizada a implementação `SqlAlchemyAgendamentoRepository`, que conhece a entidade `Agendamento` e utiliza a sessão do SQLAlchemy para realizar sua persistência.

Também optei por não executar `commit()` dentro do método `add()` do repositório. Dessa maneira, o repositório fica responsável por adicionar e recuperar entidades, enquanto o controle da transação permanece separado dessa responsabilidade.

Para os testes que não precisam utilizar um banco de dados, implementei `FakeAgendamentoRepository`. A implementação utiliza um dicionário em memória indexado pelo `id_agendamento`, mantendo as operações básicas compatíveis com o contrato utilizado pelo repositório real.

No teste de integração, optei por utilizar SQLite em memória. Isso permite exercitar o mapeamento ORM e o repositório SQLAlchemy utilizando um banco real durante o teste, sem criar um arquivo de banco permanente no projeto.