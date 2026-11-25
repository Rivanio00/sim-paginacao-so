"""Algoritmos avançados de substituição: Clock, NRU, LFU e MFU (stubs)."""

from typing import List

from .models import AlgoritmoSubstituicao, Frame, Referencia

_MSG = "Aguardando implementação"


class Clock(AlgoritmoSubstituicao):
    """Segunda Chance com ponteiro circular (Clock).

    Percorre os frames circularmente: se ``bit_r == 1`` zera o bit e avança;
    se ``bit_r == 0`` seleciona o frame como vítima. O ponteiro avança
    para depois da vítima.
    Desempate: menor ``tempo_carga`` na definição da posição inicial.
    """

    nome = "Clock"

    def ao_acessar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        raise NotImplementedError(_MSG)

    def ao_carregar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        raise NotImplementedError(_MSG)

    def selecionar_vitima(self, frames: List[Frame], passo_atual: int) -> int:
        raise NotImplementedError(_MSG)


class NRU(AlgoritmoSubstituicao):
    """Not Recently Used.

    Classes por (bit_r, bit_m): 0=(0,0), 1=(0,1), 2=(1,0), 3=(1,1).
    Vítima: frame da menor classe não vazia. O bit R é zerado periodicamente
    (ver ``pos_passo``).
    Desempate dentro da classe: menor ``tempo_carga``.
    """

    nome = "NRU"

    def ao_acessar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        raise NotImplementedError(_MSG)

    def ao_carregar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        raise NotImplementedError(_MSG)

    def selecionar_vitima(self, frames: List[Frame], passo_atual: int) -> int:
        raise NotImplementedError(_MSG)


class LFU(AlgoritmoSubstituicao):
    """Least Frequently Used.

    Vítima: frame com menor ``contador_uso``.
    Desempate: menor ``tempo_carga``.
    """

    nome = "LFU"

    def ao_acessar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        raise NotImplementedError(_MSG)

    def ao_carregar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        raise NotImplementedError(_MSG)

    def selecionar_vitima(self, frames: List[Frame], passo_atual: int) -> int:
        raise NotImplementedError(_MSG)


class MFU(AlgoritmoSubstituicao):
    """Most Frequently Used.

    Vítima: frame com maior ``contador_uso``.
    Desempate: menor ``tempo_carga``.
    """

    nome = "MFU"

    def ao_acessar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        raise NotImplementedError(_MSG)

    def ao_carregar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        raise NotImplementedError(_MSG)

    def selecionar_vitima(self, frames: List[Frame], passo_atual: int) -> int:
        raise NotImplementedError(_MSG)