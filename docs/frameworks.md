# Frameworks

O sistema usa três frameworks: **Flask** (entrada HTTP), **SQLAlchemy** (persistência) e **pytest** (testes). Nenhum deles é importado por `domain/model.py`, que usa apenas a biblioteca padrão (`abc`, `dataclasses`, `datetime`, `typing`, `enum`), nem por `service_layer/services.py`, que importa apenas o domínio. Os trechos citados foram conferidos no commit `9149c61`, com as versões instaladas por `pip install -r requirements.txt` (que não fixa versões): Flask 3.1.3, SQLAlchemy 2.1.5 e pytest 9.1.1.

## 1. Papel de cada framework

| Framework | Papel na solução | Camada / pasta | Por que o domínio não depende dele |
|---|---|---|---|
| Flask | Recebe as requisições HTTP, encaminha cada rota para uma função e devolve JSON | `entrypoints/flask_app.py` | As rotas traduzem o JSON em parâmetros, abrem a sessão e o repositório, chamam `services`, confirmam ou desfazem a transação e traduzem o resultado em código HTTP. As regras (data futura, transições de status, CPF) ficam no domínio (entidades e objetos de valor), que não conhece `request` nem `jsonify`. |
| SQLAlchemy | Mapeia as entidades para tabelas e controla as transações | `adapters/orm.py`, `adapters/repository.py`; a sessão é criada em `entrypoints/flask_app.py` | O mapeamento é imperativo (`registry.map_imperatively` em `start_mappers()`): as classes do domínio não herdam de `Base` nem declaram colunas. Por isso os testes unitários criam entidades sem banco. |
| pytest | Descobre e executa os testes unitários, de integração e e2e | `tests/` | O domínio não importa pytest; os testes é que importam o domínio. |

## 2. Pontos de inversão de controle

Usar uma **biblioteca** é chamar o código dela quando o nosso código decide: `datetime.now()` em `RelogioDoSistema` é uma chamada que o grupo faz e controla. Usar um **framework** é o contrário: o framework controla o fluxo e chama o código do grupo nos momentos que ele define. Os três frameworks fazem isso no sistema:

1. **Registro de rotas (Flask).** Em `create_app()`, funções como `criar_agendamento()` são registradas com `@app.route("/agendamentos", methods=["POST"])`. Nenhum código do grupo chama essas funções: o Flask recebe a requisição, escolhe a rota pelo caminho e pelo método e chama a função, que devolve a resposta para ele.
2. **Fixtures e descoberta de testes (pytest).** Em `tests/integration/conftest.py`, a fixture `configurar_mappers()` (`scope="session", autouse=True`) nunca é chamada pelo grupo: o pytest a executa uma vez antes dos testes de integração. Da mesma forma, o pytest encontra as funções `test_*` pelo nome e gera um caso para cada linha de `@pytest.mark.parametrize` (por exemplo, em `tests/unit/test_estado_agendamento.py`).
3. **Mapeamento do ORM (SQLAlchemy).** Depois de `map_imperatively(Agendamento, agendamentos)`, é o SQLAlchemy que cria os objetos do domínio ao ler do banco, sem chamar `__init__`, e que preenche seus atributos. Verificamos isso: um `Agendamento` lido com `session.get` não passa por `__init__`. Por isso o padrão State do Agendamento obtém o estado a partir do `status` persistido, e não de algo criado no construtor.

## 3. Padrões que os frameworks usam internamente

