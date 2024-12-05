import sys

sys.setrecursionlimit()

class ListAdj:
    def __init__(self, n, m) -> None:
        self.n = n
        self.m = m
        self.list = dict()

        for i in range(1,n+1):
            entry = list(map(int, input(f'Vertices conectados a {i}: ').split()))
            self.list[i] = entry

    def neighbours(self, index: int):
        neighbourhood = self.list[index]

        return neighbourhood


def dfs(pai: int, v: dict):
    global cont
    global pre
    global graph
    
    cont += 1
    pre[v] = cont

    w = graph.neighbours(v)

    for vertex in w:
        if pre[vertex-1] == 0:
            dfs(v, vertex)


def maxpath(pai, v):
    global cont
    global marked

    cont += 1
    marked[v] = 1

    w = graph[v]

    for i in w:
        if marked[i] == 0:
            maxpath(v,i)

    marked[v] = 0


def top(array):
    value = array[0]
    top = 0

    for i in range(1,len(array)):
        if array[i] > top:
            value = array[i]
            top = i

    return top

             

if __name__ == "__main__":
    n,m = map(int, input('Insira o N e o M: ').split())

    graph = ListAdj(n,m)
    cont = 0
    pre = [0] * graph.n

    chosen = int(input("\nQual vertice escolhido: "))
    chosen_neighbourhood = graph.neighbours(chosen)

    if len(chosen_neighbourhood) > 1:
        for i in range(graph.n):
            if pre[i] == 0:
                dfs(i+1,i+1)

        root = top(pre)
        cont = 0
        marked = [0] * graph.n

        maxpath(root+1, root+1)
        print(f"\nO comprimento do maior caminho é {cont}")

    else:
        print("\n\nO comprimento do maior caminho é 0 pois o vértice é uma extremidade ")
