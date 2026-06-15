# Apresentação - CSES School Dance

## 1. Ideia do problema

O problema quer formar o maior número possível de pares entre meninos e meninas.

Cada par da entrada informa que aquele menino e aquela menina aceitam dançar juntos.

A restrição principal é que cada pessoa pode aparecer em no máximo um par.

## 2. Ideia da modelagem

Esse é um problema de emparelhamento bipartido.

Podemos transformar em fluxo máximo usando quatro camadas:

```text
S -> meninos -> meninas -> T
```

## 3. Capacidades

Usamos capacidade `1` em todas as arestas importantes:

- `S -> menino`: limita cada menino a um par;
- `menino -> menina`: representa um par permitido;
- `menina -> T`: limita cada menina a um par.

Assim, cada unidade de fluxo representa exatamente um par de dança válido.

## 4. Algoritmo usado

Foi usado Ford-Fulkerson.

Ele encontra caminhos aumentantes no grafo residual e aumenta o fluxo enquanto ainda existir caminho de `S` até `T`.

O algoritmo trabalha no grafo residual, que mostra onde ainda existe capacidade para passar mais fluxo.

As arestas reversas são importantes porque permitem desfazer ou reorganizar escolhas anteriores.

## 5. Recuperação da resposta

Depois do fluxo máximo, olhamos as arestas originais entre meninos e meninas.

Se uma dessas arestas recebeu fluxo `1`, então aquele par foi escolhido.

Primeiro imprimimos a quantidade máxima de pares e depois os pares.

## 6. Exemplo

Entrada:

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

Não é possível formar mais de 2 pares porque só existem 2 meninas.

## 7. Complexidade

No Ford-Fulkerson, como as capacidades são inteiras, o número de aumentos depende do valor do fluxo máximo.

```text
O(F * E)
```

Neste problema, como as capacidades são unitárias, o número de aumentos é no máximo `min(n, m)`.

Com `n, m <= 500` e `k <= 1000`, a solução funciona dentro dos limites.
