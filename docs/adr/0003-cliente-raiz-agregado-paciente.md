# ADR 0003 — Cliente como raiz do agregado Cliente / Paciente

- **Autor:** David Pereira Ramos (@dramos-cpu)
- **Status:** Aceita. A decisão foi tomada na Fase 1 e está sendo registrada e reavaliada no Checkpoint 1 da Fase 2.
- **Data do registro:** 21/10/2026

## Contexto

O sistema veterinário precisa representar os clientes responsáveis pelos animais atendidos. Cada `Cliente` possui dados próprios de identificação e mantém uma coleção de objetos `Paciente`. Cada paciente possui identidade própria através de `id_paciente`, além de nome, data de nascimento e referência à raça.

Durante a construção da Fase 1, foi necessário definir a fronteira entre essas duas entidades. Embora `Paciente` possua identidade própria, isso não significa necessariamente que ele precise ser uma raiz de agregado independente.

A principal decisão era escolher entre permitir que `Paciente` tivesse persistência e operações próprias ou manter seu ciclo de vida associado ao `Cliente` responsável.

A evolução do código mostra essa decisão acontecendo progressivamente. A entidade `Paciente` foi introduzida no commit `ca43c8a`, e posteriormente `Cliente` foi criado explicitamente como **raiz do agregado Cliente / Paciente** no commit `29e37f3`.

No modelo atual:

- `Cliente` mantém uma coleção de pacientes;
- `Cliente` possui operações para adicionar, buscar e remover pacientes;
- a inclusão de pacientes duplicados é impedida através de `id_paciente`;
- `Paciente` possui identidade própria, mas não possui repositório próprio;
- a persistência do agregado é realizada através de `SqlAlchemyClienteRepository`;
- a versão em memória utilizada nos testes é `FakeClienteRepository`;
- os pacientes são persistidos através do relacionamento ORM existente com `Cliente`;
- a camada de serviço recupera a raiz antes de realizar operações relacionadas à coleção de pacientes;
- a API permite cadastrar e consultar clientes e adicionar pacientes a um cliente.

## Decisão

Manter `Cliente` como a **raiz do agregado Cliente / Paciente**.

`Paciente` continua sendo uma entidade do domínio, pois possui uma identidade própria através de `id_paciente`, mas seu ciclo de vida permanece subordinado ao agregado cuja raiz é `Cliente`.

Isso significa que alterações relacionadas à coleção de pacientes devem passar por `Cliente`.

A responsabilidade de manter as invariantes dessa associação permanece na entidade raiz. Por exemplo, a regra que impede a inclusão de dois pacientes com o mesmo identificador é executada por `Cliente.adicionar_paciente()` e não pela API ou pelo repositório.

Na camada de persistência, essa decisão é refletida pela existência de apenas um repositório para o agregado: `SqlAlchemyClienteRepository`.

Não foi criado um `SqlAlchemyPacienteRepository`. Os pacientes são persistidos e recuperados através do relacionamento entre `Cliente` e `Paciente`.

O mesmo princípio foi mantido no repositório utilizado nos testes. O sistema possui `FakeClienteRepository`, sem uma implementação fake separada para `Paciente`.

Na camada de serviço, o caso de uso `adicionar_paciente()` recupera primeiro o `Cliente`, cria a entidade `Paciente` e delega à raiz a operação de inclusão.

Durante a implementação da entrega final chegou a existir um caso de uso separado para `buscar_paciente()`. Esse caso de uso foi posteriormente removido no commit `a807a62`, mantendo a camada de serviço concentrada nos fluxos necessários para a raiz do agregado.

## Alternativas consideradas

### 1. Transformar Paciente em uma raiz de agregado independente

Nesta alternativa, `Paciente` teria seu próprio repositório, como `SqlAlchemyPacienteRepository`, além de casos de uso próprios para criação, consulta e alteração.

**Vantagens:**

- permitiria consultar e persistir pacientes diretamente;
- facilitaria operações focadas exclusivamente em pacientes;
- evitaria recuperar o cliente em determinadas consultas.

**Desvantagens:**

- adicionaria outro repositório, outro fake e mais casos de uso;
- permitiria modificar pacientes sem necessariamente passar pelas regras mantidas por `Cliente`;
- aumentaria a quantidade de pontos de entrada para modificar informações pertencentes à mesma relação de domínio.

