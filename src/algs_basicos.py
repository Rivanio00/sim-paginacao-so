"""Algoritmos básicos de substituição: FIFO, LRU e Ótimo."""

from typing import List

from .models import AlgoritmoSubstituicao, Frame, Referencia


class FIFO(AlgoritmoSubstituicao):
    """First-In, First-Out.

    Vítima: o frame com a página residente há mais tempo, isto é, o de
    menor ``tempo_carga``. Hits não alteram a ordem.
    Desempate: menor ``tempo_carga`` (e, se ainda empatar, menor ``id``).
    """

    nome = "FIFO"

    def ao_acessar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        # No FIFO, um acerto (HIT) não altera o tempo em que a página entrou na memória.
        pass

    def ao_carregar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        # Registra o momento (passo) em que a página foi carregada no frame.
        frame.tempo_carga = passo

    def selecionar_vitima(self, frames: List[Frame], passo_atual: int) -> int:
        # Escolhe o frame com o menor tempo_carga (a página que entrou primeiro).
        vitima = min(frames, key=lambda f: (f.tempo_carga, f.id))
        return vitima.id


class LRU(AlgoritmoSubstituicao):
    """Least Recently Used.

    Vítima: o frame com menor ``ultimo_acesso`` (acesso mais antigo).
    ``ultimo_acesso`` deve ser atualizado em hits e em cargas.
    Desempate: menor ``tempo_carga``.
    """

    nome = "LRU"

    def ao_acessar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        # Em caso de HIT, atualiza o carimbo de tempo do último uso para o passo atual.
        frame.ultimo_acesso = passo

    def ao_carregar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        # Ao entrar na memória, o primeiro uso da página é o próprio passo de carga.
        frame.ultimo_acesso = passo

    def selecionar_vitima(self, frames: List[Frame], passo_atual: int) -> int:
        # Escolhe o frame cujo ultimo_acesso é o menor (mais antigo).
        # Em caso de empate, desempata pelo menor tempo_carga e menor id.
        vitima = min(frames, key=lambda f: (f.ultimo_acesso, f.tempo_carga, f.id))
        return vitima.id


class Otimo(AlgoritmoSubstituicao):
    """Algoritmo Ótimo (Belady / OPT).

    Usa ``self.trace_completo`` para olhar o futuro: vítima é a página
    cujo próximo uso está mais distante (ou que nunca mais será usada).
    Desempate (várias páginas sem uso futuro): menor ``tempo_carga``.
    """

    nome = "OPT"

    def ao_acessar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        # O algoritmo Ótimo olha apenas para o futuro; hits não exigem metadados extras.
        pass

    def ao_carregar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        # O tempo_carga já é registrado para servir como critério de desempate.
        frame.tempo_carga = passo

    def _proximo_uso(self, pagina: int, passo_atual: int) -> float:
        """Retorna o índice do próximo acesso futuro da página, ou infinito se não houver."""
        # Como passo_atual começa em 1, os acessos futuros começam no índice passo_atual.
        for indice_futuro in range(passo_atual, len(self.trace_completo)):
            if self.trace_completo[indice_futuro].pagina == pagina:
                return float(indice_futuro)
        return float("inf")

    def selecionar_vitima(self, frames: List[Frame], passo_atual: int) -> int:
        # Queremos a MAIOR distância até o próximo uso (-_proximo_uso mais negativo)
        # e, em caso de empate (ex.: duas páginas com distância infinita),
        # o MENOR tempo_carga (página residente há mais tempo).
        vitima = min(
            frames,
            key=lambda f: (-self._proximo_uso(f.pagina, passo_atual), f.tempo_carga, f.id),
        )
        return vitima.id