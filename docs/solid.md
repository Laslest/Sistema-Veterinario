# Refatorações SOLID

## Agendamento — Davi Gesteira dos Anjos Paula

### Princípio violado

**Princípio da Inversão de Dependência (DIP).** A regra de negócio de `Agendamento` dependia diretamente de um detalhe concreto, o relógio do processo, em vez de depender de uma abstração.

Commit "antes": `9fdc4d5` (`refactor: alinha agendamento ao modelo de dominio`, 26/09/2026), em `src/sistema_veterinario/domain/model.py`:

```python
class Agendamento:

    def __init__(
        self,
        id_agendamento,
        id_paciente,
        id_veterinario,
        id_unidade,
        id_tipo_agendamento,
        data_hora,
    ):
        if data_hora <= datetime.now():
            raise ValueError("A data do agendamento deve ser futura")
```

### Problema concreto

A regra "a data do agendamento deve ser futura" consultava `datetime.now()` diretamente. Assim, o resultado dependia do fuso horário do servidor, e nem o caso de uso nem os testes conseguiam controlar qual é o "agora":

- A mesma requisição `POST /agendamentos` com `data_hora` = `2026-10-30T23:50:00`, enviada em 30/10/2026 por volta das 22h45 (horário de Brasília), respondeu **201** com o processo em `TZ=America/Sao_Paulo` e **400** ("A data do agendamento deve ser futura") com o processo em `TZ=UTC`, fuso usado pelo runner `ubuntu-latest` da CI. Isso foi observado em 30/10/2026; para reproduzir, a `data_hora` precisa estar entre o horário de Brasília e o horário UTC do momento.
- O limite da regra (`data_hora` exatamente igual ao instante atual) não podia ser testado, porque o instante muda durante o teste. Por isso os testes da Fase 1 usam margens de ±1 dia.

### Refatoração

Commit "depois": `f730509` (`refactor: inverte dependência do Agendamento em relação ao relógio do sistema (DIP)`, 31/10/2026).

- Criada a abstração `Relogio` (classe abstrata com `agora()`) em `domain/model.py`, junto da implementação `RelogioDoSistema`, que devolve `datetime.now()`.
- `Agendamento.__init__` recebe o parâmetro opcional `relogio` e compara `data_hora` com `relogio.agora()`. Sem relógio informado, usa `RelogioDoSistema`.
- `services.criar_agendamento` recebe e repassa o `relogio`.

```python
class Relogio(ABC):

    @abstractmethod
    def agora(self) -> datetime:
        raise NotImplementedError


class RelogioDoSistema(Relogio):

    def agora(self) -> datetime:
        return datetime.now()


class Agendamento:

    def __init__(
        self,
        id_agendamento,
        id_paciente,
        id_veterinario,
        id_unidade,
        id_tipo_agendamento,
        data_hora,
        relogio: Optional[Relogio] = None,
    ):
        if relogio is None:
            relogio = RelogioDoSistema()

        if data_hora <= relogio.agora():
            raise ValueError("A data do agendamento deve ser futura")
```

A refatoração não corrige o problema de fuso, cujo comportamento padrão foi mantido de propósito; ela torna o "agora" substituível sem alterar `Agendamento`.

### Como os testes garantiram que o comportamento não mudou

- Os testes da Fase 1 que exercitam a criação de agendamento (`tests/unit/test_agendamento.py`, `tests/unit/test_services_agendamento.py`, `tests/unit/test_fake_repository_agendamento.py`, `tests/integration/test_repository_agendamento.py` e `tests/e2e/test_agendamento_api.py`) não foram alterados e continuam passando, assim como o restante da suíte. Eles chamam `Agendamento` e `criar_agendamento` sem informar relógio, ou seja, pelo caminho padrão.
- O arquivo novo `tests/unit/test_agendamento_relogio.py` verifica o ponto de injeção com um `RelogioFixo`: aceita uma data um minuto após o relógio injetado, mesmo estando no passado real; rejeita uma data igual ao instante do relógio, cobrindo o limite `<=`; e confirma que `criar_agendamento` repassa o relógio ao `Agendamento`.
- Resultado: a suíte foi de 103 para 106 testes, todos passando.

