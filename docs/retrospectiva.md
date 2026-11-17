# Retrospectiva

**Decisão: manteríamos a arquitetura em camadas, com Service Layer, Repository e mapeamento imperativo.** As quatro refatorações SOLID e os quatro padrões GoF da Fase 2 ficaram em no máximo duas camadas e nunca mudaram o ORM. Os três riscos do checkpoint 1 continuam abertos, e a única previsão que não se confirmou foi a de que agregados quase CRUD dispensariam as camadas.

## 1. As previsões do checkpoint 1 se confirmaram?

| Previsão em `docs/arquitetura.md` | O que aconteceu na Fase 2 |
|---|---|
| Uma regra de negócio muda só no domínio e no seu teste (cenário 2.1) | **Confirmada.** State (`c627c26`), Strategy (`0e8991f`), Iterator (`0aedaaf`) e a SRP de Veterinário (`86c5816`) alteraram só `domain/model.py` e testes. |
| Os testes unitários isolam o domínio do banco (cenário 2.2) | **Confirmada.** Os padrões GoF foram testados sem banco; a suíte foi de 103 para 120 e 157 testes nas tags dos checkpoints 1, 2 e 3, sempre passando. |
| O fake não reproduz o banco (trade-off 4.3) | **Confirmada e tratada.** A LSP de Cliente (`53715cc`, `f8d4215`) formalizou o contrato e testou se o fake e o repositório SQLAlchemy se comportam igual. |
| O mapeamento imperativo é um ponto sensível (trade-off 4.4) | **Não se manifestou.** `orm.py` não mudou desde `bb4a1dd` (29/09). Apareceu outro custo, comum a qualquer mapeamento do SQLAlchemy: o objeto lido do banco não passa por `__init__`, e o State lê o estado do `status` persistido. |
| A entrada HTTP é acoplada à persistência (risco 3) | **Confirmada.** `flask_app.py` só mudou em refatorações de persistência ou serialização (`53715cc`, `ecffe2f`); a composição continua nele. |
| Dependências sem versão (risco 1) e agendamento sem integridade de referências (risco 2) | **Ainda abertos.** `requirements.txt` segue sem versões e `agendamentos` sem `ForeignKey`. |
| Exceção comparada por texto no cancelamento (seção 4.1) | **Ainda aberta** (`flask_app.py`, linha 119). |
| Para agregados quase CRUD, como Unidade, o benefício das camadas é menor (4.2 e 5.1) | **Não confirmada.** A Fase 2 demonstrou que Unidade também se beneficiou da separação de responsabilidades: a serialização foi extraída das rotas HTTP (`ecffe2f`) e as regras de atendimento foram separadas com Strategy (`0e8991f`). |

O trade-off que mais pesou foi **separação × simplicidade**, a favor da separação: o custo apareceu na quantidade de classes (o State distribuiu a lógica de três métodos em cinco classes), não na dificuldade das mudanças.

## 2. As camadas ajudaram ou atrapalharam?

Ajudaram. Arquivos de produção alterados por commit da Fase 2 (sem os testes):

| Commit | Mudança | Arquivos de produção alterados |
|---|---|---|
| `f730509` | DIP em Agendamento | `domain/model.py`, `service_layer/services.py` |
| `53715cc` | LSP em Cliente | `adapters/repository.py`, `entrypoints/flask_app.py` |
| `86c5816` | SRP em Veterinário | `domain/model.py` |
| `ecffe2f` | SRP em Unidade | `entrypoints/flask_app.py`, `entrypoints/serializers.py` |
| `c627c26` | State em Agendamento | `domain/model.py` |
| `29095ca` | Factory Method em Paciente | `domain/model.py`, `service_layer/services.py` |
| `0e8991f` | Strategy em Unidade | `domain/model.py` |
| `0aedaaf` | Iterator em Veterinário | `domain/model.py` |

Nenhuma mudança tocou mais de duas camadas, e os padrões GoF ficaram no domínio. Com Active Record, a mesma classe teria regra, colunas e consultas, e cada padrão exigiria testes com banco.

### Análise do agregado Veterinário

No agregado Veterinário, as alterações da Fase 2 reforçaram a decisão de manter a arquitetura em camadas.

A primeira mudança foi a refatoração de Responsabilidade Única (SRP), no commit `86c5816`. Antes, `Veterinario.adicionar_disponibilidade()` verificava diretamente a sobreposição dos horários. Com a refatoração, essa comparação passou para `Disponibilidade.conflita_com()`, enquanto `Veterinario` continuou responsável por controlar a inclusão na agenda.