| Padrão | Framework | Onde aparece no código do grupo |
|---|---|---|
| **Data Mapper** (Fowler, PoEAA) | SQLAlchemy | `adapters/orm.py`: `start_mappers()` liga cada classe do domínio à sua tabela por fora da classe; `composite(CPF, ...)`, `composite(Telefone, ...)` e `composite(Endereco, ...)` mapeiam objetos de valor para colunas. |
| **Unit of Work** (Fowler, PoEAA) | SQLAlchemy | `entrypoints/flask_app.py`: cada rota abre `session = Session()`; nenhum repositório chama `commit()`: eles só registram os objetos na sessão (`session.add()`), e a gravação acontece de uma vez em `session.commit()` ou é descartada em `session.rollback()`. |
| **Identity Map** (Fowler, PoEAA) | SQLAlchemy | `adapters/repository.py`: `get()` usa `self.session.get(Agendamento, id)`. Na mesma sessão, duas chamadas devolvem o mesmo objeto (verificado: `a is b` é verdadeiro), sem nova consulta. |
| **Factory** | SQLAlchemy | `entrypoints/flask_app.py`: `Session = sessionmaker(bind=engine)` devolve uma fábrica de sessões já configurada com o engine (uma fábrica configurável, não o Factory Method do GoF); cada rota pede uma sessão nova a ela. |
| **Proxy** (GoF) | Flask | `entrypoints/flask_app.py`: `request.get_json(silent=True)`. `flask.request` é um `LocalProxy` do Werkzeug: um objeto global que repassa cada acesso para a requisição atual. |

## 4. O que mudaria com Django

- **Modelo:** as entidades herdariam de `django.db.models.Model`, com os campos declarados na própria classe (Active Record). O domínio passaria a depender do framework, e `Agendamento.confirmar()` ficaria na mesma classe que sabe se salvar.
- **Persistência:** `orm.py`, `start_mappers()` e boa parte de `repository.py` desapareceriam; as tabelas sairiam das migrações geradas pelo Django. Os objetos de valor (`CPF`, `Telefone`, `Endereco`) precisariam virar campos ou modelos próprios, porque o ORM do Django não tem equivalente direto ao `composite`.
- **Entrada:** as rotas de `flask_app.py` virariam views registradas em `urls.py`, com o tratamento de requisição e transação dado pelo framework.
- **Testes:** a maioria dos testes de modelo usaria o banco de testes do Django (`django.test.TestCase`), e os repositórios falsos perderiam o sentido. Os testes unitários ficariam mais lentos e acoplados ao banco.
- **Ganhos:** painel administrativo, migrações, autenticação e validação de formulários prontos, com bem menos código de infraestrutura para escrever.


## 5. Veterinário — relationship e cascade das disponibilidades

### Relacionamento no SQLAlchemy

No agregado Veterinário, a entidade `Veterinario` possui uma coleção de disponibilidades, que representa os dias e horários em que o profissional pode realizar atendimentos.

O relacionamento entre `Veterinario` e `Disponibilidade` é configurado pelo SQLAlchemy no arquivo `src/sistema_veterinario/adapters/orm.py`.

A tabela `disponibilidades` possui a coluna `id_veterinario`, que funciona como chave estrangeira para a tabela `veterinarios`.

O mapeamento é definido em `start_mappers()`:

```python
if inspect(Veterinario, raiseerr=False) is None:
    mapper_registry.map_imperatively(
        Veterinario,
        veterinarios,
        properties={
            "disponibilidades": relationship(
                Disponibilidade,
                cascade="all, delete-orphan",
            ),
        },
    )
```

O método `relationship()` permite que o SQLAlchemy associe as disponibilidades ao veterinário correspondente. Dessa forma, o código pode trabalhar com a coleção `veterinario.disponibilidades`, sem precisar executar manualmente uma consulta para cada associação.

Esse relacionamento representa uma associação de um veterinário para várias disponibilidades.

### Funcionamento do cascade

A configuração `cascade="all, delete-orphan"` define como o SQLAlchemy gerencia os objetos associados durante as operações de persistência.

O parâmetro `all` inclui operações como salvar, atualizar e excluir objetos relacionados. Assim, ao adicionar um veterinário à sessão, suas disponibilidades associadas também podem ser persistidas.

O `delete-orphan` determina que uma disponibilidade removida da coleção do veterinário seja excluída do banco quando a sessão sincronizar as alterações.

A configuração também permite que, ao excluir um veterinário por meio da sessão ORM, suas disponibilidades relacionadas sejam excluídas.

Esse comportamento é gerenciado pelo SQLAlchemy. Não se trata de um `ON DELETE CASCADE` definido diretamente na chave estrangeira do banco.

### Relação com a arquitetura do projeto

O uso de `relationship()` e `cascade` mantém os detalhes da persistência na camada de infraestrutura.