**Por que não foi escolhida:**

No domínio atual, não existe uma necessidade concreta de administrar o ciclo de vida de um paciente separadamente do cliente responsável. A separação acrescentaria complexidade sem resolver um problema existente.

### 2. Manter Cliente como raiz, mas criar um repositório de leitura para Paciente

Nesta alternativa, as operações de alteração continuariam sendo realizadas através de `Cliente`, porém existiria um repositório específico para consultar pacientes diretamente.

**Vantagens:**

- uma busca por `id_paciente` seria mais direta;
- permitiria implementar consultas globais sobre pacientes sem recuperar clientes.

**Desvantagens:**

- introduziria uma abstração adicional somente para consultas;
- aumentaria a quantidade de código de persistência;
- tornaria menos clara a fronteira atual do agregado.

**Por que não foi escolhida:**

Os casos de uso existentes não exigem consultas globais ou independentes de pacientes. Criar essa abstração antecipadamente aumentaria a complexidade sem necessidade comprovada.

### 3. Acessar Paciente diretamente através do SQLAlchemy

Outra possibilidade seria utilizar a sessão do SQLAlchemy diretamente nos serviços ou endpoints para consultar ou modificar pacientes.

**Vantagens:**

- menos classes e abstrações;
- determinadas consultas poderiam ser implementadas com menos código.

**Desvantagens:**

- os serviços e endpoints passariam a conhecer detalhes da persistência;
- seria possível modificar pacientes sem passar pelas regras de `Cliente`;
- aumentaria o acoplamento com SQLAlchemy;
- enfraqueceria a fronteira definida para o agregado.

**Por que não foi escolhida:**

As regras relacionadas à associação entre cliente e paciente pertencem ao domínio. Permitir alterações diretamente através da infraestrutura tornaria mais fácil contornar essas regras.

## Consequências

### Positivas

- As regras relacionadas à coleção de pacientes ficam centralizadas em `Cliente`.
- A prevenção de pacientes duplicados permanece no domínio.
- Existe apenas uma porta de persistência para o agregado.
- Não foi necessário criar `SqlAlchemyPacienteRepository`.
- Não foi necessário criar `FakePacienteRepository`.
- Os testes da camada de serviço podem utilizar `FakeClienteRepository` sem inicializar SQLAlchemy ou banco de dados.
- A camada de serviço não precisa conhecer detalhes do relacionamento entre as tabelas `clientes` e `pacientes`.
- Os testes de integração conseguem salvar um cliente juntamente com seus pacientes e reconstruir posteriormente a coleção através do ORM.
- Os testes E2E conseguem adicionar um paciente e consultar novamente o cliente para confirmar que a alteração foi persistida.

### Negativas e trade-offs

- Consultar um paciente isoladamente pode exigir primeiro identificar ou recuperar seu cliente.
- O repositório atual não oferece consultas globais sobre pacientes.
- Uma operação como listar todos os pacientes de determinada raça exigiria uma nova solução de consulta.
- Caso `Paciente` ganhe muitas responsabilidades próprias, `Cliente` pode começar a concentrar operações demais.
- `FakeClienteRepository` não reproduz todas as restrições existentes no banco relacional, portanto os testes de integração continuam necessários.
- A decisão prioriza consistência e centralização das regras, mas deixa algumas consultas menos diretas.

## Evolução da decisão no repositório

A decisão de manter `Cliente` como raiz pode ser observada em diferentes etapas da Fase 1.

O commit `ca43c8a` introduziu a entidade `Paciente`.

Em seguida, o commit `29e37f3` criou `Cliente` explicitamente como raiz do agregado Cliente / Paciente.

O comportamento da raiz foi coberto pelo commit `e4de5de`, que adicionou os testes de `Cliente`, incluindo operações relacionadas à coleção de pacientes.

Na persistência, o commit `9e6f465` introduziu as tabelas de clientes e pacientes e o commit `6d248c0` implementou o mapeamento ORM do agregado.

O commit `72fc4cc` introduziu o `SqlAlchemyClienteRepository`. Não houve criação de um repositório equivalente para `Paciente`.

