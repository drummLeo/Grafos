from scipy.sparse import lil_matrix

from collections import deque


class Grafo:
    def __init__(self, arquivo):
        self.arestas = tuple()
        self.vertices = 0
        if arquivo is not None:
            with open(arquivo, "r") as f:
                self.vertices = int(f.readline())
                self.arestas = (x.strip() for x in f.readlines())
        self.matriz = []
        self.adjacencia = {}

    def matriz_adjacencia(self):
        # Usamos lil_matrix, pois é eficiente para a construção da matriz
        self.matriz = lil_matrix((self.vertices, self.vertices), dtype=bool)

        for aresta in self.arestas:
            v1, v2 = map(int, aresta.split())
            # Ajuste dos índices (se necessário)
            self.matriz[v1 - 1, v2 - 1] = 1
            self.matriz[v2 - 1, v1 - 1] = 1

        # Opcionalmente, podemos converter para csr_matrix após a construção,
        # que é mais eficiente para operações e armazenamento
        self.matriz = self.matriz.tocsr()

    def lista_adjacencia(self):
        self.adjacencia = {i: [] for i in range(self.vertices)}
        for aresta in self.arestas:
            u, v = map(int, aresta.split())
            self.adjacencia[u - 1].append(v - 1)
            self.adjacencia[v - 1].append(u - 1)

    def grau_minimo(self):
        grau_min = self.vertices
        if self.adjacencia:
            for vertice in self.adjacencia:
                grau_vertice = len(self.adjacencia[vertice])
                grau_min = min(grau_min, grau_vertice)
        if self.matriz:
            for vertice in self.matriz:
                grau_vertice = sum(vertice)
                grau_min = min(grau_min, grau_vertice)

        return grau_min

    def grau_maximo(self):
        grau_maximo = 0

        if self.adjacencia:
            for vertice in self.adjacencia:
                grau_vertice = len(self.adjacencia[vertice])
                grau_maximo = max(grau_maximo, grau_vertice)
        if self.matriz:
            for vertice in self.matriz:
                grau_vertice = sum(vertice)
                grau_maximo = max(grau_maximo, grau_vertice)

        return grau_maximo

    def grau_medio(self):
        if self.adjacencia:
            return sum([len(self.adjacencia[vertice]) for vertice in self.adjacencia]) // self.vertices
        if self.matriz:
            return sum([sum(vertice) for vertice in self.matriz]) // self.vertices

    def mediana_de_grau(self):
        if self.adjacencia:
            graus = sorted([len(self.adjacencia[vertice]) for vertice in self.adjacencia])
            return graus[len(graus) // 2]
        if self.matriz:
            graus = sorted([sum(vertice) for vertice in self.matriz])
            return graus[len(graus) // 2]

    def bfs(self, vertice_inicial, arquivo_saida=None):
        vertice_inicial -= 1
        if vertice_inicial < 0 or vertice_inicial >= self.vertices:
            raise KeyError("Vértice não encontrado")
        if self.adjacencia:
            # Dicionários para armazenar o pai e o nível de cada vértice
            pai = {}
            nivel = {}

            # Fila para o BFS
            fila = deque([vertice_inicial])

            # Inicializando o pai e nível do vértice inicial
            pai[vertice_inicial] = None
            nivel[vertice_inicial] = 0

            # Executando o BFS
            while fila:
                vertice = fila.popleft()

                # Iterando sobre os vizinhos do vértice atual
                for vizinho in self.adjacencia[vertice]:
                    if vizinho not in nivel:  # Se o vizinho não foi visitado
                        fila.append(vizinho)
                        pai[vizinho] = vertice
                        nivel[vizinho] = nivel[vertice] + 1
        else:

            # Dicionários para armazenar o pai e o nível de cada vértice
            pai = {}
            nivel = {}

            # Fila para o BFS
            fila = deque([vertice_inicial])

            # Inicializando o pai e nível do vértice inicial
            pai[vertice_inicial] = None
            nivel[vertice_inicial] = 0

            # Executando o BFS
            while fila:
                vertice = fila.popleft()

                vizinhos = self.matriz[vertice].indices

                # Iterando sobre os vizinhos do vértice atual (checa a matriz de adjacência)
                for vizinho in vizinhos:
                    if vizinho not in nivel:
                        fila.append(vizinho)
                        pai[vizinho] = vertice
                        nivel[vizinho] = nivel[vertice] + 1

        if arquivo_saida is not None:
            # Escrevendo o resultado no arquivo de saída
            with open(arquivo_saida, 'w') as f:
                f.write(f"Vértice inicial: {vertice_inicial + 1}\n")
                f.write("Vértice, Pai, Nível\n")
                for vertice in nivel:
                    f.write(
                        f"{vertice + 1}, {pai[vertice] + 1 if pai[vertice] is not None else None}, {nivel[vertice]}\n")

        return [(vertice + 1, pai[vertice] + 1 if pai[vertice] is not None else None, nivel[vertice]) for vertice in
                nivel if nivel]

    def dfs(self, vertice_inicial, arquivo_saida=None):
        vertice_inicial -= 1
        if vertice_inicial < 0 or vertice_inicial >= self.vertices:
            raise KeyError("Vértice não encontrado")
        if self.adjacencia:
            # Dicionários para armazenar o pai e o nível de cada vértice
            pai = {}
            nivel = {}

            # Pilha para o DFS (inicialmente com o vértice inicial)
            pilha = [(vertice_inicial, 0)]  # (vértice, nível)
            pai[vertice_inicial] = None
            nivel[vertice_inicial] = 0

            # Realizando a DFS iterativa
            while pilha:
                vertice, nivel_atual = pilha.pop()

                # Verifica os vizinhos do vértice (na lista de adjacência)
                for vizinho in self.adjacencia.get(vertice, []):
                    if vizinho not in nivel:
                        # Marcar o pai e o nível do vizinho
                        pai[vizinho] = vertice
                        nivel[vizinho] = nivel_atual + 1
                        # Adiciona o vizinho na pilha
                        pilha.append((vizinho, nivel_atual + 1))
        else:
            # Dicionários para armazenar o pai e o nível de cada vértice
            pai = {}
            nivel = {}

            # Pilha para o DFS (inicialmente com o vértice inicial)
            pilha = [(vertice_inicial, 0)]  # (vértice, nível)
            pai[vertice_inicial] = None
            nivel[vertice_inicial] = 0

            # Realizando a DFS iterativa
            while pilha:
                vertice, nivel_atual = pilha.pop()
                vizinhos = self.matriz[vertice].indices

                # Verifica os vizinhos do vértice (na matriz de adjacência)
                for vizinho in vizinhos:
                    if vizinho not in nivel:
                        # Marcar o pai e o nível do vizinho
                        pai[vizinho] = vertice
                        nivel[vizinho] = nivel_atual + 1
                        # Adiciona o vizinho na pilha
                        pilha.append((vizinho, nivel_atual + 1))

        if arquivo_saida is not None:
            # Escrevendo o resultado no arquivo de saída
            with open(arquivo_saida, 'w') as f:
                f.write(f"Vértice inicial: {vertice_inicial}\n")
                f.write("Vértice, Pai, Nível\n")
                for vertice in nivel:
                    f.write(
                        f"{vertice + 1}, {pai[vertice] + 1 if pai[vertice] is not None else None}, {nivel[vertice]}\n")
                    if vertice + 1 in (10, 20, 30):
                        print(
                            f"{vertice + 1}, {pai[vertice] + 1 if pai[vertice] is not None else None}, {nivel[vertice]}\n")

    def bfs_distancia(self, vertice_inicial):
        if self.adjacencia:
            # Dicionário para armazenar a distância do vértice inicial até os outros
            distancias = {vertice_inicial: 0}

            # Fila para o BFS
            fila = deque([vertice_inicial])

            # Executa o BFS
            while fila:
                vertice = fila.popleft()

                # Para cada vizinho do vértice
                for vizinho in self.adjacencia.get(vertice, []):
                    if vizinho not in distancias:
                        distancias[vizinho] = distancias[vertice] + 1
                        fila.append(vizinho)
        elif self.matriz:
            n = len(self.matriz)  # Número de vértices no grafo
            distancias = [-1] * n  # Inicializa as distâncias como -1 (não visitado)
            distancias[vertice_inicial] = 0  # Distância do vértice inicial para ele mesmo é 0

            # Fila para o BFS
            fila = deque([vertice_inicial])

            # Executa o BFS
            while fila:
                vertice = fila.popleft()
                vizinhos = self.matriz[vertice].indices

                # Para cada vizinho do vértice (usando a matriz de adjacência)
                for vizinho in vizinhos:
                    if self.matriz[vertice, vizinho] == 1 and distancias[vizinho] == -1:  # Não visitado
                        distancias[vizinho] = distancias[vertice] + 1
                        fila.append(vizinho)

        return distancias

    def distancia(self, v1, v2):
        v1 -= 1
        v2 -= 1
        # Executa o BFS a partir do vértice u
        distancias = self.bfs_distancia(v1)

        # Retorna a distância do vértice u até o vértice v (se existir caminho)
        return distancias.get(v2, float('inf')) if self.adjacencia else (
            distancias[v2] if distancias[v2] != -1 else float('inf'))  # Se v não for acessível, retorna infinito

    def bfs_diametro(self, start):
        visitados = {start: 0}
        fila = deque([start])

        no_mais_distante = start
        distancia_maxima = 0

        while fila:
            no_atual = fila.popleft()
            distancia_atual = visitados[no_atual]

            for vizinho in self.adjacencia[no_atual]:
                if vizinho not in visitados:
                    visitados[vizinho] = distancia_atual + 1
                    fila.append(vizinho)

                    # Atualiza o vértice mais distante e a distância máxima
                    if visitados[vizinho] > distancia_maxima:
                        distancia_maxima = visitados[vizinho]
                        no_mais_distante = vizinho

        return no_mais_distante, distancia_maxima

    def diametro_aproximado(self):
        # Escolhe um vértice arbitrário (pode ser o primeiro da lista)
        no_aleatorio = next(iter(self.adjacencia))

        # Primeiro BFS a partir de um vértice arbitrário
        no_mais_distante, _ = self.bfs_diametro(no_aleatorio)

        # Segundo BFS a partir do vértice mais distante encontrado
        _, distancia_maxima = self.bfs_diametro(no_mais_distante)

        return distancia_maxima

    def diametro(self):
        diametro = 0
        if self.adjacencia:
            # Para cada vértice do grafo, calcular a maior distância a partir dele
            for vertice in self.adjacencia:
                distancias = self.bfs_distancia(vertice)
                # A maior distância encontrada a partir deste vértice
                maior_distancia = max(distancias.values(), default=0)
                # Atualiza o diâmetro se essa distância for maior que o atual
                diametro = max(diametro, maior_distancia)
        elif self.matriz:
            # Para cada vértice do grafo, calcular a maior distância a partir dele
            for vertice in self.matriz:
                distancias = self.bfs_distancia(vertice)
                # Ignora os vértices inacessíveis (-1) e calcula a maior distância
                maior_distancia = max([dist for dist in distancias if dist != -1], default=0)
                # Atualiza o diâmetro se essa distância for maior que o atual
                diametro = max(diametro, maior_distancia)

        return diametro

    def bfs_componente(self, vertice_inicial, visitados):
        if self.adjacencia:
            componente = []
            fila = deque([vertice_inicial])
            visitados.add(vertice_inicial)

            while fila:
                vertice = fila.popleft()
                componente.append(vertice + 1)

                for vizinho in self.adjacencia.get(vertice, []):
                    if vizinho not in visitados:
                        visitados.add(vizinho)
                        fila.append(vizinho)
        elif self.matriz:
            componente = []
            fila = deque([vertice_inicial])
            visitados.add(vertice_inicial)

            while fila:
                vertice = fila.popleft()
                componente.append(vertice + 1)

                vizinhos = self.matriz[vertice].indices

                for vizinho in vizinhos:
                    if vizinho not in visitados:
                        visitados.add(vizinho)
                        fila.append(vizinho)

        return componente

    # Função para encontrar as componentes conexas do grafo
    def encontrar_componentes_conexas(self):
        if self.adjacencia:
            visitados = set()  # Conjunto de vértices já visitados
            componentes = []  # Lista de componentes conexas

            # Explora cada vértice do grafo
            for vertice in self.adjacencia:
                if vertice not in visitados:
                    componente = self.bfs_componente(vertice, visitados)
                    componentes.append(componente)

            # Ordena as componentes por tamanho (ordem decrescente)
            componentes.sort(key=len, reverse=True)
        elif self.matriz:
            visitados = set()  # Conjunto de vértices já visitados
            componentes = []  # Lista de componentes conexas

            # Explora cada vértice do grafo
            for vertice in range(self.vertices):
                if vertice not in visitados:
                    componente = self.bfs_componente(vertice, visitados)
                    componentes.append(componente)

            # Ordena as componentes por tamanho (ordem decrescente)
            componentes.sort(key=len, reverse=True)

        return componentes

    def gerar_texto(self):
        with open("resultado_1.txt", "w") as f:
            f.write(str(self.vertices) + '\n')
            f.write(str(len(self.arestas)) + '\n')
            f.write(str(self.grau_minimo()) + '\n')
            f.write(str(self.grau_maximo()) + '\n')
            f.write(str(self.grau_medio()) + '\n')
            f.write(str(self.mediana_de_grau()) + '\n')