A segunda mudança foi a implementação do padrão Iterator, no commit `0aedaaf`. A classe `IteradorDisponibilidades` passou a concentrar o percurso e a filtragem dos horários por dia da semana, permitindo reutilizar esse comportamento.

Ambas as alterações ficaram na camada de domínio, sem exigir mudanças no SQLAlchemy, nos repositórios ou nos endpoints Flask. Isso confirmou a vantagem da separação entre regras de negócio e persistência.

O principal custo foi acrescentar métodos e uma classe ao domínio. Além disso, a coleção pública de disponibilidades ainda permite modificações diretas, sem passar pela validação de conflitos.

Portanto, manteríamos a arquitetura em camadas, mas consideraríamos melhorar o encapsulamento das disponibilidades para proteger as regras do agregado.

### Análise do agregado Unidade

O agregado Unidade é um exemplo importante para avaliar a previsão de que agregados com comportamento próximo de CRUD teriam menos benefícios com a arquitetura em camadas. Inicialmente, sua implementação parecia relativamente simples, pois suas principais operações envolviam cadastrar e consultar unidades de atendimento. Entretanto, as alterações realizadas na Fase 2 demonstraram que mesmo esse agregado possuía responsabilidades e regras que justificavam uma organização mais cuidadosa.

A primeira alteração ocorreu na aplicação do princípio da Responsabilidade Única (SRP), no commit `ecffe2f`. Antes da refatoração, os endpoints de cadastro e busca de Unidade, em `flask_app.py`, construíam individualmente a representação JSON da entidade, incluindo os dados do endereço e o tratamento de unidades domiciliares sem endereço físico. Essa duplicação fazia com que a responsabilidade de apresentação dos dados ficasse misturada ao fluxo de comunicação HTTP.

A solução foi extrair essa lógica para a função `serializar_unidade()`, localizada em `entrypoints/serializers.py`. Com isso, os endpoints passaram a reutilizar o mesmo componente para produzir suas respostas. A alteração não exigiu mudanças no domínio nem na persistência, demonstrando que a separação das responsabilidades permitiu modificar a apresentação da entidade sem ampliar o impacto da alteração para outras partes do sistema.

A segunda alteração foi a aplicação do padrão Strategy, no commit `0e8991f`. Nesse caso, a questão estava relacionada às próprias regras de negócio de Unidade. A modalidade de atendimento determina comportamentos diferentes: uma unidade presencial precisa possuir um endereço, enquanto uma unidade que realiza atendimento domiciliar pode não possuir um endereço físico.

Uma implementação baseada apenas em uma condição dentro da entidade seria suficiente para atender à regra atual. Entretanto, essa abordagem manteria os comportamentos das modalidades concentrados na própria classe `Unidade`. Com Strategy, foram introduzidas a abstração `PoliticaAtendimento` e as implementações `AtendimentoPresencial` e `AtendimentoDomiciliar`. A entidade passou a selecionar a política correspondente e delegar a validação do endereço, mantendo as regras no domínio e separando os comportamentos de cada modalidade.

As duas alterações apresentam benefícios em pontos diferentes da arquitetura. O SRP organizou a responsabilidade de serialização na camada de entrada, enquanto Strategy organizou as variações de comportamento na camada de domínio. Portanto, não se tratou apenas de adicionar classes ou aplicar padrões por conveniência, mas de responder a problemas identificados na implementação existente.

O custo dessas decisões também deve ser considerado. A extração do serializador introduziu um componente adicional, enquanto Strategy aumentou a quantidade de classes necessárias para representar uma regra que poderia ser escrita com uma condição simples. Esse custo foi considerado aceitável diante da redução da duplicação, da separação das responsabilidades e da possibilidade de estender as políticas de atendimento sem concentrar novas condições na entidade.

Assim, o caso de Unidade contraria a expectativa de que agregados próximos de CRUD necessariamente se beneficiariam menos da arquitetura em camadas. A quantidade de operações não é suficiente para determinar a complexidade de um agregado: suas regras de negócio, responsabilidades e possibilidades de evolução também precisam ser consideradas.

### Análise do agregado Cliente/Paciente

No agregado Cliente/Paciente, as alterações realizadas na Fase 2 envolveram a aplicação do princípio da Substituição de Liskov (LSP) e do padrão Factory Method. As duas mudanças demonstraram como a arquitetura em camadas permite organizar responsabilidades diferentes sem concentrar toda a lógica em uma única parte do sistema.