Essa decisão foi validada pelo teste de integração introduzido em `4242c70`, que verifica a persistência e recuperação do cliente e de seus pacientes.

Para testes sem banco, o commit `0cdbe4c` introduziu `FakeClienteRepository`, enquanto `1bbe0ae` adicionou seus testes.

Na camada de serviço, o commit `59992c9` adicionou os casos de uso do agregado e `4898333` adicionou os respectivos testes unitários.

Durante a revisão desses casos de uso, o commit `a807a62` removeu o caso de uso independente `buscar_paciente()`, reduzindo operações que tratavam `Paciente` separadamente da raiz.

Por fim, o commit `f05ba5a` adicionou os endpoints da API e `9b49979` adicionou os testes E2E. Esses testes verificam inclusive que, depois de adicionar um paciente, uma nova consulta ao cliente retorna o paciente na coleção persistida.

## Riscos e evolução prevista

A decisão atual deverá ser reavaliada caso `Paciente` passe a possuir um ciclo de vida significativamente independente de `Cliente`.

Algumas mudanças de requisito poderiam justificar essa revisão:

- busca global de pacientes por nome;
- busca de pacientes por raça ou espécie;
- transferência de um paciente entre clientes;
- prontuário clínico com ciclo de vida independente;
- operações administrativas diretamente sobre pacientes;
- consultas frequentes de pacientes sem necessidade de carregar o cliente;
- novas associações de `Paciente` com outros agregados.

Caso essas necessidades apareçam, `Paciente` poderá ser promovido a uma raiz de agregado própria ou poderá ser criada uma solução específica para consultas.

Essa mudança deve ser orientada por uma necessidade concreta do sistema. O fato de `Paciente` possuir `id_paciente` não é, sozinho, motivo suficiente para transformá-lo em uma raiz de agregado.

## Evidências relacionadas

- `ca43c8a` — `feat: adicionado a entidade Paciente a respeito do Agregado Cliente / Paciente.`  
  Introduziu `Paciente` como entidade com identidade própria no domínio.

- `29e37f3` — `feat: adiciona a entidade Cliente, Raiz do Agregado Cliente / Paciente.`  
  Estabeleceu explicitamente `Cliente` como raiz do agregado.

- `e4de5de` — `test: adiciona testes para Cliente, Raiz do Agregado Cliente / Paciente`  
  Verificou as regras e operações mantidas pela raiz, incluindo o controle da coleção de pacientes.

- `9e6f465` — `feat: adiciona tabelas Cliente e Paciente ao ORM`  
  Criou as estruturas utilizadas para persistir as duas entidades.

- `6d248c0` — `feat: adiciona mapeamento ORM do agregado Cliente/Paciente`  
  Configurou a associação entre `Cliente` e `Paciente` na camada de persistência.

- `72fc4cc` — `feat: adiciona repositório SQLAlchemy de Cliente`  
  Criou o repositório da raiz do agregado sem introduzir um repositório independente para `Paciente`.

- `4242c70` — `test: adiciona testes de integração do repositório de Cliente`  
  Verificou a persistência e recuperação do agregado utilizando SQLite em memória.

- `0cdbe4c` — `feat: adiciona FakeClienteRepository`  
  Criou a implementação em memória do repositório da raiz.

- `1bbe0ae` — `test: adiciona testes do FakeRepository de Cliente`  
  Verificou o comportamento da implementação fake utilizada nos testes.

- `59992c9` — `feat: adiciona casos de uso do agregado Cliente / Paciente`  
  Adicionou a camada de aplicação responsável por coordenar os fluxos do agregado.

- `4898333` — `test: adiciona testes unitarios dos casos de uso do Cliente`  
  Verificou os casos de uso utilizando o repositório em memória.

- `a807a62` — `refactor: remove caso de uso buscar_paciente referente ao agregado Cliente / Paciente`  
  Removeu uma operação independente de consulta de paciente e manteve os casos de uso necessários concentrados no agregado.

- `f05ba5a` — `adiciona API do agregado Cliente / Paciente`  
  Disponibilizou os casos de uso através da API Flask.

- `9b49979` — `test: adiciona testes da API do agregado Cliente / Paciente`  
  Verificou o fluxo completo pela API, incluindo a persistência e posterior recuperação do paciente através do cliente.