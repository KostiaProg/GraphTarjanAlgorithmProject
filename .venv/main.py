import random

'''
ЩО ТРЕБА ЩЕ ЗРОБИТИ
Найближчим часом:
1) генератор рандомних графів
2) МОЖЛИВО якось об'єднати ці два класи в один, або зробити їх дітьми якогось загального класу Graph
'''

# graph[0].append(int) --- взяти першу ноду графа і пов'язати її з іншою
class GraphList:
    def __init__(self, n):
        self.graph = [[] for _ in range(n)]
        self.n = n # size

        self.stack = []
        self.on_stack = [False for _ in range(n)] # bitmap

        self.counter = 0 # to give bigger and bigger id to each node
        self.node_counter = [-1 for _ in range(n)] # to keep track which nodes have which ids, where -1 is unvisited node
        self.low = [0 for _ in range(n)] # lowlink value to create scc

        self.solved = False
        self.sccomp_count = 0

    def addEdge(self, a: int, b: int):
        if b not in graph[a]:
            self.graph[a].append(b)


    # Get amount of strongly connected components, and if don't know it yet, find it
    def getSccompCount(self) -> int:
        if self.solved == True:
            return self.sccomp
        else:
            return self.findSccomp()

    # Returns dict where key - lowlink value, value - all strongly connected nodes with this lowlink value
    def getSccomp(self) -> dict:
        nodes = {}
        for i in range(self.n):
            if self.low[i] in nodes:
                nodes[self.low[i]].append(i)
            else:
                nodes.update({self.low[i]: [i]})
        return nodes

    def findSccomp(self) -> int:
        for i in range(self.n):
            if self.visited[i] == False:
                self.dfs(i)
        return self.sccomp_count


    # dfs + algo to find all sccomp, cur - current node we are working with
    # returns lowlink value of this node
    def dfs(self, cur: int):
        if self.solved == True:
            return self.low[cur]

        self.on_stack[cur] = True
        self.stack.append(cur)
        self.node_counter[cur] = self.counter
        self.low[cur] = self.counter
        self.counter += 1

        # check all edges
        for it in self.graph[cur]:
            if self.node_counter[it] == -1:
                self.low[cur] = min(self.low[cur], self.dfs(it))
            if self.on_stack[it] == True:
                self.low[cur] = min(self.low[cur], self.low[it])


        # if we reached the node that doesn't connect to any other node after dfs, we call it sccomp, cause we can't get any lower lowlink value
        if self.node_counter[cur] == self.low[cur]:
            last_el = self.stack.pop()
            while cur != last_el:
                self.on_stack[last_el] = False
                last_el = self.stack.pop()

            self.on_stack[cur] = False
            self.sccomp_count += 1

        return self.low[cur]

    def randomGraph(self, d: float):
        n = self.n
        m = int(d * n * (n-1))
        edges_added = 0

        while edges_added < m:
            v1 = random.randint(0, n-1)
            v2 = random.randint(0, n-1)  

            # якщо ребро вже існує, пропускаємо
            if v2 in self.graph[v1]:
                continue

            self.addEdge(v1, v2)
            edges_added += 1

        return self.graph


# graph[0][1] = bool --- взяти edge від першої ноди графа і до другої ноди графа
# Якщо цей edge існує - True, інакше False
class GraphMatrix:
    def __init__(self, n):
        self.graph = [[False for _ in range(n)] for _ in range(n)]
        self.n = n # size

        self.stack = []
        self.on_stack = [False for _ in range(n)]  # bitmap

        self.counter = 0  # to give bigger and bigger id to each node
        self.node_counter = [-1 for _ in range(n)]  # to keep track which nodes have which ids, where -1 is unvisited node
        self.low = [0 for _ in range(n)]  # lowlink value to create scc

        self.solved = False
        self.sccomp_count = 0

    def addEdge(self, a: int, b: int):
        self.graph[a][b] = True


    # Get amount of strongly connected components, and if don't know it yet, find it
    def getSccompCount(self) -> int:
        if self.solved == True:
            return self.sccomp
        else:
            return self.findSccomp()

     # Returns dict where key - lowlink value, value - all strongly connected nodes with this lowlink value
    def getSccomp(self) -> dict:
        nodes = {}
        for i in range(self.n):
            if self.low[i] in nodes:
                nodes[self.low[i]].append(i)
            else:
                nodes.update({self.low[i]: [i]})
        return nodes

    def findSccomp(self) -> int:
        for i in range(self.n):
            if self.visited[i] == False:
                self.dfs(i)
        return self.sccomp_count


    # dfs + algo to find all sccomp, cur - current node we are working with
    # returns lowlink value of this node
    def dfs(self, cur: int):
        if self.solved == True:
            return self.low[cur]

        self.on_stack[cur] = True
        self.stack.append(cur)
        self.node_counter[cur] = self.counter
        self.low[cur] = self.counter
        self.counter += 1

        # check all edges
        for i in range(self.n):
            if self.graph[cur][i] == False:
                continue

            if self.node_counter[i] == -1:
                self.low[cur] = min(self.low[cur], self.dfs(i))
            if self.on_stack[i] == True:
                self.low[cur] = min(self.low[cur], self.low[i])


        # if we reached the node that doesn't connect to any other node after dfs, we call it sccomp, cause we can't get any lower lowlink value
        if self.node_counter[cur] == self.low[cur]:
            last_el = self.stack.pop()
            while cur != last_el:
                self.on_stack[last_el] = False
                last_el = self.stack.pop()

            self.on_stack[cur] = False
            self.sccomp_count += 1

        return self.low[cur]


# ? Створити окремо randomGraph для різних класів, але це вже далі по імплементації видно буде ?
# міні-тест
def short_examlpe():
    graph = GraphList(3)
    graph.randomGraph(0.58)
    print("Рандомний граф: ")
    for i, neighbors in enumerate(graph.graph):
        print(f"{i} - {neighbors}")

if __name__ == "__main__":
    short_examlpe()