import random
import time
import statistics


class Grafo:
    def __init__(self, n):
        self.n = n
        self.m = 0

    def adicionar_aresta(self, u, v):
        pass

    def grau(self, v):
        pass

    def vizinhos(self, v):
        pass


class GrafoMatriz(Grafo):
    def __init__(self, n):
        super().__init__(n)
        self.matriz = [[0] * n for _ in range(n)]

    def tem_aresta(self, u, v):
        return self.matriz[u][v] == 1

    def adicionar_aresta(self, u, v):
        if self.matriz[u][v] == 0:
            self.matriz[u][v] = 1
            self.matriz[v][u] = 1
            self.m += 1

    def grau(self, v):
        return sum(self.matriz[v])

    def vizinhos(self, v):
        return [i for i, val in enumerate(self.matriz[v]) if val == 1]

    def espaco(self):
        return self.n ** 2


class GrafoLista(Grafo):
    def __init__(self, n):
        super().__init__(n)
        self.lista = [[] for _ in range(n)]

    def tem_aresta(self, u, v):
        return v in self.lista[u]

    def adicionar_aresta(self, u, v):
        if v not in self.lista[u]:
            self.lista[u].append(v)
            self.lista[v].append(u)
            self.m += 1

    def grau(self, v):
        return len(self.lista[v])

    def vizinhos(self, v):
        return self.lista[v]

    def espaco(self):
        return self.n + 2 * self.m


def contar_triangulos(grafo):
    triangulos = 0
    n = grafo.n
    for u in range(n):
        for v in grafo.vizinhos(u):
            if u < v:
                for w in grafo.vizinhos(v):
                    if v < w and grafo.tem_aresta(u, w):
                        triangulos += 1
    return triangulos


def teste_figura_3_1(tipo_grafo):
    g = tipo_grafo(6)
    arestas = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (2, 5), (3, 4)]
    for u, v in arestas:
        g.adicionar_aresta(u, v)

    n_correto = (g.n == 6)
    m_correto = (g.m == 8)

    graus = sorted([g.grau(i) for i in range(g.n)], reverse=True)
    seq_correta = (graus == [4, 3, 3, 3, 2, 1])
    soma_correta = (sum(graus) == 2 * g.m)

    return n_correto and m_correto and seq_correta and soma_correta


def medir_efeito_representacao():
    n = 2000
    densidades = [0.001, 0.05, 0.5]
    random.seed(42)

    tabela = []

    for rho in densidades:
        g_matriz = GrafoMatriz(n)
        g_lista = GrafoLista(n)

        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < rho:
                    g_matriz.adicionar_aresta(u, v)
                    g_lista.adicionar_aresta(u, v)
        tempos_matriz = []
        for _ in range(3):
            inicio = time.perf_counter()
            contar_triangulos(g_matriz)
            tempos_matriz.append(time.perf_counter() - inicio)
        mediana_matriz = statistics.median(tempos_matriz)
        tempos_lista = []
        for _ in range(3):
            inicio = time.perf_counter()
            contar_triangulos(g_lista)
            tempos_lista.append(time.perf_counter() - inicio)
        mediana_lista = statistics.median(tempos_lista)

        tabela.append({
            'densidade': rho,
            'esp_mat': g_matriz.espaco(),
            'tem_mat': mediana_matriz,
            'esp_lis': g_lista.espaco(),
            'tem_lis': mediana_lista
        })

    print(
        f"| {'Densidade':<9} | {'Espaço Matriz':<13} | {'Tempo Matriz (s)':<16} | {'Espaço Lista':<12} | {'Tempo Lista (s)':<15} |")
    print("|" + "-" * 11 + "|" + "-" * 15 + "|" + "-" * 18 + "|" + "-" * 14 + "|" + "-" * 17 + "|")
    for r in tabela:
        print(
            f"| {r['densidade']:<9} | {r['esp_mat']:<13} | {r['tem_mat']:<16.5f} | {r['esp_lis']:<12} | {r['tem_lis']:<15.5f} |")


if __name__ == '__main__':
    print("Verificando ITEM 2 (Testes da sequência de graus):")
    print(" - GrafoMatriz:", "Aprovado" if teste_figura_3_1(GrafoMatriz) else "Falhou")
    print(" - GrafoLista:", "Aprovado" if teste_figura_3_1(GrafoLista) else "Falhou")
    print("\nExecutando ITEM 4 e 5 (Medições - Isto irá demorar alguns minutos):")
    medir_efeito_representacao()