A classe `Veterinario`, em `domain/model.py`, não precisa importar SQLAlchemy para controlar suas disponibilidades. Ela continua responsável pelas regras de negócio, como impedir a inclusão de intervalos conflitantes.

Já o SQLAlchemy cuida da associação entre as tabelas e do acompanhamento das alterações realizadas nos objetos durante a sessão.

Essa separação facilita os testes unitários do domínio, que podem trabalhar com objetos `Veterinario` e `Disponibilidade` sem depender de um banco de dados.

### Evidência no repositório

O arquivo `tests/integration/test_repository_veterinario.py` contém o teste `test_repository_salva_e_busca_veterinario()`.

Nesse teste, uma disponibilidade é adicionada ao veterinário, o objeto é salvo utilizando o repositório SQLAlchemy e a transação é confirmada com `session.commit()`.

Depois, o teste limpa os objetos da sessão com `session.expunge_all()` e recupera o veterinário pelo repositório.

As verificações confirmam que a disponibilidade foi persistida e recuperada com seu identificador, dia da semana e horários.

Esse teste demonstra o funcionamento da associação na persistência. Ele não verifica diretamente a exclusão em cascata ou a remoção de objetos órfãos.

### Benefícios e limitações

O principal benefício desse mapeamento é evitar a implementação manual de operações de persistência para cada disponibilidade associada ao veterinário.

A configuração também mantém as classes de domínio independentes do SQLAlchemy, seguindo a arquitetura em camadas adotada pelo grupo.

Por outro lado, o uso de `cascade` exige atenção. A remoção de um objeto da coleção pode provocar sua exclusão no banco de dados, mesmo que a intenção inicial tenha sido apenas alterar a associação.

Além disso, a coleção `disponibilidades` continua pública e pode ser modificada diretamente, sem passar pelas validações realizadas no método `adicionar_disponibilidade()`.

Por isso, considero a configuração adequada para o sistema atual, mas o comportamento de exclusão e o encapsulamento da coleção merecem atenção caso o sistema evolua.

## 6. Unidade — composite e return_none_on do Endereco

### Mapeamento do objeto de valor no SQLAlchemy

No agregado Unidade, o objeto de valor `Endereco` representa as informações de localização de uma unidade de atendimento. Ele é composto pelos atributos `rua`, `numero`, `bairro`, `cidade`, `estado` e `cep`.

O mapeamento entre `Unidade` e a tabela `unidades` é configurado pelo SQLAlchemy no arquivo `src/sistema_veterinario/adapters/orm.py`, utilizando `map_imperatively()` dentro de `start_mappers()`.

Diferentemente de uma entidade com tabela própria, o endereço é armazenado diretamente na tabela `unidades`, por meio de seis colunas correspondentes aos seus atributos.

O mapeamento utiliza o recurso `composite()`:

```python
if inspect(Unidade, raiseerr=False) is None:
    mapper_registry.map_imperatively(
        Unidade,
        unidades,
        properties={
            "endereco": composite(
                Endereco,
                unidades.c.rua,
                unidades.c.numero,
                unidades.c.bairro,
                unidades.c.cidade,
                unidades.c.estado,
                unidades.c.cep,
                return_none_on=lambda *campos: all(
                    campo is None for campo in campos
                ),
            ),
        },
    )
```

O método `composite()` permite agrupar várias colunas da tabela em um único objeto de valor. Dessa forma, quando uma unidade é recuperada pelo SQLAlchemy, os valores armazenados nas colunas do endereço são utilizados para representar uma instância de `Endereco`.

### Funcionamento do composite e return_none_on

A utilização de `composite()` permite manter o endereço como parte da entidade `Unidade`, sem a necessidade de criar uma tabela ou um repositório específico para ele.

Entretanto, o sistema permite cadastrar unidades que realizam atendimento exclusivamente domiciliar sem possuir um endereço físico. Por isso, o mapeamento precisa tratar a possibilidade de todas as colunas do endereço estarem nulas.

Para resolver essa situação, foi utilizado o parâmetro `return_none_on`.

