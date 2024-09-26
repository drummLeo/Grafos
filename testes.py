import time
import tracemalloc
from grafos import *

if __name__ == '__main__':
    for i in range(1, 7):
        try:
            print(f"grafo_{i}.txt: Matriz")
            tracemalloc.start()
            g = Grafo(f"grafo_{i}.txt")
            g.matriz_adjacencia()
            print(tracemalloc.get_traced_memory()[1] / (1024 * 1024), "MB")
            del g

            tracemalloc.reset_peak()

            print(f"grafo_{i}.txt: Lista")
            g = Grafo(f"grafo_{i}.txt")
            g.lista_adjacencia()
            print(tracemalloc.get_traced_memory()[1] / (1024 * 1024), "MB")
            tracemalloc.stop()
            del g
        except MemoryError as e:
            print("Memória Insuficiente:", e.args)

    for i in range(1, 7):
        g = Grafo(f"grafo_{i}.txt")
        g.lista_adjacencia()
        t1 = time.perf_counter()
        for j in range(1, 101):
            g.bfs(j)
        t2 = time.perf_counter()
        print(f"100 BFS (Grafo {i} - Lista de Adjacência):", t2 - t1)

    for i in range(1, 7):
        g = Grafo(f"grafo_{i}.txt")
        g.matriz_adjacencia()
        t1 = time.perf_counter()
        for j in range(1, 101):
            g.bfs(j)
        t2 = time.perf_counter()
        print(f"100 BFS (Grafo {i} - Matriz de Adjacência):", t2 - t1)

    for i in range(1, 7):
        g = Grafo(f"grafo_{i}.txt")
        g.lista_adjacencia()
        t1 = time.perf_counter()
        for j in range(1, 101):
            g.dfs(j)
        t2 = time.perf_counter()
        print(f"100 DFS (Grafo {i} - Lista de Adjacência):", t2 - t1)

    for i in range(1, 7):
        g = Grafo(f"grafo_{i}.txt")
        g.matriz_adjacencia()
        t1 = time.perf_counter()
        for j in range(1, 101):
            g.dfs(j)
        t2 = time.perf_counter()
        print(f"100 DFS (Grafo {i} - Matriz de Adjacência):", t2 - t1)

    for n in range(1, 7):
        print(f"grafo {n}:", "\tvértice \tpai\n")
        g = Grafo(f"grafo_{n}.txt")
        g.lista_adjacencia()
        for i in (1, 2, 3):
            bfs = g.bfs(i)
            print(f"bfs {i}:")
            for j in (10, 20, 30):
                try:
                    vertice, pai = bfs[[x[0] for x in bfs].index(j)][:2]
                    print("\t\t\t", vertice, "\t\t", pai)
                except ValueError:
                    print(f"O vértice {j} não está na bfs de {i} no grafo {n}")
            print()

    for i in range(1, 7):
        g = Grafo(f"grafo_{i}.txt")
        g.lista_adjacencia()
        print(f"Grafo {i}:\n")
        print("Distância (10, 20):", g.distancia(10, 20))
        print("Distância (10, 30):", g.distancia(10, 30))
        print("Distância (20, 30):", g.distancia(20, 30))
        print()

    for i in range(1, 7):
        g = Grafo(f"grafo_{i}.txt")
        g.lista_adjacencia()
        print(f"Grafo {i}:\n")
        componentes_conexas = g.encontrar_componentes_conexas()
        print("Componentes conexas:", g.encontrar_componentes_conexas())
        print("Maior Componente:", componentes_conexas[0])
        print("Tamanho:", len(componentes_conexas[0]))
        print("Menor Componente:", componentes_conexas[-1])
        print("Tamanho:", len(componentes_conexas[-1]))
        print()

    for i in range(1, 7):
        g = Grafo(f"grafo_{i}.txt")
        g.lista_adjacencia()

        print(f"Diâmetro do Grafo {i}: ", g.diametro_aproximado() if i > 1 else g.diametro())
