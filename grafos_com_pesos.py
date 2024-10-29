from heapq import heappop, heappush
from collections import deque, defaultdict
import time

from grafos import *

class GrafoComPesos(Grafo):
    def __init__(self, arquivo):
        super().__init__(None)
        self.arestas = []
        self.vertices = 0
        with open(arquivo, "r") as f:
            self.vertices = int(f.readline())
            for linha in f:
                if '-' in linha:
                    print("Não implementamos grafos com pesos negativos ainda.")
                v1, v2, peso = linha.split()
                self.arestas.append((int(v1) - 1, int(v2) - 1, float(peso)))

    def matriz_adjacencia(self):
        self.matriz = lil_matrix((self.vertices, self.vertices), dtype=float)
        for v1, v2, peso in self.arestas:
            self.matriz[v1, v2] = peso
            self.matriz[v2, v1] = peso
        self.matriz = self.matriz.tocsr()

    def lista_adjacencia(self):
        self.adjacencia = defaultdict(list)
        for u, v, peso in self.arestas:
            self.adjacencia[u].append((v, peso))
            self.adjacencia[v].append((u, peso))

    def dijkstra_vetor(self, inicio):
        inicio -= 1
        distancias = [float('inf')] * self.vertices
        distancias[inicio] = 0
        visitados = [False] * self.vertices
        pais = [None] * self.vertices
        for _ in range(self.vertices):
            min_dist = float('inf')
            u = -1
            for i in range(self.vertices):
                if not visitados[i] and distancias[i] < min_dist:
                    min_dist = distancias[i]
                    u = i
            if u == -1: break
            visitados[u] = True
            for vizinho, peso in self.adjacencia[u]:
                if distancias[u] + peso < distancias[vizinho]:
                    distancias[vizinho] = distancias[u] + peso
                    pais[vizinho] = u
        return distancias, pais

    def dijkstra_heap(self, inicio):
        inicio -= 1
        distancias = [float('inf')] * self.vertices
        distancias[inicio] = 0
        heap = [(0, inicio)]
        pais = [None] * self.vertices
        while heap:
            dist_u, u = heappop(heap)
            if dist_u > distancias[u]:
                continue
            for vizinho, peso in self.adjacencia[u]:
                if distancias[u] + peso < distancias[vizinho]:
                    distancias[vizinho] = distancias[u] + peso
                    heappush(heap, (distancias[vizinho], vizinho))
                    pais[vizinho] = u
        return distancias, pais

    def obter_caminho(self, pais, destino):
        caminho = []
        atual = destino - 1
        while atual is not None:
            caminho.append(atual+1)
            atual = pais[atual]
        return caminho[::-1]

    def tempo_medio_dijkstra(self, k=100):
        import random
        tempos_vetor = []
        tempos_heap = []
        vertices_aleatorios = random.sample(range(self.vertices), k)
        for v in vertices_aleatorios:
            inicio = time.perf_counter()
            self.dijkstra_vetor(v)
            tempos_vetor.append(time.perf_counter() - inicio)

            inicio = time.perf_counter()
            self.dijkstra_heap(v)
            tempos_heap.append(time.perf_counter() - inicio)

        tempo_medio_vetor = sum(tempos_vetor) / k
        tempo_medio_heap = sum(tempos_heap) / k
        return tempo_medio_vetor, tempo_medio_heap

    def calcular_distancias_entre_pesquisadores(self, inicio, fim):
        mapa_pesquisadores = {
            "Edsger W. Dijkstra": 2722,  # Ajuste o índice conforme necessário
            "Alan M. Turing": 11365,
            "J. B. Kruskal": 471365,
            "Jon M. Kleinberg": 5709,
            "Éva Tardos": 11386,
            "Daniel R. Figueiredo": 343930
        }
        inicio_idx = mapa_pesquisadores.get(inicio)
        fim_idx = mapa_pesquisadores.get(fim)
        if inicio_idx is None or fim_idx is None:
            return None
        dijkstra = self.dijkstra_heap(inicio_idx)
        return dijkstra[0][fim_idx-1], self.obter_caminho(dijkstra[1], fim_idx)
