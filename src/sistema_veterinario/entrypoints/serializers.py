"""Serialização das entidades de Unidade para a resposta da API."""


def serializar_unidade(unidade):
    endereco = unidade.endereco

    return {
        "id_unidade": unidade.id_unidade,
        "nome": unidade.nome,
        "atende_domicilio": unidade.atende_domicilio,
        "endereco": (
            {
                "rua": endereco.rua,
                "numero": endereco.numero,
                "bairro": endereco.bairro,
                "cidade": endereco.cidade,
                "estado": endereco.estado,
                "cep": endereco.cep,
            }
            if endereco is not None
            else None
        ),
    }
