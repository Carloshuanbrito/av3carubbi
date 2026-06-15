# Ficha de Acompanhamento - CSES School Dance

## 1. Contexto do problema e objetivo

O problema pede o maior numero possivel de pares de danca entre meninos e meninas.

Cada par informado na entrada indica que aquele menino e aquela menina aceitam dancar juntos. Cada pessoa pode participar de no maximo um par.

Portanto, a quantidade que deve ser maximizada e o numero de pares validos escolhidos.

Esse problema pode ser visto como um emparelhamento bipartido maximo e sera resolvido como fluxo maximo em rede.

## 2. Interpretacao da entrada e da saida

A entrada possui `n`, `m` e `k`:

- `n`: quantidade de meninos;
- `m`: quantidade de meninas;
- `k`: quantidade de pares possiveis.

Depois aparecem `k` linhas no formato `a b`, indicando que o menino `a` pode formar par com a menina `b`.

A saida imprime primeiro a quantidade maxima de pares. Em seguida, imprime os pares escolhidos.

## 3. Vertices e camadas da rede

A rede foi montada em quatro camadas:

```text
S -> meninos -> meninas -> T
```

Cada grupo de vertices tem um significado:

- `S`: origem do fluxo;
- meninos: cada vertice representa um menino;
- meninas: cada vertice representa uma menina;
- `T`: sorvedouro do fluxo.

A origem `S` representa o inicio das escolhas de pareamento. O sorvedouro `T` representa o fim de uma escolha completa.

Chegar em `T` significa que foi formado um caminho completo:

```text
S -> menino -> menina -> T
```

Esse caminho representa um par de danca valido.

## 4. Arestas direcionadas e capacidades

As arestas sao:

- `S -> menino`, com capacidade `1`;
- `menino -> menina`, com capacidade `1`, quando o par existe na entrada;
- `menina -> T`, com capacidade `1`.

A aresta `S -> menino` limita cada menino a participar de no maximo um par.

A aresta `menino -> menina` representa uma permissao de pareamento. Ela so existe se o enunciado informou que aquele menino e aquela menina podem dancar juntos.

A aresta `menina -> T` limita cada menina a participar de no maximo um par.

Todas as capacidades usadas sao unitarias porque cada pessoa e cada par permitido podem ser usados no maximo uma vez.

Neste problema nao e necessario usar capacidade infinita, porque nao existe uma passagem sem limite. Tambem nao existe capacidade igual a uma quantidade maior do enunciado, pois as restricoes importantes sao todas do tipo "no maximo um".

## 5. Conversao completa para fluxo maximo

A conversao do enunciado para rede de fluxo fica assim:

1. Criar uma origem `S`.
2. Criar um vertice para cada menino.
3. Criar um vertice para cada menina.
4. Criar um sorvedouro `T`.
5. Ligar `S` a cada menino com capacidade `1`.
6. Ligar cada menina a `T` com capacidade `1`.
7. Para cada par possivel da entrada, ligar o menino correspondente a menina correspondente com capacidade `1`.

O valor do fluxo representa a resposta porque cada unidade de fluxo passa por exatamente um menino e uma menina, formando um par valido.

Como as capacidades de `S -> menino` e `menina -> T` sao `1`, nenhum menino e nenhuma menina pode aparecer em mais de um par.

## 6. Algoritmo usado: Ford-Fulkerson

O problema sera resolvido somente com o algoritmo de Ford-Fulkerson.

Ford-Fulkerson calcula fluxo maximo procurando caminhos aumentantes no grafo residual. Nesta implementacao, a busca por caminho aumentante e feita por DFS, ou seja, uma busca em profundidade simples.

A diferenca para Edmonds-Karp e que Edmonds-Karp escolhe os caminhos aumentantes usando BFS. Aqui nao usamos Edmonds-Karp; usamos Ford-Fulkerson com DFS.

## 7. Grafo residual, gargalo e arestas reversas

A capacidade residual indica quanto fluxo ainda pode passar por uma aresta.

Depois que um caminho aumentante e escolhido, o grafo residual muda:

- a capacidade das arestas usadas diminui;
- a capacidade das arestas reversas aumenta.

O gargalo do caminho aumentante e a menor capacidade residual entre as arestas do caminho.

Neste problema, como todas as capacidades sao `1`, o gargalo de qualquer caminho completo tambem e `1`.

As arestas reversas permitem corrigir escolhas anteriores. Por exemplo, se inicialmente o algoritmo escolhe `menino 1 -> menina 1`, depois ele pode usar o residual para desfazer ou reorganizar essa escolha e conseguir uma solucao melhor.

## 8. Condicao de parada e otimalidade

O Ford-Fulkerson para quando nao existe mais caminho de `S` ate `T` com capacidade residual positiva.

Nesse momento, nao ha como aumentar o numero de pares. Pelo teorema do fluxo maximo e corte minimo, o fluxo encontrado e maximo.

Assim, a estrategia encontra uma solucao otima para o emparelhamento.

## 9. Recuperacao dos pares escolhidos

Depois de calcular o fluxo maximo, a resposta e reconstruida olhando as arestas originais de menino para menina.

Se uma aresta `menino -> menina` ficou com capacidade residual `0`, significa que passou uma unidade de fluxo por ela.

Entao esse par foi escolhido e deve ser impresso na saida.

## 10. Complexidade e memoria

Sejam:

- `V = n + m + 2`, o numero de vertices;
- `E = n + m + k`, o numero de arestas principais;
- `F`, o valor do fluxo maximo.

No Ford-Fulkerson com DFS, cada busca por caminho aumentante custa `O(E)`.

Como cada aumento adiciona uma unidade de fluxo, a complexidade fica:

```text
O(F * E)
```

Neste problema, `F <= min(n, m)`, entao `F <= 500`.

A estrutura principal de memoria e a lista de adjacencia do grafo residual, que guarda as arestas normais e as arestas reversas. A memoria usada e `O(V + E)`.

## 11. Casos especiais aplicaveis

Os casos especiais importantes para este problema sao:

- se nao houver caminho de `S` ate `T`, o fluxo maximo sera `0`;
- se houver varios pares possiveis para a mesma pessoa, as capacidades unitarias impedem repeticao;
- se existirem multiplas arestas entre o mesmo menino e a mesma menina, elas podem aparecer na entrada como possibilidades repetidas, mas a capacidade dos vertices ainda limita cada pessoa a um unico par;
- nao ha varios casos de teste na entrada;
- nao e necessario usar infinito, pois todas as restricoes relevantes sao unitarias.

## 12. Instancia pequena

Entrada usada:

```text
3 2 4
1 1
1 2
2 1
3 1
```

Existem 3 meninos, 2 meninas e 4 pares possiveis.

Como existem apenas 2 meninas, a resposta nao pode ser maior que `2`.

## 13. Execucao manual passo a passo

Um primeiro caminho possivel e:

```text
S -> menino 1 -> menina 1 -> T
```

Isso forma 1 par.

Depois, usando o grafo residual de Ford-Fulkerson, o algoritmo pode encontrar outro caminho aumentante que reorganiza a escolha e obter:

```text
menino 1 -> menina 2
menino 3 -> menina 1
```

Assim, o fluxo total passa a ser `2`.

## 14. Verificacao da resposta final

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

## 15. Resumo para apresentacao

1. O objetivo e maximizar o numero de pares de danca validos.
2. A rede tem camadas `S -> meninos -> meninas -> T`.
3. A origem representa o inicio das escolhas e o sorvedouro representa completar um par.
4. As arestas indicam permissao de escolha e todas tem capacidade `1`.
5. Cada unidade de fluxo representa um par menino-menina.
6. Usamos Ford-Fulkerson com DFS para encontrar caminhos aumentantes.
7. O grafo residual e as arestas reversas permitem reorganizar escolhas.
8. O algoritmo para quando nao ha mais caminho aumentante.
9. Os pares finais sao recuperados pelas arestas menino-menina que receberam fluxo.
10. A complexidade e `O(F * E)` e a memoria e `O(V + E)`.
