# ADR 0002 — Endereço como objeto de valor no agregado Unidade

- **Autor:** Cauã Raphael Santos de Paula (@cauaraphael)
- **Status:** Aceita. Decisão implementada na Fase 1 e registrada para reavaliação no Checkpoint 1 da Fase 2.
- **Data do registro:** 20/10/2026

## Contexto

O sistema veterinário permite cadastrar locais de atendimento, que podem ser clínicas físicas ou unidades que realizam atendimento a domicílio. A entidade `Unidade` precisa guardar um nome, identificar cada local por `id_unidade` e indicar se realiza atendimento domiciliar. Uma clínica que não atende a domicílio precisa ter um endereço; já uma unidade que atende a domicílio pode ser cadastrada sem endereço fixo.

O endereço possui rua, número, bairro, cidade, estado e CEP, mas não precisa de um identificador ou ciclo de vida próprio neste sistema. Ele é utilizado como parte dos dados da unidade. Era necessário preservar essa regra ao criar unidades pela API e ao salvar e recuperar os objetos pelo SQLAlchemy, inclusive quando o endereço não é informado.

Na implementação atual:

- `src/sistema_veterinario/domain/model.py` declara `Endereco` como `@dataclass(frozen=True)`, com validação de rua, cidade, estado e CEP de oito dígitos; declara `Unidade` como entidade identificada por `id_unidade`;
- `Unidade.__post_init__()` exige nome e impede unidades não domiciliares de serem criadas sem endereço;
- `src/sistema_veterinario/service_layer/services.py` implementa `cadastrar_unidade()` e `buscar_unidade()`, recebendo um repositório como parâmetro;
- `src/sistema_veterinario/adapters/repository.py` oferece `SqlAlchemyUnidadeRepository` e `FakeUnidadeRepository` com as operações `add()` e `get()`;
- `src/sistema_veterinario/adapters/orm.py` mapeia os campos de `Endereco` como um `composite()` na tabela `unidades`, sem criar uma tabela separada para o endereço;
- `src/sistema_veterinario/entrypoints/flask_app.py` monta o objeto `Endereco` quando o JSON traz um endereço e o deixa como `None` quando não traz, delegando o cadastro à camada de serviço.

## Decisão

Representar `Endereco` como **objeto de valor imutável**, armazenado como parte de `Unidade`, e manter `Unidade` como a entidade responsável pela regra de obrigatoriedade do endereço. Duas unidades são identificadas pelo mesmo `id_unidade`; dois endereços são descritos pelos seus valores, sem um ID próprio.

A regra escolhida é: quando `atende_domicilio` é `False`, `endereco` não pode ser `None`; quando `atende_domicilio` é `True`, `endereco` pode ser `None`. Isso não proíbe que uma unidade que atende a domicílio também possua endereço.

As validações são feitas no domínio e não dependem de Flask ou SQLAlchemy. A API apenas converte o JSON para `Endereco` e `Unidade`, e a persistência utiliza mapeamento imperativo. O `composite()` reúne as seis colunas do endereço em um objeto e usa `return_none_on` quando todas estão nulas, para representar corretamente a ausência de endereço.

Essa escolha mantém os conceitos do domínio explícitos e permite testar as regras sem precisar iniciar a aplicação HTTP ou consultar um banco de dados.

## Alternativas consideradas

### 1. Endereço como entidade própria, em outra tabela

Criar uma classe `Endereco` com identificador, repositório próprio e relacionamento com `Unidade`.

- **Vantagens:** permitiria compartilhar endereços entre unidades e gerenciar seus registros separadamente.
- **Desvantagens:** acrescentaria tabela, chave estrangeira, relacionamento e operações de persistência para algo que ainda não tem identidade nem uso independente no domínio.
- **Por que não:** no sistema atual o endereço só descreve uma unidade; não há necessidade demonstrada de gerenciá-lo como entidade autônoma.

### 2. Exigir endereço para todas as unidades

Tornar `endereco` obrigatório mesmo para um serviço exclusivamente domiciliar, usando, por exemplo, o endereço administrativo da empresa.

- **Vantagens:** evitaria valores opcionais e tornaria o mapeamento e as consultas mais simples.
- **Desvantagens:** impediria cadastrar serviços domiciliares que não possuem local físico de atendimento e criaria a obrigação de informar um endereço que não representa necessariamente o local do atendimento.
- **Por que não:** a regra do negócio diferencia a clínica física da prestação de serviço a domicílio.

