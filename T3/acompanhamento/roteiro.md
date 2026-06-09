# Ficha de Acompanhamento - CSES School Dance

## 1. Resumo do problema em linguagem propria

O problema pede o maior numero possivel de pares de danca entre meninos e meninas.

Cada par informado na entrada indica que aquele menino e aquela menina aceitam dancar juntos. Cada pessoa pode participar de no maximo um par.

## 2. Interpretacao da entrada e da saida

A entrada possui `n`, `m` e `k`:

- `n`: quantidade de meninos;
- `m`: quantidade de meninas;
- `k`: quantidade de pares possiveis.

Depois aparecem `k` linhas no formato `a b`, indicando que o menino `a` pode formar par com a menina `b`.

A saida imprime primeiro a quantidade maxima de pares. Em seguida, imprime os pares escolhidos.

## 3. Modelagem da rede de fluxo

A rede foi montada assim:

```text
S -> meninos -> meninas -> T
```

As arestas sao:

- `S -> menino`, com capacidade `1`;
- `menino -> menina`, com capacidade `1`, quando o par existe;
- `menina -> T`, com capacidade `1`.

Como as capacidades sao `1`, cada menino e cada menina so podem aparecer em um par.

## 4. Justificativa da escolha entre Ford-Fulkerson e Edmonds-Karp

O problema pode ser resolvido com Ford-Fulkerson, pois ele busca fluxo maximo.

Foi escolhido Edmonds-Karp porque ele e uma versao do Ford-Fulkerson que usa BFS para encontrar caminhos aumentantes. Isso deixa o processo mais organizado e previsivel.

## 5. Instancia pequena

Entrada usada:

```text
3 2 4
1 1
1 2
2 1
3 1
```

Existem 3 meninos, 2 meninas e 4 pares possiveis.

## 6. Execucao manual passo a passo

Um primeiro caminho possivel e:

```text
S -> menino 1 -> menina 1 -> T
```

Isso forma 1 par.

Depois, usando o grafo residual, o algoritmo pode reorganizar a escolha e obter:

```text
menino 1 -> menina 2
menino 3 -> menina 1
```

Assim, o fluxo total passa a ser `2`.

## 7. Verificacao da resposta final

Uma saida possivel e:

```text
2
1 2
3 1
```

A resposta e valida porque:

- foram formados 2 pares;
- nenhum menino se repete;
- nenhuma menina se repete;
- todos os pares escolhidos existem na entrada.

Nao e possivel formar 3 pares, pois existem apenas 2 meninas.