A primeira alteração foi a formalização do contrato do repositório de Cliente, no commit `53715cc`. Antes dessa refatoração, não havia um contrato específico para esse agregado que estabelecesse o comportamento esperado das implementações. Com a criação da abstração `ClienteRepository`, tanto `FakeClienteRepository` quanto `SqlAlchemyClienteRepository` passaram a implementar o mesmo contrato, incluindo as operações de adicionar e buscar clientes. Também foi estabelecida a regra de que um cliente existente não pode ser substituído por outro com o mesmo identificador, utilizando `ClienteJaCadastradoError` para representar essa situação.

Essa mudança evidenciou a importância da separação entre a camada de serviços e os detalhes de persistência. Os serviços recebem o repositório como dependência, sem precisar conhecer qual implementação está sendo utilizada. Os testes verificam separadamente o comportamento do repositório falso e do repositório SQLAlchemy, incluindo a busca de clientes inexistentes e a rejeição de identificadores duplicados. Na camada de entrada, o Flask trata o conflito e retorna HTTP 409, mantendo a responsabilidade de traduzir os erros para respostas da API.

A segunda alteração foi a aplicação do padrão Factory Method à criação de pacientes, no commit `29095ca`. Antes, o serviço de adição de pacientes instanciava diretamente a classe `Paciente`. Com a refatoração, foram introduzidas a abstração `PacienteFactory` e sua implementação concreta `PacienteFactoryPadrao`, responsáveis por definir e realizar a criação do paciente.

A função `adicionar_paciente()`, na camada de serviços, passou a receber uma fábrica opcional por meio do parâmetro `paciente_factory`, utilizando `PacienteFactoryPadrao` quando nenhuma implementação é fornecida. Dessa forma, o serviço depende da abstração de criação, permitindo a substituição da fábrica sem modificar o fluxo principal do caso de uso. Entretanto, a responsabilidade de associar o paciente ao cliente permaneceu no agregado `Cliente`, que continua verificando as regras de negócio, como a proibição de pacientes com identificadores duplicados.

Os testes acrescentados verificam tanto a criação de pacientes e o respeito às validações da entidade quanto a utilização de uma fábrica injetada no serviço. Isso permitiu conferir que a criação foi delegada à abstração sem retirar do agregado a responsabilidade de controlar sua coleção de pacientes.

As duas alterações trouxeram benefícios distintos para a organização do sistema. O LSP tornou explícito o contrato de persistência do agregado Cliente/Paciente, permitindo utilizar implementações diferentes sem alterar a lógica dos serviços. Já o Factory Method separou a responsabilidade de criação do paciente da coordenação do caso de uso. Em ambos os casos, as mudanças ficaram concentradas nas camadas necessárias, sem exigir uma reestruturação completa da arquitetura.

O custo dessas decisões também deve ser considerado. A formalização do contrato tornou a implementação do repositório mais explícita e exigiu tratamento específico da exceção na camada de entrada. O Factory Method acrescentou duas classes e um parâmetro opcional ao serviço, embora atualmente exista apenas uma fábrica concreta de produção e um único tipo concreto de produto (`Paciente`). Portanto, a flexibilidade para substituir a criação foi introduzida, mas ainda não existem diferentes modalidades de pacientes previstas no domínio atual.

Assim, a experiência com Cliente/Paciente reforçou a decisão de manter a arquitetura em camadas. O LSP demonstrou a importância de contratos consistentes entre as implementações de persistência, enquanto o Factory Method mostrou que a criação de objetos pode ser flexibilizada sem comprometer as responsabilidades do domínio.

As camadas atrapalharam em dois pontos:

- **Composição na entrada:** `flask_app.py` cria engine, sessão e repositórios, e `app = create_app()` na importação gera `sistema_veterinario.db` a cada execução dos e2e, o que levou ao `.db` commitado em `f8d4215` e removido em `b5fd88d`.
- **Duplicação:** cada agregado tem repositório real e falso (150 linhas em `repository.py`), e o contrato só é explícito para Cliente.

## 3. Decisão final

**Manter a arquitetura em camadas**, com quatro ajustes:

1. Fixar versões em `requirements.txt` (no mínimo `SQLAlchemy>=2.1`).
2. Levar a composição para um ponto único chamado por `create_app()` e remover o `create_app()` da importação.
3. Trocar a comparação por texto por exceções do domínio (como `AgendamentoNaoEncontrado`), com testes e2e dos erros.
4. Garantir as referências de Agendamento: `ForeignKey` em `agendamentos` e verificação em `criar_agendamento()`.

Revemos a conclusão do checkpoint 1 de que agregados quase CRUD aceitariam uma solução mais simples: não adotaríamos um híbrido com Active Record. Unidade parecia simples, mas já tinha desde a Fase 1 a regra de endereço opcional e recebeu um Strategy; dois estilos no mesmo sistema obrigariam todos a conhecer os dois.