### 3. Fazer as validações diretamente na rota Flask

Validar CEP, campos obrigatórios e o tipo de atendimento apenas no endpoint `POST /unidades`.

- **Vantagens:** implementação inicial curta e próxima da entrada dos dados.
- **Desvantagens:** outra interface ou um teste que instanciasse `Unidade` diretamente poderia ignorar a regra; seria necessário repetir a validação.
- **Por que não:** a obrigatoriedade de endereço é uma regra do domínio, não uma regra do protocolo HTTP.

## Consequências

**Positivas**

- A regra de endereço obrigatório para unidade física está concentrada em `Unidade.__post_init__()`, enquanto `Endereco.__post_init__()` verifica o formato mínimo de um endereço informado.
- O atributo `endereco` não exige uma entidade ou tabela própria. Suas colunas estão na tabela `unidades` e são agrupadas pelo mapeamento `composite()`.
- `Endereco` é imutável por ser uma dataclass congelada, evitando alterações parciais acidentais no objeto de valor.
- Testes unitários exercitam as regras diretamente, e os casos de uso podem ser testados com `FakeUnidadeRepository`.
- A API permite cadastrar uma unidade domiciliar com `endereco: null`, caso coberto em `tests/e2e/test_unidade_api.py`.

**Negativas e trade-offs**

- Manter endereço opcional exige tratamento de `None` na API, na serialização e no mapeamento ORM. Essa complexidade adicional é o custo de representar corretamente os dois tipos de unidade.
- O endereço está espalhado por seis colunas na tabela `unidades`. Caso o sistema precise compartilhar endereços ou manter histórico de mudanças de local, o modelo poderá exigir revisão.
- A validação de `Endereco` cobre rua, cidade, estado e CEP, mas não exige atualmente número nem bairro. É uma decisão simples para o escopo atual, porém pode exigir maior rigor em uma futura integração com mapas ou logística.
- `FakeUnidadeRepository` armazena unidades em dicionário e não reproduz todas as restrições e situações do banco relacional; por isso, testes de integração continuam necessários.
- A tabela possui colunas de endereço anuláveis. Uma inserção externa ao domínio poderia gravar uma unidade física sem endereço; a regra de `Unidade` não substitui uma restrição de integridade no banco.

**Riscos e evolução prevista**

- Incluir um teste de integração que salve uma unidade domiciliar sem endereço, limpe a sessão e a consulte novamente, verificando que `endereco` retorna `None`. O teste E2E atual cobre o cadastro, mas uma leitura em sessão nova exercitaria melhor a reconstituição pelo ORM.
- Reavaliar os campos obrigatórios caso o endereço seja utilizado para cálculo de deslocamento ou localização geográfica.
- Se o sistema passar a exigir compartilhamento, histórico ou manutenção independente de endereços, reconsiderar a alternativa de entidade própria.

## Evidências relacionadas

- `5224767` — `feat: adiciona objeto de valor Endereco`: criação do objeto de valor no domínio.
- `3b833f7` — `feat: adiciona entidade Unidade`: implementação da entidade e da regra de endereço obrigatório para unidade física.
- `b400d4e` — `test: adiciona testes de unidade e endereco`: testes iniciais das regras de domínio (posteriormente organizados em `tests/unit/test_unidade_endereco.py`).
- `91cb828` — `feat: adiciona mapeamento ORM de unidade/endereco`: mapeamento dos dados da unidade e do endereço no SQLAlchemy.
- `6636ada` — `feat: adiciona repositorio de unidade e teste de integracao`: repositório real e teste com banco SQLite em memória.
- `885608d` — `feat: adiciona casos de uso de unidade`: operações `cadastrar_unidade()` e `buscar_unidade()`.
- `f2e9690` — `test: adiciona testes dos servicos de unidade`: testes unitários dos casos de uso com repositório falso.
- `844079e` — `feat: adiciona endpoints de unidade`: endpoints de criação e busca HTTP.
- `7c68eee` — `test: adiciona testes e2e de unidade`: testes de cadastro e consulta pela API.
- `bb4a1dd` — `fix: trata endereco opcional no mapeamento de unidade`: ajuste para endereço nulo na persistência.
