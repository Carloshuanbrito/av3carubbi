# Kattis - Treehouses

## Problema

**Nome:** Kattis - Treehouses

**Link:** <https://open.kattis.com/problems/treehouses>

## Integrantes do grupo

- LUCAS DE VASCONCELOS BARREIRA CARVALHO
- JOSÉ EUGÊNIO DE PAIVA NETO
- CARLOS HUAN CELESTINO DE BRITO
- MATEUS ROCHA LESSA

## Linguagem utilizada

Python 3.

## Como executar a solução

Na pasta raiz do projeto `T1`, execute:

```bash
python src/main.py
```

Depois, digite ou cole a entrada no terminal.

Para executar usando um arquivo de entrada no PowerShell:

```powershell
Get-Content dados\ex1 | python src\main.py
Get-Content dados\ex2 | python src\main.py
Get-Content dados\ex3 | python src\main.py
```

Também é possível executar a partir da pasta anterior:

```powershell
Get-Content T1\dados\ex1 | python T1\src\main.py
```

## Explicação da modelagem

O problema foi modelado como uma Árvore Geradora Mínima (MST). Cada casa na árvore é representada como um vértice do grafo.

As primeiras `K` casas já possuem acesso fácil à terra aberta. Portanto, elas podem ser consideradas previamente conectadas entre si com custo zero. Além disso, os cabos já existentes também são conexões de custo zero.

Para todos os outros pares de casas, consideramos a possibilidade de instalar um novo cabo. O custo desse cabo é a distância euclidiana entre as coordenadas das duas casas:

```text
distancia = sqrt((x1 - x2)^2 + (y1 - y2)^2)
```

Assim, a resposta é o menor custo adicional necessário para que todas as casas fiquem conectadas ao mesmo componente.

## Algoritmo utilizado

Foi utilizado o algoritmo de Kruskal com a estrutura Union-Find.

Etapas:

1. Criar uma estrutura Union-Find com `N` casas.
2. Unir as primeiras `K` casas com custo zero.
3. Unir todas as casas que já possuem cabos existentes, também com custo zero.
4. Gerar todas as arestas possíveis entre pares de casas, usando a distância euclidiana como peso.
5. Ordenar as arestas pelo peso.
6. Aplicar Kruskal: sempre que uma aresta conectar dois componentes diferentes, ela é escolhida e seu peso é somado à resposta.

## Análise de complexidade

O grafo completo possui:

```text
N * (N - 1) / 2
```

arestas possíveis.

- Geração das arestas: `O(N^2)`
- Ordenação das arestas: `O(N^2 log N)`
- Operações de Union-Find: praticamente `O(N^2)`, usando compressão de caminho e união por rank

Complexidade total:

```text
O(N^2 log N)
```

## Comprovante de Accepted

O comprovante deve estar no arquivo:

[evidencias/accepted.pdf](evidencias/accepted.pdf)

Esse arquivo pode ser substituído pelo print ou PDF real do Accepted no Kattis após o envio da solução.
