# CSES School Dance - Fluxo Máximo em Rede

## 1. Problema em linguagem simples

O problema **School Dance** pede para formar o maior número possível de pares de dança entre meninos e meninas.

Temos:

- `n` meninos;
- `m` meninas;
- `k` pares possíveis.

Cada par possível indica que um menino e uma menina aceitam dançar juntos. Porém:

- cada menino pode dançar com no máximo uma menina;
- cada menina pode dançar com no máximo um menino.

O objetivo é escolher a maior quantidade possível de pares válidos.

Esse problema é um caso clássico de **emparelhamento bipartido máximo**, que pode ser resolvido por **fluxo máximo em rede**.

## 2. Modelagem como rede de fluxo

Construímos um grafo direcionado com capacidades:

- criamos uma origem `S`;
- criamos um vértice para cada menino;
- criamos um vértice para cada menina;
- criamos um sorvedouro `T`;
- ligamos `S` a cada menino com capacidade `1`;
- ligamos cada menina a `T` com capacidade `1`;
- para cada par possível menino-menina, criamos uma aresta do menino para a menina com capacidade `1`.

Visualmente:

```text
S -> meninos -> meninas -> T
```

Com capacidades:

```text
S -> menino: capacidade 1
menino -> menina: capacidade 1, se o par for permitido
menina -> T: capacidade 1
```

## 3. Por que uma unidade de fluxo representa um par válido?

Um caminho aumentante completo tem a forma:

```text
S -> menino i -> menina j -> T
```

Se uma unidade de fluxo passa por esse caminho, isso significa que o menino `i` foi pareado com a menina `j`.

Como a aresta `menino i -> menina j` só existe quando esse par é permitido na entrada, toda unidade de fluxo escolhida representa um par de dança válido.

## 4. Por que ninguém aparece em mais de um par?

As capacidades são todas unitárias nas arestas que controlam a participação:

- `S -> menino` tem capacidade `1`, então cada menino só pode receber uma unidade de fluxo;
- `menina -> T` tem capacidade `1`, então cada menina só pode enviar uma unidade de fluxo ao sorvedouro.

Assim, mesmo que um menino aceite dançar com várias meninas, apenas uma dessas opções pode ser usada no fluxo final. O mesmo vale para cada menina.

## 5. Algoritmo Edmonds-Karp

Usamos o algoritmo **Edmonds-Karp**, uma versão do Ford-Fulkerson que sempre usa **BFS** para encontrar caminhos aumentantes no grafo residual.

A ideia é:

1. começar com fluxo `0`;
2. procurar, por BFS, um caminho de `S` até `T` com capacidade residual positiva;
3. aumentar o fluxo nesse caminho;
4. atualizar as capacidades residuais;
5. repetir até não existir mais caminho aumentante.

Quando não há mais caminho de `S` até `T`, o fluxo atual é máximo.

## 6. Grafo residual e arestas reversas

O **grafo residual** mostra quanto fluxo ainda pode passar por cada aresta.

Se uma aresta `u -> v` tem capacidade restante, ela pode ser usada em um novo caminho aumentante.

As **arestas reversas** `v -> u` permitem desfazer ou redirecionar parte do fluxo já escolhido. Isso é essencial porque uma escolha inicial pode impedir uma combinação melhor depois.

Exemplo de ideia:

- primeiro escolhemos `menino 1 -> menina 1`;
- depois percebemos que seria melhor mandar o `menino 1` para outra menina;
- a aresta reversa permite cancelar o fluxo anterior e reorganizar os pares.

## 7. Recuperação dos pares escolhidos

Depois de calcular o fluxo máximo, verificamos as arestas originais de menino para menina.

Se uma aresta original `menino i -> menina j` ficou com fluxo igual a `1`, então o par `(i, j)` foi escolhido.

Na implementação, isso é identificado quando a aresta original ficou com capacidade residual `0`, pois sua capacidade inicial era `1`.

## 8. Implementação em Python

Arquivo principal: [`src/main.py`](src/main.py)

