from grafos_com_pesos import GrafoComPesos

k = 10
for i in range(1, 2):
    g = GrafoComPesos(f"grafo_W_{i}.txt")
    g.lista_adjacencia()

    for j in range(20, 61, 10):
        dijkstra = g.dijkstra_heap(10)
        print(f"Distância/Caminho mínimo (Grafo {i} - Vértice {j}): {dijkstra[0][j-1]}/{g.obter_caminho(dijkstra[1], j)}")

    print(f"Tempo médio (Grafo {i}):", g.tempo_medio_dijkstra(k))
    del g

g = GrafoComPesos("rede_colaboracao.txt")
g.lista_adjacencia()
for autor in ("Alan M. Turing", "J. B. Kruskal", "Jon M. Kleinberg", "Éva Tardos", "Daniel R. Figueiredo"):
    print(f'Distância entre "Edsger W. Dijkstra" e "{autor}":', g.calcular_distancias_entre_pesquisadores("Edsger W. Dijkstra", autor))