A função verifica se todos os campos recebidos estão com valor `None`. Quando essa condição é verdadeira, o SQLAlchemy representa o atributo `endereco` como `None`, em vez de criar um objeto `Endereco` com todos os atributos nulos.

Esse comportamento permite preservar a regra do domínio: unidades que realizam atendimento presencial precisam obrigatoriamente de endereço, enquanto unidades que realizam atendimento domiciliar podem ser cadastradas sem ele.

### Relação com a arquitetura do projeto

O uso de `composite()` mantém os detalhes de persistência na camada de infraestrutura.

A classe `Endereco`, localizada em `domain/model.py`, é definida como um objeto de valor imutável utilizando `@dataclass(frozen=True)`. Ela possui validações próprias para os campos de rua, cidade, estado e CEP.

Já a entidade `Unidade` permanece responsável pelas regras relacionadas ao tipo de atendimento. A validação é delegada às políticas `AtendimentoPresencial` e `AtendimentoDomiciliar`, que determinam se o endereço pode ou não ser ausente.

O domínio não precisa importar ou conhecer o SQLAlchemy para representar essas regras. O framework é utilizado apenas na camada de adapters, responsável por converter os dados entre os objetos do domínio e as tabelas do banco.

Essa separação permite testar as regras de negócio independentemente da infraestrutura de persistência.

### Evidência no repositório

O arquivo `tests/integration/test_repository_unidade.py` contém o teste `test_repository_salva_e_busca_unidade()`.

Nesse teste, uma unidade com endereço é criada, adicionada ao `SqlAlchemyUnidadeRepository` e persistida utilizando SQLite em memória. Em seguida, são verificadas as informações recuperadas, incluindo os atributos de rua e CEP.

O arquivo `tests/e2e/test_unidade_api.py` também contém testes relacionados ao comportamento do endereço pela API.

O teste `test_api_cadastra_unidade_com_endereco()` verifica o cadastro de uma unidade com endereço informado. Já o teste `test_api_cadastra_unidade_domiciliar_sem_endereco()` verifica o cadastro de uma unidade domiciliar com `endereco: None` e sua posterior consulta pela API.

Além disso, o arquivo `tests/unit/test_unidade_endereco.py` contém o teste `test_unidade_fisica_sem_endereco_gera_erro()`, que verifica se uma unidade física é impedida de ser criada sem endereço.

### Benefícios e limitações

O principal benefício dessa abordagem é permitir que o endereço seja representado como um objeto de valor dentro da entidade `Unidade`, sem acrescentar uma tabela ou operações de persistência desnecessárias.

O uso de `return_none_on` também permite representar corretamente a ausência de endereço no banco, mantendo o comportamento esperado para unidades domiciliares.

Outro benefício é a separação entre domínio e infraestrutura, pois as regras de validação permanecem nas classes do domínio, enquanto o SQLAlchemy fica responsável pelo mapeamento e pela persistência.

Por outro lado, as colunas relacionadas ao endereço são anuláveis no banco de dados. Isso significa que uma inserção realizada diretamente no banco poderia cadastrar uma unidade física sem endereço, ignorando as validações do domínio.

Além disso, o teste de integração atual não limpa a sessão antes de recuperar a unidade, utilizando a mesma sessão após a persistência. Um teste adicional com `session.expunge_all()` poderia verificar de forma mais isolada a reconstrução do objeto `Endereco` a partir dos dados armazenados.

Considero essa solução adequada ao sistema atual, pois mantém o modelo de persistência simples, evita a criação de uma entidade desnecessária e preserva a regra que diferencia unidades físicas de unidades domiciliares.

## 7. Cliente/Paciente — composite e relationship

### Mapeamento dos objetos de valor com composite

No agregado Cliente/Paciente, o SQLAlchemy utiliza `composite()` para mapear os objetos de valor `CPF` e `Telefone` às colunas correspondentes da tabela `clientes`.

A tabela `clientes`, definida em `src/sistema_veterinario/adapters/orm.py`, possui as colunas `cpf_numero` e `telefone_numero`, responsáveis por armazenar os respectivos números.

O mapeamento é realizado em `start_mappers()`:

