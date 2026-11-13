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
