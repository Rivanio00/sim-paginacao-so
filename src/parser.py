"""Leitura de argumentos de CLI e de arquivos .trace."""

import argparse
import re
from typing import List

from .models import Referencia

ALGORITMOS_VALIDOS = ["fifo", "lru", "opt", "clock", "nru", "lfu", "mfu"]

_PADRAO_LINHA = re.compile(r"^(\d+)\s*([RrWw])?$")


def _frames_positivo(valor: str) -> int:
    try:
        n = int(valor)
    except ValueError:
        raise argparse.ArgumentTypeError(f"--frames deve ser um inteiro (recebido: {valor!r})")
    if n < 1:
        raise argparse.ArgumentTypeError("--frames deve ser >= 1")
    return n


def _algo_valido(valor: str) -> str:
    v = valor.strip().lower()
    if v not in ALGORITMOS_VALIDOS:
        raise argparse.ArgumentTypeError(
            f"algoritmo inválido: {valor!r} (opções: {', '.join(ALGORITMOS_VALIDOS)})"
        )
    return v


def parse_args(argv=None) -> argparse.Namespace:
    """Interpreta os argumentos de linha de comando."""
    p = argparse.ArgumentParser(
        prog="pager.py",
        description="Simulador de Substituição de Páginas",
    )
    p.add_argument("--algo", required=True, type=_algo_valido,
                   help="fifo, lru, opt, clock, nru, lfu ou mfu (case-insensitive)")
    p.add_argument("--frames", required=True, type=_frames_positivo,
                   help="número de frames (inteiro >= 1)")
    p.add_argument("--trace", required=True, help="caminho do arquivo .trace")
    p.add_argument("--verbose", action="store_true",
                   help="imprime o estado a cada passo")
    return p.parse_args(argv)


def ler_trace(caminho: str) -> List[Referencia]:
    """Lê um arquivo .trace e devolve a lista de referências.

    Ignora linhas em branco e linhas iniciadas por '#'.
    Formatos aceitos: "7", "0 R", "0R", "1 W", "1W".
    """
    refs: List[Referencia] = []
    with open(caminho, "r", encoding="utf-8") as f:
        for num, linha in enumerate(f, start=1):
            texto = linha.strip()
            if not texto or texto.startswith("#"):
                continue
            m = _PADRAO_LINHA.match(texto)
            if not m:
                raise ValueError(f"{caminho}:{num}: linha inválida: {texto!r}")
            tipo = (m.group(2) or "R").upper()
            refs.append(Referencia(pagina=int(m.group(1)), tipo=tipo))
    return refs