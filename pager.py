#!/usr/bin/env python3
"""Entrypoint CLI do Simulador de Substituição de Páginas.

Uso: python3 pager.py --algo <ALGO> --frames <N> --trace <arquivo> [--verbose]
"""

import sys

from src.engine import ALGORITMOS, formatar_saida, simular
from src.parser import ler_trace, parse_args


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        trace = ler_trace(args.trace)
    except (OSError, ValueError) as e:
        print(f"Erro ao ler trace: {e}", file=sys.stderr)
        return 1

    try:
        resultado = simular(ALGORITMOS[args.algo], args.frames, trace)
    except NotImplementedError as e:
        print(f"[PENDENTE] {args.algo.upper()}: {e}", file=sys.stderr)
        return 2

    print(formatar_saida(resultado, args.verbose))
    return 0


if __name__ == "__main__":
    sys.exit(main())