```python
from collections import deque
import sys


class Edge:
    def __init__(self, to, rev, capacity):
        self.to = to
        self.rev = rev
        self.capacity = capacity
        self.original_capacity = capacity


def add_edge(graph, u, v, capacity):
    forward = Edge(v, len(graph[v]), capacity)
    backward = Edge(u, len(graph[u]), 0)
    graph[u].append(forward)
    graph[v].append(backward)
    return len(graph[u]) - 1


def bfs(graph, source, sink, parent):
    for i in range(len(parent)):
        parent[i] = None

    queue = deque([source])
    parent[source] = (-1, -1)

    while queue:
        u = queue.popleft()

        for edge_index, edge in enumerate(graph[u]):
            if parent[edge.to] is None and edge.capacity > 0:
                parent[edge.to] = (u, edge_index)
                if edge.to == sink:
                    return True
                queue.append(edge.to)

    return False


def edmonds_karp(graph, source, sink):
    flow = 0
    parent = [None] * len(graph)

    while bfs(graph, source, sink, parent):
        path_flow = 10**18
        current = sink

        while current != source:
            previous, edge_index = parent[current]
            path_flow = min(path_flow, graph[previous][edge_index].capacity)
            current = previous

        current = sink

        while current != source:
            previous, edge_index = parent[current]
            edge = graph[previous][edge_index]
            reverse_edge = graph[edge.to][edge.rev]

            edge.capacity -= path_flow
            reverse_edge.capacity += path_flow

            current = previous

        flow += path_flow

    return flow


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    iterator = iter(data)
    n = int(next(iterator))
    m = int(next(iterator))
    k = int(next(iterator))

    source = 0
    boys_start = 1
    girls_start = boys_start + n
    sink = girls_start + m
    total_vertices = sink + 1

    graph = [[] for _ in range(total_vertices)]
    pair_edges = []

    for boy in range(1, n + 1):
        add_edge(graph, source, boys_start + boy - 1, 1)

    for girl in range(1, m + 1):
        add_edge(graph, girls_start + girl - 1, sink, 1)

    for _ in range(k):
        boy = int(next(iterator))
        girl = int(next(iterator))
        boy_vertex = boys_start + boy - 1
        girl_vertex = girls_start + girl - 1
        edge_index = add_edge(graph, boy_vertex, girl_vertex, 1)
        pair_edges.append((boy, girl, boy_vertex, edge_index))

    maximum_pairs = edmonds_karp(graph, source, sink)

    chosen_pairs = []
    for boy, girl, boy_vertex, edge_index in pair_edges:
        edge = graph[boy_vertex][edge_index]
        if edge.original_capacity == 1 and edge.capacity == 0:
            chosen_pairs.append((boy, girl))

    output = [str(maximum_pairs)]
    output.extend(f"{boy} {girl}" for boy, girl in chosen_pairs)
    print("\n".join(output))


if __name__ == "__main__":
    main()
```

## 9. Uso de `collections.deque`

A BFS usa `collections.deque`, pois ela permite inserir no fim e remover do início da fila em tempo constante.

Isso é adequado para a busca em largura do Edmonds-Karp.

## 10. Limites do problema

O algoritmo funciona dentro dos limites:

- `1 <= n, m <= 500`;
- `1 <= k <= 1000`.

O número de vértices é:

```text
V = n + m + 2
```

O número de arestas principais é:

```text
E = n + m + k
```

Como `n` e `m` são no máximo `500`, e `k` é no máximo `1000`, a rede é pequena o suficiente para Edmonds-Karp.

## 11. Formato da saída

A saída imprime:

1. a quantidade máxima de pares;
2. cada par escolhido, um por linha.

Exemplo de formato:

```text
2
1 2
3 1
```

## 12. Análise de complexidade

No Edmonds-Karp, a complexidade geral é:

```text
O(V * E^2)
```

Para este problema, como todas as capacidades são `1`, cada aumento adiciona exatamente uma unidade de fluxo. O fluxo máximo é no máximo:

```text
min(n, m)
```

Assim, uma forma prática de analisar esta implementação é:

```text
O(F * E)
```

onde:

- `F` é o valor do fluxo máximo;
- `E` é o número de arestas da rede residual.

Como `F <= 500` e `E` é proporcional a `n + m + k`, a solução passa confortavelmente nos limites do CSES.

## 13. Explicação manual do exemplo

Entrada:

```text
3 2 4
1 1
1 2
2 1
3 1
```

Temos:

- 3 meninos;
- 2 meninas;
- 4 pares possíveis.

Pares possíveis:

- menino 1 com menina 1;
- menino 1 com menina 2;
- menino 2 com menina 1;
- menino 3 com menina 1.

Como existem apenas 2 meninas, a resposta nunca pode ser maior que 2.

Uma solução ótima é:

- menino 1 com menina 2;
- menino 3 com menina 1.

Saída possível:

```text
2
1 2
3 1
```

Também poderiam existir outras saídas corretas com 2 pares, dependendo dos caminhos aumentantes encontrados, desde que nenhum menino ou menina se repita.

## Resumo para apresentação de até 5 minutos

1. O problema pede o maior conjunto de pares menino-menina sem repetir pessoas.
2. Modelamos como fluxo máximo: `S -> meninos -> meninas -> T`.
3. Todas as capacidades são `1`, garantindo que cada pessoa participe de no máximo um par.
4. Cada unidade de fluxo representa um par de dança válido.
5. Usamos Edmonds-Karp com BFS para encontrar caminhos aumentantes no grafo residual.
6. As arestas reversas permitem reorganizar escolhas anteriores.
7. Depois do fluxo máximo, recuperamos os pares olhando as arestas menino-menina que receberam fluxo.
