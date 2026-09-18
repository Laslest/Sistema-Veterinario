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

## Fase 1 - Checkpoint 1

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

A relação entre `Veterinario` e `Unidade` não foi implementada neste checkpoint, pois a implementação da entidade `Unidade` está sob responsabilidade de outro integrante do grupo.

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
