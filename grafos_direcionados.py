from grafos_com_pesos import *
from collections import defaultdict, deque
import time

class GrafoDirecionado(GrafoComPesos):
    def __init__(self, arquivo=None):
        super().__init__(arquivo)
        self.fluxo = defaultdict(float)  # Fluxos nas arestas
        self.capacidade_residual = defaultdict(lambda: defaultdict(float))  # Capacidades residuais
        self.grafo_residual = defaultdict(list)

    def inicializar_capacidades_residuais(self):
        """Inicializa as capacidades residuais com base nas arestas e fluxos."""
        for u, v, capacidade in self.arestas:
            self.capacidade_residual[u][v] = capacidade  # Capacidade residual inicial
            self.capacidade_residual[v][u] = 0  # Capacidade inversa (sem fluxo ainda)

    def criar_grafo_residual(self):
        """Cria o grafo residual com base no fluxo atual, armazenando capacidade e fluxo."""
        self.grafo_residual = defaultdict(list)
        for u, v, capacidade in self.arestas:
            fluxo_atual = self.fluxo[(u, v)]
            # Aresta original com capacidade residual e fluxo
            if capacidade - fluxo_atual > 0:
                self.grafo_residual[u].append((v, capacidade - fluxo_atual, fluxo_atual, 1))  # Tipo 1 (original)
            # Aresta reversa com capacidade igual ao fluxo atual e fluxo negativo
            if fluxo_atual > 0:
                self.grafo_residual[v].append((u, fluxo_atual, -fluxo_atual, 0))  # Tipo 0 (reversa)

    def encontrar_caminho_aumentante(self, fonte, sumidouro):
        """Busca um caminho aumentante no grafo residual usando BFS."""
        pais = [-1] * self.vertices
        visitados = [False] * self.vertices
        fila = deque([fonte])
        visitados[fonte] = True
        while fila:
            u = fila.popleft()
            for v in self.capacidade_residual[u]:
                if not visitados[v] and self.capacidade_residual[u][v] > 0:  # Há capacidade residual
                    pais[v] = u
                    if v == sumidouro:
                        return pais
                    fila.append(v)
                    visitados[v] = True
        return None

    def calcular_gargalo(self, caminho, fonte, sumidouro):
        """Calcula o gargalo do caminho aumentante."""
        gargalo = float('inf')
        atual = sumidouro
        while atual != fonte:
            anterior = caminho[atual]
            gargalo = min(gargalo, self.capacidade_residual[anterior][atual])
            atual = anterior
        return gargalo

    def atualizar_fluxos(self, caminho, gargalo, fonte, sumidouro):
        """Atualiza os fluxos no grafo residual."""
        atual = sumidouro
        while atual != fonte:
            anterior = caminho[atual]
            self.capacidade_residual[anterior][atual] -= gargalo  # Diminui a capacidade residual
            self.capacidade_residual[atual][anterior] += gargalo  # Aumenta a capacidade residual reversa
            atual = anterior
            self.fluxo[(anterior, atual)] += gargalo  # Atualiza o fluxo nas arestas

    def ford_fulkerson(self, fonte, sumidouro, arquivo=""):
        """Implementa o algoritmo de Ford-Fulkerson para fluxo máximo."""
        fonte -= 1
        sumidouro -= 1
        max_fluxo = 0

        # Inicializa as capacidades residuais no grafo
        self.inicializar_capacidades_residuais()

        # Continuar enquanto houver caminho aumentante
        while True:
            caminho = self.encontrar_caminho_aumentante(fonte, sumidouro)
            if not caminho:
                break  # Não há mais caminho aumentante
            gargalo = self.calcular_gargalo(caminho, fonte, sumidouro)
            self.atualizar_fluxos(caminho, gargalo, fonte, sumidouro)
            max_fluxo += gargalo  # Atualiza o fluxo máximo

        if arquivo:
            self.salvar_fluxos_em_disco(arquivo)

        return max_fluxo, self.fluxo

    def salvar_fluxos_em_disco(self, caminho_arquivo):
        """Salva a capacidade e o fluxo de cada aresta no grafo residual."""
        with open(caminho_arquivo, 'w') as arquivo:
            arquivo.write("Aresta,Capacidade,Fluxo\n")
            for u in self.capacidade_residual:
                for v in self.capacidade_residual[u]:
                    arquivo.write(f"{u + 1} {v + 1} {self.fluxo[(u, v)]}\n")