```python
mapper_registry.map_imperatively(
    Cliente,
    clientes,
    properties={
        "cpf": composite(CPF, clientes.c.cpf_numero),
        "telefone": composite(
            Telefone,
            clientes.c.telefone_numero,
        ),
        "pacientes": relationship(Paciente),
    },
)
```

O uso de `composite()` permite que os valores armazenados nas colunas sejam representados como instâncias das classes `CPF` e `Telefone` na aplicação.

Na camada de domínio, ambas são definidas como objetos de valor imutáveis (`dataclass(frozen=True)`), possuem o atributo `numero` e implementam suas próprias validações.

Assim, o SQLAlchemy realiza a conversão entre as colunas do banco de dados e os objetos utilizados pelo domínio, sem que essas classes precisem conhecer os detalhes do ORM.

### Mapeamento da coleção de pacientes com relationship

A associação entre `Cliente` e `Paciente` é realizada por meio de `relationship()`. Na tabela `pacientes`, a coluna `id_cliente` funciona como chave estrangeira para `clientes.id_cliente`.

O relacionamento é configurado no mapeamento da classe `Cliente`:

```python
"pacientes": relationship(Paciente)
```

Essa configuração permite que o SQLAlchemy associe os registros de pacientes ao respectivo cliente e disponibilize essa associação por meio da coleção `cliente.pacientes`.

No domínio, a classe `Cliente` já possui essa coleção e disponibiliza os métodos `adicionar_paciente()`, `buscar_paciente()` e `remover_paciente()`. Além disso, o método de adição impede que dois pacientes com o mesmo identificador sejam incluídos na coleção.

Diferentemente do relacionamento utilizado no agregado Veterinário, esse mapeamento não declara explicitamente configurações de `cascade`.

### Relação com a arquitetura do projeto

Os mapeamentos de `CPF`, `Telefone` e `Paciente` são definidos externamente, no arquivo `adapters/orm.py`, utilizando `map_imperatively()`.

Dessa maneira, as classes `Cliente`, `Paciente`, `CPF` e `Telefone`, localizadas em `domain/model.py`, não precisam importar SQLAlchemy ou herdar de classes do framework.

O domínio permanece responsável pelas regras de negócio, incluindo as validações dos objetos de valor e o controle da coleção de pacientes. Já o adaptador de persistência define como essas estruturas são relacionadas às tabelas do banco de dados.

Essa organização mantém a separação entre as regras de negócio e os detalhes de infraestrutura.

### Evidência no repositório

O arquivo `tests/integration/test_repository_cliente.py` contém testes que verificam o funcionamento dos mapeamentos utilizando um banco SQLite em memória.

No teste `test_repository_salva_e_busca_cliente()`, um cliente é persistido e posteriormente recuperado após a limpeza da sessão com `session.expunge_all()`. As verificações confirmam que os atributos `cpf` e `telefone` continuam sendo instâncias das respectivas classes e preservam seus números.

No teste `test_repository_salva_cliente_com_paciente()`, um paciente é associado ao cliente por meio de `adicionar_paciente()`. Após a persistência e recuperação do cliente, o teste verifica se a coleção contém o paciente e se seus atributos foram preservados.

Esses testes demonstram que os objetos de valor e a associação entre cliente e paciente são reconstruídos corretamente durante a recuperação dos dados.

### Benefícios e limitações

O uso de `composite()` permite trabalhar com objetos de valor no domínio, mantendo suas validações centralizadas nas respectivas classes, enquanto os dados permanecem armazenados em colunas do banco.

O `relationship()` facilita o acesso à coleção de pacientes associados a um cliente, evitando que a aplicação precise implementar manualmente essa associação em cada consulta.

Além disso, a definição externa dos mapeamentos mantém as classes do domínio independentes do SQLAlchemy, permitindo que os testes unitários trabalhem com essas classes sem depender de um banco de dados.

Por outro lado, o relacionamento atual não define explicitamente opções de `cascade` nem configura uma associação bidirecional com `back_populates`. Portanto, o gerenciamento da persistência e da exclusão de pacientes relacionados deve considerar as configurações efetivamente declaradas no ORM.