### Custo e por que compensa

O custo é pequeno: duas classes novas (`Relogio` e `RelogioDoSistema`) e um parâmetro opcional em `Agendamento` e em `criar_agendamento`, num total de 21 linhas adicionadas e 1 removida em código de produção (`git show --numstat f730509`). A indireção também é pequena: quem lê `Agendamento` precisa saber que o "agora" vem de um objeto.

Limitação: o domínio ainda instancia `RelogioDoSistema` como padrão, o que foi aceito para não alterar as chamadas e os testes existentes.

O custo compensa porque a regra de data é a principal invariante na criação de um agendamento e passa a ser testável de forma determinística, inclusive no limite. Além disso, a correção do problema de fuso deixa de exigir mudança na entidade: basta fornecer outro `Relogio`.

### Cliente — David Pereira Ramos

### Princípio relacionado

**Princípio da Substituição de Liskov (LSP).**

O Princípio da Substituição de Liskov estabelece que implementações de uma abstração devem poder ser utilizadas de maneira intercambiável, sem comprometer o comportamento esperado pelo contrato.

Neste caso, as implementações `FakeClienteRepository` e `SqlAlchemyClienteRepository` devem respeitar as mesmas regras comportamentais do repositório de Cliente, independentemente da tecnologia utilizada para armazenamento.

### Problema concreto

Antes da refatoração, as duas implementações apresentavam comportamentos diferentes diante de clientes com o mesmo identificador.

As implementações originais foram introduzidas nos seguintes commits:

- `72fc4cc` (`feat: adiciona repositório SQLAlchemy de Cliente`, 27/09/2026).
- `0cdbe4c` (`feat: adiciona FakeClienteRepository`, 27/09/2026).

No estado anterior à refatoração, o método `add()` do `FakeClienteRepository` realizava uma atribuição direta ao dicionário:

```python
def add(self, cliente: Cliente):
    self.clientes[cliente.id_cliente] = cliente
```

Dessa forma, quando outro cliente com o mesmo identificador era adicionado, o objeto anteriormente armazenado era silenciosamente substituído.

Já o `SqlAlchemyClienteRepository` realizava apenas a inclusão do objeto na sessão:

```python
def add(self, cliente: Cliente):
    self.session.add(cliente)
```

Nesse caso, não existia uma verificação explícita de duplicidade no método `add()`. A restrição de chave primária do banco de dados ficava responsável por impedir a persistência de registros com o mesmo identificador.

Portanto, as implementações apresentavam comportamentos diferentes diante da mesma situação.

O contrato abstrato anterior, baseado em `AbstractRepository`, não especificava explicitamente como as implementações deveriam tratar a duplicidade de identificadores.

Essa inconsistência motivou a formalização de um contrato específico para o repositório de Cliente, alinhando o comportamento das implementações.

### Refatoração

Commit "depois": `53715cc` (`refactor: formaliza contrato do repositório de Cliente`, 02/11/2026).

Foram realizadas as seguintes alterações:

- Criada a classe abstrata `ClienteRepository`, especializada no contrato do agregado Cliente/Paciente.
- Criada a exceção `ClienteJaCadastradoError`, utilizada para identificar tentativas de cadastro de clientes com identificadores já existentes.
- Alterado o `SqlAlchemyClienteRepository` para herdar de `ClienteRepository`.
- Alterado o `FakeClienteRepository` para herdar de `ClienteRepository`.
- Implementada uma verificação de duplicidade no `FakeClienteRepository`, impedindo a substituição de um cliente por outro com o mesmo ID.
- Implementada uma verificação de duplicidade no `SqlAlchemyClienteRepository`, considerando tanto outros clientes pendentes na sessão quanto clientes já persistidos.
- Atualizado o endpoint de cadastro de Cliente em `flask_app.py` para tratar `ClienteJaCadastradoError`, além de `IntegrityError`, retornando HTTP 409 em caso de duplicidade ou dados inválidos.

A partir da refatoração, as duas implementações passaram a respeitar a mesma regra comportamental: um objeto `Cliente` diferente não pode substituir outro cliente que já possua o mesmo identificador.

