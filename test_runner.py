#!/usr/bin/env python3
"""Validação automatizada dos algoritmos contra os gabaritos conhecidos.

Valores inteiros comparam apenas faltas de página; tuplas comparam
(faltas, evicções, escritas em disco).
"""

import os
import sys

from src.engine import ALGORITMOS, simular
from src.parser import ler_trace

BASE = os.path.dirname(os.path.abspath(__file__))

# (arquivo de trace, nº de frames) -> {algoritmo: esperado}
GABARITOS = {
    ("silberschatz2001.trace", 3): {"fifo": 15, "lru": 12, "opt": 9, "clock": 14,
                                    "nru": 10, "lfu": 13, "mfu": 15},
    ("silberschatz2001.trace", 4): {"fifo": 10, "lru": 8, "opt": 8, "clock": 9,
                                    "nru": 9, "lfu": 9, "mfu": 12},
    ("belady.trace", 3): {"fifo": 9, "lru": 10, "opt": 7},
    ("belady.trace", 4): {"fifo": 10, "lru": 8, "opt": 6},
    ("escritas.trace", 3): {"fifo": (6, 3, 3), "lru": (9, 6, 3),
                            "clock": (8, 5, 3), "nru": (9, 6, 2)},
}


def main() -> int:
    ok = falha = pendente = 0
    for (arquivo, n), esperados in GABARITOS.items():
        trace = ler_trace(os.path.join(BASE, "traces", arquivo))
        print(f"\n== {arquivo} | {n} frames ==")
        for nome, esperado in esperados.items():
            rotulo = f"{nome.upper():<6}"
            try:
                r = simular(ALGORITMOS[nome], n, trace)
            except NotImplementedError:
                print(f"{rotulo} [PENDENTE]")
                pendente += 1
                continue
            if isinstance(esperado, tuple):
                obtido = (r.faltas, r.eviccoes, r.escritas_disco)
                desc = "(faltas, evicções, escritas)"
            else:
                obtido = r.faltas
                desc = "faltas"
            if obtido == esperado:
                print(f"{rotulo} [OK]    {desc} = {obtido}")
                ok += 1
            else:
                print(f"{rotulo} [FALHA] {desc}: esperado {esperado}, obtido {obtido}")
                falha += 1

    print(f"\nResumo: {ok} OK, {falha} FALHA, {pendente} PENDENTE")
    return 1 if falha else 0


if __name__ == "__main__":
    sys.exit(main())