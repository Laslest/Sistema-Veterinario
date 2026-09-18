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