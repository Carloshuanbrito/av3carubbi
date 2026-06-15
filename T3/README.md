# CSES School Dance - Fluxo Máximo em Rede

## Como executar

O arquivo principal da solução é:

```text
T3/src/main.py
```

Requisito:

- Python 3 instalado.

Para executar no PowerShell, a partir da raiz do repositório:

```powershell
python T3\src\main.py
```

Depois, cole a entrada do problema no terminal.

Também é possível executar usando um arquivo de entrada:

```powershell
Get-Content T3\dados\entradas_do_problema.txt | python T3\src\main.py
```

Em terminal Linux, macOS ou Git Bash:

```bash
python3 T3/src/main.py < T3/dados/entradas_do_problema.txt
```

Exemplo de entrada:

```text
3 2 4
1 1
1 2
2 1
3 1
```

Uma saída possível:

```text
2
1 2
3 1
```

## Abordagem resumida

O problema foi modelado como uma rede de fluxo para encontrar um emparelhamento bipartido máximo.

A rede usa quatro camadas:

```text
S -> meninos -> meninas -> T
```

Cada unidade de fluxo que sai da origem `S`, passa por um menino, passa por uma menina e chega ao sorvedouro `T` representa um par de dança válido.

Todas as capacidades são `1`, garantindo que cada menino e cada menina apareçam em no máximo um par.

O fluxo máximo é calculado com Ford-Fulkerson usando DFS para encontrar caminhos aumentantes no grafo residual. Depois do cálculo, os pares escolhidos são recuperados pelas arestas `menino -> menina` que receberam fluxo.

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

## 5. Algoritmo Ford-Fulkerson

Usamos somente o algoritmo **Ford-Fulkerson** para calcular o fluxo máximo.

Nesta implementação, cada caminho aumentante é encontrado com uma busca em profundidade no grafo residual.

A ideia é:

1. começar com fluxo `0`;
2. procurar um caminho de `S` até `T` com capacidade residual positiva;
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


def dfs(graph, source, sink, parent):
    for i in range(len(parent)):
        parent[i] = None

    visited = [False] * len(graph)
    stack = [source]
    visited[source] = True
    parent[source] = (-1, -1)

    while stack:
        u = stack.pop()

        for edge_index, edge in enumerate(graph[u]):
            if not visited[edge.to] and edge.capacity > 0:
                parent[edge.to] = (u, edge_index)
                if edge.to == sink:
                    return True
                visited[edge.to] = True
                stack.append(edge.to)

    return False


def ford_fulkerson(graph, source, sink):
    flow = 0
    parent = [None] * len(graph)

    while dfs(graph, source, sink, parent):
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

    maximum_pairs = ford_fulkerson(graph, source, sink)

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

## 9. Busca de caminhos aumentantes

A implementação usa uma pilha para fazer busca em profundidade no grafo residual.

Essa busca encontra um caminho aumentante qualquer de `S` até `T`, como previsto pelo Ford-Fulkerson.

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

Como `n` e `m` são no máximo `500`, e `k` é no máximo `1000`, a rede é pequena o suficiente para Ford-Fulkerson.

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

No Ford-Fulkerson, usando capacidades inteiras, o número de iterações depende do valor do fluxo máximo.

```text
O(F * E)
```

Para este problema, como todas as capacidades são `1`, cada aumento adiciona exatamente uma unidade de fluxo. O fluxo máximo é no máximo:

```text
min(n, m)
```

Assim, para esta implementação:

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
5. Usamos Ford-Fulkerson para encontrar caminhos aumentantes no grafo residual.
6. As arestas reversas permitem reorganizar escolhas anteriores.
7. Depois do fluxo máximo, recuperamos os pares olhando as arestas menino-menina que receberam fluxo.
