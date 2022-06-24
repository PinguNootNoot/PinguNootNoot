#include <bits/stdc++.h>
#include <signal.h>
#define SIZE 82168
using namespace std;

vector<int> graph[SIZE];
vector<int> degree(SIZE, 0);
vector<pair<int, int>> corness(SIZE, {0, 0});
set<int> maxclique;
int k;

bool Kcompare(const pair<int, int> &a, const pair<int, int> &b){
    return a.second > b.second;
}

class Graph {
private:

    void Kcore(int k){
        bool exit = false;

        while(!exit){
            exit = true;
            bool flag = false;

            while(!flag){
                flag = true;
                for(int i = 0; i < degree.size(); ++i){
                    if(degree[i] >= 0 && degree[i] < k){
                        flag = false;
                        corness.push_back({i, k-1});
                        if(degree[i] != 0){
                            for(int j = 0; j < graph[i].size(); ++j) --degree[graph[i][j]];
                        }
                        degree[i] = -1;
                    }
                    else if(degree[i] > 0) exit = false;
                }
            }
            ++k;
        }
    }

    //  TO FIND Maximum Clique:
    //
    //  algorithm BronKerbosch2(R, P, X) is
    //  if P and X are both empty then
    //      report R as a maximal clique
    //
    //  for each vertex v in P U X do
    //      BronKerbosch2(R U {v}, P intersects N(v), X intersects N(v))
    //      P := P \ {v}
    //      X := X U {v}
    //  ----------------------------------------------------------------------
    //  algorithm BronKerbosch3(G) is
    //  P = V(G)    # P is the set of all vertices in graph G
    //  R = X = empty    # R & X initialized as empty sets
    //
    //  for each vertex v in a degeneracy ordering of G do
    //      BronKerbosch2({v}, P intersects N(v), X intersects N(v))
    //      P := P \ {v}
    //      X := X U {v}
    void subBron(set<int> R, set<int> P, set<int> X){
        auto PX = P;  // P U X
        set<int> NP, NX;

        if(P.empty() && X.empty()){
            auto tmp = R;
            if(maxclique.size() < tmp.size()) maxclique = tmp;
            return;
        }
        for(set<int>::iterator it = X.begin(); it != X.end(); ++it) PX.insert(*it);
        for(set<int>::iterator it = PX.begin(); it != PX.end(); ++it){
            if(R.size() + P.size() <= maxclique.size()) return;

            for(int j = 0; j < graph[*it].size(); ++j){
                if(P.find(graph[*it][j]) != P.end()){
                    NP.insert(graph[*it][j]);
                }
            }
            for(int j = 0; j < graph[*it].size(); ++j){
                if(X.find(graph[*it][j]) != X.end()){
                    NX.insert(graph[*it][j]);
                }
            }
            R.insert(*it);
            subBron(R,NP,NX);
            R.erase(*it);
            P.erase(*it);
            X.insert(*it);
            NP.clear();
            NX.clear();
        }
    }

    void BronKerbosch(){
        set<int> P, R, X;
        set<int> NP, NX;  // For neighbor

        for(int i = 0; i < SIZE; ++i) P.insert(i);
        auto degeneracy = corness;
        sort(degeneracy.begin(), degeneracy.end(), Kcompare);

        for(int i = 0; i < degeneracy.size(); ++i){
            for(int j = 0; j < graph[degeneracy[i].first].size(); ++j){
                if(P.find(graph[degeneracy[i].first][j]) != P.end()){
                    NP.insert(graph[degeneracy[i].first][j]);
                }
            }
            for(int j = 0; j < graph[degeneracy[i].first].size(); ++j){
                if(X.find(graph[degeneracy[i].first][j]) != X.end()){
                    NX.insert(graph[degeneracy[i].first][j]);
                }
            }
            R.insert(degeneracy[i].first);
            subBron(R,NP,NX);
            R.clear();
            P.erase(degeneracy[i].first);
            X.insert(degeneracy[i].first);
            NP.clear();
            NX.clear();
        }
    }

public:
    void kcorepath(){
        Kcore(1);
        sort(corness.begin(), corness.end());
    }

    void cliquepath(){
        BronKerbosch();
    }
};

void signalHandler(int signum){
    cout << "Get signal " << signum << endl;

    ofstream out;
    out.open("kcore.txt", ios::trunc);
    for(int i = 0; i < corness.size(); ++i){
        if(corness[i].second >= k){
            out << corness[i].first << ' ' << corness[i].second << endl;
        }
    }
    out.close();

    ofstream clique;
    clique.open("clique.txt", ios::trunc);
    for(set<int>::iterator it = maxclique.begin(); it != maxclique.end(); ++it){
        clique << (*it) << endl;
    }
    clique.close();
    exit(signum);
}

int main(int argc, char *argv[]){
    Graph g;
    int v1, v2;
    clock_t t;

    string file_name = string(argv[1]);
    string K = string(argv[2]);
    k = stoi(K);

    signal(SIGINT, signalHandler);
    //--------------------------------
    ifstream in;
    in.open(file_name, ios::in);
    while(in >> v1 >> v2){
        graph[v1].push_back(v2);
        graph[v2].push_back(v1);
        ++degree[v1];
        ++degree[v2];
    }
    in.close();
    g.kcorepath();
    g.cliquepath();

    ofstream out;
    out.open("kcore.txt", ios::trunc);
    for(int i = 0; i < corness.size(); ++i){
        if(corness[i].second >= k){
            out << corness[i].first << ' ' << corness[i].second << endl;
        }
    }
    out.close();

    ofstream clique;
    clique.open("clique.txt", ios::trunc);
    for(set<int>::iterator it = maxclique.begin(); it != maxclique.end(); ++it){
        clique << (*it) << endl;
    }
    clique.close();

    return 0;
}
