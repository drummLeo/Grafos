#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <queue>
#include <chrono>
#include <iomanip> // Para configurar precisão da saída
#include <limits>


using namespace std;

class GrafoDirecionadoComPesos {
private:
    struct Aresta {
        int destino;
        double capacidade;
        bool original; // true para aresta original, false para reversa
    };

    int numVertices;
    unordered_map<int, vector<Aresta>> grafoResidual;

public:
    GrafoDirecionadoComPesos(int vertices) : numVertices(vertices) {}

    void adicionarAresta(int origem, int destino, double capacidade) {
        grafoResidual[origem].push_back({destino, capacidade, true});
        grafoResidual[destino].push_back({origem, 0, false}); // Aresta reversa com capacidade 0
    }

    double fluxoMaximo(int origem, int destino) {
        double fluxoTotal = 0;

        while (true) {
            // Busca em largura para encontrar um caminho aumentante
            vector<int> parent(numVertices, -1);
            queue<pair<int, double>> fila;
            fila.push(make_pair(origem, numeric_limits<double>::max()));

            while (!fila.empty()) {
                int atual = fila.front().first;
                double fluxo = fila.front().second;
                fila.pop();

                for (const auto& aresta : grafoResidual[atual]) {
                    if (parent[aresta.destino] == -1 && aresta.destino != origem && aresta.capacidade > 0) {
                        parent[aresta.destino] = atual;
                        double novoFluxo = min(fluxo, aresta.capacidade);

                        if (aresta.destino == destino) {
                            fluxoTotal += novoFluxo;

                            // Atualizar as capacidades no grafo residual
                            int cur = destino;
                            while (cur != origem) {
                                int prev = parent[cur];
                                for (auto& a : grafoResidual[prev]) {
                                    if (a.destino == cur) {
                                        a.capacidade -= novoFluxo;
                                        break;
                                    }
                                }
                                for (auto& a : grafoResidual[cur]) {
                                    if (a.destino == prev) {
                                        a.capacidade += novoFluxo;
                                        break;
                                    }
                                }
                                cur = prev;
                            }
                            goto next_iteration; // Caminho encontrado, continuar o loop
                        }

                        fila.push({aresta.destino, novoFluxo});
                    }
                }
            }
            break; // Se não encontrou caminho, fim do algoritmo

        next_iteration:;
        }

        return fluxoTotal;
    }

    // Lê um grafo de um arquivo
    static GrafoDirecionadoComPesos lerDeArquivo(const string& nomeArquivo) {
        ifstream arquivo(nomeArquivo);
        if (!arquivo.is_open()) {
            cerr << "Erro ao abrir o arquivo: " << nomeArquivo << endl;
            exit(1);
        }

        string linha;
        getline(arquivo, linha); // Número de vértices
        int numVertices = stoi(linha);

        GrafoDirecionadoComPesos grafo(numVertices);

        while (getline(arquivo, linha)) {
            stringstream ss(linha);
            int origem, destino;
            double capacidade;
            ss >> origem >> destino >> capacidade;
            grafo.adicionarAresta(origem - 1, destino - 1, capacidade); // Índices ajustados para 0
        }

        arquivo.close();
        return grafo;
    }
};

int main() {
    string caminhoArquivo = "grafo_rf_6.txt";

    // Lê o grafo do arquivo
    GrafoDirecionadoComPesos grafo = GrafoDirecionadoComPesos::lerDeArquivo(caminhoArquivo);

    // Cálculo do fluxo máximo e medição do tempo
    auto inicio = chrono::high_resolution_clock::now();
    double fluxoMax = grafo.fluxoMaximo(0, 1); // Considerando vértices 1 e 2 como origem e destino
    auto fim = chrono::high_resolution_clock::now();

    // Tempo de execução
    chrono::duration<double> duracao = fim - inicio;

    // Resultados
    cout << "Fluxo máximo: " << fluxoMax << endl;
    cout << fixed << setprecision(9) << "Tempo de execução: " << duracao.count() << " segundos" << endl;

    return 0;
}