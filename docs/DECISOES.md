# Decisões de Arquitetura e Contrato de Implementação

Este documento define a arquitetura, as estruturas de dados e as regras de negócio do simulador. Ele serve tanto como **guia de contrato técnico** para o desenvolvimento paralelo da equipe quanto como **documentação de projeto**.

---

## 1. Arquitetura e Padrões de Projeto

Para isolar o motor de simulação das regras específicas de cada política de substituição, adotou-se o padrão comportamental **Strategy**:

* **Contexto (`src/engine.py`):** Gerencia o ciclo de vida da simulação (alocação inicial em frames livres, detecção de *hits* e *faults*, contagem de evicções/escritas em disco e formatação de saída). O motor não conhece a lógica interna de nenhum algoritmo.
* **Estratégia Abstrata (`AlgoritmoSubstituicao` em `src/models.py`):** Define a interface única que todas as políticas devem implementar.
* **Estratégias Concretas (`src/algs_basicos.py` e `src/algs_avancados.py`):** Implementam os 7 algoritmos de forma desacoplada, manipulando apenas os metadados expostos na estrutura `Frame`.

---

## 2. Estruturas de Dados (`src/models.py`)

As estruturas abaixo são imutáveis para os módulos de algoritmos.

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Referencia:
    pagina: int
    tipo: str  # 'R' (leitura) ou 'W' (escrita)

@dataclass
class Frame:
    id: int
    pagina: Optional[int] = None
    bit_r: int = 0
    bit_m: int = 0
    tempo_carga: int = 0      # Passo em que a página entrou na memória
    ultimo_acesso: int = 0    # Passo do acesso mais recente (hit ou carga)
    contador_uso: int = 0     # Contador de referências desde a carga
```

### Interface Obrigatória dos Algoritmos

```python
class AlgoritmoSubstituicao:
    def __init__(self, num_frames: int, trace_completo: List[Referencia]):
        self.num_frames = num_frames
        self.trace_completo = trace_completo

    def ao_acessar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        """Executado em caso de HIT. Atualiza metadados do frame."""
        raise NotImplementedError

    def ao_carregar(self, frame: Frame, passo: int, ref: Referencia) -> None:
        """Executado em caso de FAULT ao inserir nova página no frame."""
        raise NotImplementedError

    def selecionar_vitima(self, frames: List[Frame], passo_atual: int) -> int:
        """Retorna o frame.id da página escolhida para remoção."""
        raise NotImplementedError

    def pos_passo(self, frames: List[Frame], passo: int) -> None:
        """Hook executado ao final de cada referência (opcional)."""
        pass
```

---

## 3. Regras de Simulação e Contratos de Negócio

Para garantir determinismo e conformidade com o enunciado, todas as implementações seguem rigorosamente estas diretrizes:

1. **Preenchimento Inicial:** Enquanto houver frames vazios (`frame.pagina is None`), o motor aloca a nova página no frame vazio de **menor `id`**. O método `selecionar_vitima` só é invocado quando todos os frames estiverem ocupados.
2. **Critério Universal de Desempate:** Em **todos** os algoritmos, caso duas ou mais páginas empatem no critério de remoção, remove-se obrigatoriamente aquela residente há mais tempo (menor valor de `frame.tempo_carga`).
3. **Persistência do Bit Modificado (`bit_m`):**
   * Quando uma página é carregada com acesso `W`, inicia com `bit_m = 1`.
   * Se sofrer um *hit* de escrita (`W`), `bit_m` passa para `1`.
   * Se sofrer um *hit* de leitura (`R`), `bit_m` mantém seu estado anterior (se já era `1`, permanece `1`).
   * Ao ser removida (evicção), se `bit_m == 1`, incrementa-se a métrica de **escritas em disco** e os metadados do frame são reiniciados para a nova página.
4. **Especificidades por Algoritmo:**
   * **FIFO:** Remove o frame com menor `tempo_carga`.
   * **LRU:** Atualiza `ultimo_acesso = passo` na carga e nos acessos; remove o frame com menor `ultimo_acesso`.
   * **Ótimo (`opt`):** Consulta `self.trace_completo[passo_atual:]` para encontrar o índice da próxima ocorrência de cada página residente. Páginas sem acessos futuros recebem distância infinita ($\infty$) e têm prioridade de remoção.
   * **Clock:** Mantém um ponteiro interno iniciado em `0`, que só se move durante evicções. Ao buscar vítima, zera `bit_r` dos frames com `bit_r == 1` e avança circularmente (`(ptr + 1) % num_frames`) até encontrar `bit_r == 0`. Após substituir, o ponteiro avança uma posição.
   * **NRU:** Define `bit_r = 1` em todo acesso/carga. Ao final de cada 4 referências (`passo % 4 == 0`), zera `bit_r` de todos os frames residentes via `pos_passo`. Calcula a classe via $2 \times \text{bit\_r} + \text{bit\_m}$ e remove a página da menor classe.
   * **LFU / MFU:** Inicia `contador_uso = 1` em `ao_carregar` e incrementa `+1` em `ao_acessar`. LFU remove o menor `contador_uso`; MFU remove o maior `contador_uso`.

---

## 4. Análise Experimental (A preencher após execução dos testes)


### Comparativo de Faltas de Página
| Algoritmo | Silberschatz (3 frames) | Silberschatz (4 frames) | Belady (3 frames) | Belady (4 frames) | Apresenta Anomalia de Belady? |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **FIFO** | 15 | 10 | 9 | 10 | Sim |
| **LRU** | 12 | 8 | 10 | 8 | Não |
| **Ótimo** | 9 | 8 | 7 | 6 | Não |
| **Clock** | 14 | 9 | *Rodar* | *Rodar* | *Analisar* |
| **NRU** | 10 | 9 | *Rodar* | *Rodar* | *Analisar* |
| **LFU** | 13 | 9 | *Rodar* | *Rodar* | *Analisar* |
| **MFU** | 15 | 12 | *Rodar* | *Rodar* | *Analisar* |

### Explicação da Anomalia de Belady
*(Espaço reservado para explicar por que algoritmos sem a propriedade de inclusão/pilha — como FIFO e potencialmente variações de frequência/segunda chance — podem sofrer aumento no número de faltas de página ao expandir a memória física de 3 para 4 frames, enquanto algoritmos de pilha como LRU e Ótimo garantem que o conjunto residente de $N$ frames é sempre um subconjunto do conjunto residente de $N+1$ frames).*