Com isso, foi formalizado um contrato comum para as implementações Fake e SQLAlchemy, fortalecendo sua substituibilidade e alinhando seus comportamentos.

### Como os testes garantiram a preservação do comportamento

Foram acrescentados testes para verificar o contrato nas diferentes camadas da aplicação:

- **Testes unitários:** verificam que o `FakeClienteRepository` rejeita a inclusão de outro cliente com o mesmo ID e preserva o objeto originalmente cadastrado.
- **Testes de integração:** verificam que o `SqlAlchemyClienteRepository` também rejeita clientes com identificadores duplicados e mantém os dados do cliente original.
- **Testes E2E:** verificam que a API retorna HTTP 409 quando ocorre uma tentativa de cadastrar outro cliente com um ID já existente, preservando o cadastro original.

Os resultados dos testes específicos foram:

- 3 testes unitários aprovados.
- 4 testes de integração aprovados.
- 4 testes E2E aprovados.

Além dos testes específicos, a suíte completa do projeto foi executada e todos os testes passaram, sem regressões identificadas.

### Custo e por que compensa

A refatoração introduziu uma abstração específica para o repositório de Cliente, uma exceção para representar tentativas de cadastro duplicado e verificações explícitas nas duas implementações.

O custo adicional consiste na manutenção desse contrato e das verificações de unicidade em ambas as implementações.

Esse custo compensa porque elimina a inconsistência comportamental existente entre os repositórios Fake e SQLAlchemy, tornando explícita uma regra importante do agregado Cliente/Paciente.

Além disso, os testes permitem verificar que as duas implementações respeitam o mesmo contrato, reduzindo o risco de diferenças de comportamento quando uma implementação é substituída pela outra.

A principal contribuição para o LSP foi, portanto, a formalização do contrato comportamental e o alinhamento das implementações, fortalecendo a possibilidade de utilizá-las de maneira intercambiável.

## Unidade / Local de Atendimento — Cauã Raphael Santos de Paula

### Princípio aplicado

**Princípio da Responsabilidade Única (SRP), aplicado à apresentação da API.** A conversão da entidade Unidade para o JSON de resposta foi concentrada em uma função própria.

### Evidência e problema

Antes do commit `ecffe2f`, os endpoints `cadastrar_unidade_endpoint` e `buscar_unidade_endpoint`, em `src/sistema_veterinario/entrypoints/flask_app.py`, montavam separadamente o mesmo JSON de Unidade. Ambos enumeravam os mesmos campos e convertiam `Endereco`, incluindo o caso em que o endereço é ausente.

Assim, uma alteração no formato de resposta da Unidade exigia atualizar os dois endpoints. Isso criava risco de o cadastro e a busca devolverem representações diferentes.

### Refatoração

No commit `ecffe2f` (`refactor: aplica SRP na serializacao de Unidade`, 02/11/2026 no horário de Brasília), extraí a conversão para `serializar_unidade`, em `src/sistema_veterinario/entrypoints/serializers.py`. Os dois endpoints agora chamam essa função.

As rotas continuam cuidando do fluxo HTTP, da sessão, da chamada dos serviços e dos códigos de status. O serializador apenas transforma a Unidade em um dicionário compatível com a resposta da API. O comportamento de domínio não foi alterado: endereço presente continua sendo serializado, e endereço ausente continua resultando em `"endereco": null`.

### Testes e evidência

- `tests/unit/test_serializers.py` cobre unidades com endereço e domiciliares sem endereço.
- `tests/e2e/test_unidade_api.py` confirma que a busca após o cadastro domiciliar retorna o mesmo JSON do cadastro.
- A CI do commit `ecffe2f` executou a suíte completa e terminou com sucesso: [execução 103](https://github.com/Laslest/Sistema-Veterinario/actions/runs/41562531649).

### Custo e limite

A mudança adiciona o módulo `serializers.py` e uma função de apresentação específica para Unidade. Em troca, remove a duplicação entre cadastro e busca e mantém a representação da API em um ponto. O escopo foi mantido nessa resposta; as outras rotas e agregados não foram alterados.
