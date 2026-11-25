"""Estruturas de dados e interface base dos algoritmos de substituição."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Referencia:
    """Uma referência de memória do trace: página acessada e tipo ('R' ou 'W')."""
    pagina: int
    tipo: str


@dataclass
class Frame:
    """Um quadro de memória física."""
    id: int
    pagina: Optional[int] = None
    bit_r: int = 0
    bit_m: int = 0
    tempo_carga: int = 0
    ultimo_acesso: int = 0
    contador_uso: int = 0


class AlgoritmoSubstituicao:
    """Interface base para algoritmos de substituição de páginas.

    O motor (engine) chama os ganchos abaixo. Regra geral de desempate:
    em caso de empate entre candidatos, escolhe-se o frame com menor
    ``tempo_carga`` (a página residente há mais tempo).
    """

    nome: str = "BASE"

    def __init__(self, num_frames: int, trace_completo: List[Referencia]) -> None:
        self.num_frames = num_frames
        self.trace_completo = trace_completo

    def ao_acessar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        """Chamado em um HIT, com o frame que contém a página referenciada."""
        raise NotImplementedError("Aguardando implementação do membro responsável")

    def ao_carregar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        """Chamado após carregar uma página em um frame (FAULT)."""
        raise NotImplementedError("Aguardando implementação do membro responsável")

    def selecionar_vitima(self, frames: List[Frame], passo_atual: int) -> int:
        """Retorna o ``frame.id`` do frame a ser substituído."""
        raise NotImplementedError("Aguardando implementação do membro responsável")

    def pos_passo(self, frames: List[Frame], passo: int) -> None:
        """Chamado ao final de cada referência (hit ou fault)."""
        pass