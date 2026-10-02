# Teoria-dos-Grafos

# Atividade 3.16: Medir o efeito da representação

**Repositório de Código:** https://github.com/Hemillio/Teoria-dos-Grafos

## 1. Tabela de Medição (Item 5)

Os testes foram executados com $n = 2000$ vértices, reportando a mediana de 3 execuções para o tempo.

| Densidade | Espaço Matriz | Tempo Matriz (s) | Espaço Lista | Tempo Lista (s) |
|-----------|---------------|------------------|--------------|-----------------|
| 0.001     | 4000000       | 0.24477          | 5820         | 0.00050         |
| 0.05      | 4000000       | 6.35885          | 202524       | 2.22499         |
| 0.5       | 4000000       | 118.12041        | 1999540      | 1804.95299      |

## 2. Discussão dos Resultados (Item 6)

**Qual implementação foi mais rápida em cada densidade, e porquê?**
* **Para densidades baixas (0.001 e 0.05):** A Lista de Adjacência foi significativamente mais rápida (0.00050s na lista contra 0.24477s na matriz para $\rho = 0.001$). Isso ocorre porque, em grafos esparsos, a lista itera apenas pelos poucos vizinhos existentes, enquanto a matriz perde tempo verificando muitos "zeros" (ausência de arestas) em suas linhas.
* **Para a densidade alta (0.5):** A Matriz de Adjacência foi brutalmente mais rápida (118s contra mais de 1800s da lista). Isso acontece porque o algoritmo de contar triângulos faz muitas verificações de existência de aresta cruzada (`tem_aresta(u, w)`). Na matriz, essa consulta tem custo $\Theta(1)$ (direto na posição de memória), enquanto na lista o custo é $\Theta(d(u))$, obrigando o programa a percorrer listas gigantescas milhares de vezes.

**A ordem entre elas muda conforme a densidade cresce?**
Sim. A Lista de Adjacência começa sendo a mais rápida nas densidades 0.001 e 0.05. No entanto, quando a densidade chega a 0.5, a ordem inverte-se drasticamente, e a Matriz passa a ser cerca de 15 vezes mais rápida que a Lista.

**O que vocês mediram concorda com o custo composto para `contar_triangulos`?**
Sim, os resultados concordam perfeitamente com a teoria. 
* No quesito **espaço**, a matriz manteve-se fixa em $4.000.000$ posições ($n^2$), enquanto a lista cresceu proporcionalmente às arestas $\Theta(n + 2m)$, saltando de 5.820 para quase 2 milhões de posições, mas sempre economizando espaço em relação à matriz.
* No quesito **tempo**, a limitação da lista para descobrir rapidamente se "u é vizinho de w" em listas grandes gerou o gargalo esperado para grafos densos, comprovando o peso da complexidade teórica composta.
