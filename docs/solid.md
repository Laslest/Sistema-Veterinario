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
