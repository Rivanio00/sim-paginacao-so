"""Algoritmos básicos de substituição: FIFO, LRU e Ótimo (stubs)."""

from typing import List

from .models import AlgoritmoSubstituicao, Frame, Referencia

_MSG = "Aguardando implementação"


class FIFO(AlgoritmoSubstituicao):
    """First-In, First-Out.

    Vítima: o frame com a página residente há mais tempo, isto é, o de
    menor ``tempo_carga``. Hits não alteram a ordem.
    Desempate: menor ``tempo_carga`` (e, se ainda empatar, menor ``id``).
    """

    nome = "FIFO"

    def ao_acessar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        raise NotImplementedError(_MSG)

    def ao_carregar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        raise NotImplementedError(_MSG)

    def selecionar_vitima(self, frames: List[Frame], passo_atual: int) -> int:
        raise NotImplementedError(_MSG)


class LRU(AlgoritmoSubstituicao):
    """Least Recently Used.

    Vítima: o frame com menor ``ultimo_acesso`` (acesso mais antigo).
    ``ultimo_acesso`` deve ser atualizado em hits e em cargas.
    Desempate: menor ``tempo_carga``.
    """

    nome = "LRU"

    def ao_acessar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        raise NotImplementedError(_MSG)

    def ao_carregar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        raise NotImplementedError(_MSG)

    def selecionar_vitima(self, frames: List[Frame], passo_atual: int) -> int:
        raise NotImplementedError(_MSG)


class Otimo(AlgoritmoSubstituicao):
    """Algoritmo Ótimo (Belady / OPT).

    Usa ``self.trace_completo`` para olhar o futuro: vítima é a página
    cujo próximo uso está mais distante (ou que nunca mais será usada).
    Desempate (várias páginas sem uso futuro): menor ``tempo_carga``.
    """

    nome = "OPT"

    def ao_acessar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        raise NotImplementedError(_MSG)

    def ao_carregar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        raise NotImplementedError(_MSG)

    def selecionar_vitima(self, frames: List[Frame], passo_atual: int) -> int:
        raise NotImplementedError(_MSG)