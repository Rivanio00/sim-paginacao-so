# Simulador de Algoritmos de Substituição de Páginas

Simulador desenvolvido em Python. O objetivo é simular e comparar o comportamento de algoritmos clássicos de gerenciamento de memória virtual a partir de cadeias de referências (`.trace`).

## Algoritmos Suportados

* `fifo` — First-In, First-Out
* `lru` — Least Recently Used
* `opt` — Ótimo (Belady's Optimal Algorithm)
* `clock` — Segunda Chance / Clock
* `nru` — Not Recently Used
* `lfu` — Least Frequently Used
* `mfu` — Most Frequently Used

---

## Estrutura do Repositório

```text
simulador-paginacao-so/
├── docs/
|   └── DECISOES.md              # Arquitetura, contratos de interface e decisões de projeto
├── src/
│   ├── __init__.py
│   ├── models.py                # Estruturas base (Frame, Referencia, Interface Algoritmo)
│   ├── parser.py                # Leitura de argumentos CLI e parsing de arquivos .trace
│   ├── engine.py                # Motor de simulação, métricas e formatação de saída
│   ├── algs_basicos.py         # Implementação: FIFO, LRU e Ótimo
│   └── algs_avancados.py       # Implementação: Clock, NRU, LFU e MFU
├── traces/
│   ├── silberschatz2001.trace   # Cadeia oficial (20 acessos, 6 páginas)
│   ├── belady.trace             # Cadeia para demonstração da anomalia de Belady
│   └── escritas.trace           # Cadeia com operações R/W para teste de escrita em disco
├── pager.py                     # Ponto de entrada (CLI) do simulador
├── test_runner.py               # Script de validação automatizada contra os gabaritos
└── README.md                    # Este arquivo
```

---

## Pré-requisitos

* **Python 3.8+** instalado no ambiente (utiliza apenas bibliotecas padrão da linguagem, sem dependências externas).

---

## Como Executar

A execução é feita via linha de comando através do script `pager.py`:

```bash
python3 pager.py --algo <ALGO> --frames <N> --trace <ARQUIVO> [--verbose]
```

### Parâmetros
* `--algo`: Nome do algoritmo (`fifo`, `lru`, `opt`, `clock`, `nru`, `lfu` ou `mfu`).
* `--frames`: Quantidade de molduras (frames) na memória física (inteiro $\ge 1$).
* `--trace`: Caminho para o arquivo `.trace` contendo a sequência de acessos.
* `--verbose`: *(Opcional)* Exibe o estado detalhado dos frames a cada passo da simulação.

### Exemplos de Uso

**1. Execução padrão (LRU com 3 frames):**
```bash
python3 pager.py --algo lru --frames 3 --trace traces/silberschatz2001.trace
```

**2. Execução passo a passo (Modo Verbose):**
```bash
python3 pager.py --algo lru --frames 3 --trace traces/silberschatz2001.trace --verbose
```

**3. Testando acessos de escrita (NRU com 3 frames):**
```bash
python3 pager.py --algo nru --frames 3 --trace traces/escritas.trace
```

---

## Validação e Testes

Para verificar automaticamente todos os algoritmos nos traços oficiais (`silberschatz2001.trace`, `belady.trace` e `escritas.trace`) e conferir os resultados:

```bash
python3 test_runner.py
```

---

## Divisão da Equipe