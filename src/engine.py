"""Motor principal da simulação e formatação de saída."""

from dataclasses import dataclass, field
from typing import Dict, List, Type

from .algs_avancados import LFU, MFU, NRU, Clock
from .algs_basicos import FIFO, LRU, Otimo
from .models import AlgoritmoSubstituicao, Frame, Referencia

ALGORITMOS: Dict[str, Type[AlgoritmoSubstituicao]] = {
    "fifo": FIFO,
    "lru": LRU,
    "opt": Otimo,
    "clock": Clock,
    "nru": NRU,
    "lfu": LFU,
    "mfu": MFU,
}


@dataclass
class Resultado:
    nome: str
    num_frames: int
    total_refs: int
    faltas: int
    eviccoes: int
    escritas_disco: int
    frames: List[Frame]
    linhas_verbose: List[str] = field(default_factory=list)

    @property
    def taxa_faltas(self) -> float:
        return (self.faltas / self.total_refs * 100.0) if self.total_refs else 0.0


def _estado(frames: List[Frame]) -> str:
    itens = ["." if f.pagina is None else str(f.pagina) for f in frames]
    return "[" + " ".join(itens) + "]"


def simular(classe_algo: Type[AlgoritmoSubstituicao], num_frames: int,
            trace: List[Referencia]) -> Resultado:
    """Executa a simulação. Propaga NotImplementedError dos algoritmos stub."""
    algo = classe_algo(num_frames, trace)
    frames = [Frame(id=i) for i in range(num_frames)]
    faltas = eviccoes = escritas = 0
    linhas: List[str] = []

    for passo, ref in enumerate(trace, start=1):
        alvo = next((f for f in frames if f.pagina == ref.pagina), None)

        if alvo is not None:  # HIT
            algo.ao_acessar(alvo, passo, ref)
            if ref.tipo == "W":
                alvo.bit_m = 1
            sufixo = "acerto"
        else:  # FAULT
            faltas += 1
            livre = next((f for f in frames if f.pagina is None), None)
            if livre is not None:
                livre.pagina = ref.pagina
                livre.tempo_carga = passo
                livre.bit_m = 1 if ref.tipo == "W" else 0
                algo.ao_carregar(livre, passo, ref)
                sufixo = "falta"
            else:
                vitima_id = algo.selecionar_vitima(frames, passo)
                v = frames[vitima_id]
                removida = v.pagina
                disco = v.bit_m == 1
                if disco:
                    escritas += 1
                eviccoes += 1
                v.pagina = ref.pagina
                v.tempo_carga = passo
                v.bit_m = 1 if ref.tipo == "W" else 0
                algo.ao_carregar(v, passo, ref)
                sufixo = f"falta (remove {removida}, disco)" if disco else f"falta (remove {removida})"

        algo.pos_passo(frames, passo)
        linhas.append(f"{passo} ref={ref.pagina} {_estado(frames)} {sufixo}")

    return Resultado(
        nome=classe_algo.nome,
        num_frames=num_frames,
        total_refs=len(trace),
        faltas=faltas,
        eviccoes=eviccoes,
        escritas_disco=escritas,
        frames=frames,
        linhas_verbose=linhas,
    )


def formatar_resumo(r: Resultado) -> str:
    ids = " ".join(str(f.id) for f in r.frames)
    paginas = " ".join("-" if f.pagina is None else str(f.pagina) for f in r.frames)
    return "\n".join([
        f"Algoritmo: {r.nome}",
        f"Frames: {r.num_frames}",
        f"Referências: {r.total_refs}",
        f"Faltas de página: {r.faltas}",
        f"Taxa de faltas: {r.taxa_faltas:.2f}%",
        f"Evicções: {r.eviccoes}",
        f"Escritas em disco: {r.escritas_disco}",
        "Conjunto residente final:",
        f"frame_ids: {ids}",
        f"page_ids: {paginas}",
    ])


def formatar_saida(r: Resultado, verbose: bool = False) -> str:
    partes = []
    if verbose:
        partes.extend(r.linhas_verbose)
    partes.append(formatar_resumo(r))
    return "\n".join(partes)