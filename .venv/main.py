'''
ЩО ТРЕБА ЩЕ ЗРОБИТИ
Найближчим часом:
1)ТЕСТИ
2) МОЖЛИВО якось об'єднати ці два класи в один, або зробити їх дітьми якогось загального класу Graph
'''

import networkx as nx
import matplotlib.pyplot as plt
import random

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
        if b not in self.graph[a]:
            self.graph[a].append(b)

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

    def visualise(self):
        graph_visualisation = nx.DiGraph()

        for edge_from in range(self.n):
            # lonely node - just put it without edges
            if not self.graph[edge_from]:
                edge_name = edge_from
                if self.solved == True:
                    edge_name += f" Group {self.low[edge_from]}"

                graph_visualisation.add_node(edge_from)

            for edge_to in self.graph[edge_from]:
                if self.solved == True:
                    # if the compononents are SC, they are all connected with GREEN edges, but if they are in different groups, the edge is RED
                    edge_color = 'green'
                    if self.low[edge_from] != self.low[edge_to]:
                        edge_color = 'red'

                    # Add labels with SCC group numbers
                    graph_visualisation.add_edge(edge_from + f" Group {self.low[edge_from]}", edge_to + f" Group {self.low[edge_to]}", color=edge_color)

                    graph_visualisation.nodes[edge_from]['group'] = str(self.low[edge_from])
                    graph_visualisation.nodes[edge_to]['group'] = str(self.low[edge_to])
                else:
                    # if we haven't tested the graph for SCC, then all edges are BLACK
                    graph_visualisation.add_edge(edge_from, edge_to)

        # Get the edge colors data to draw with them if we have performed SCC algo
        if self.solved == True:
            edge_colors = [graph_visualisation[edge_from][edge_to]['color'] for edge_from, edge_to in graph_visualisation.edges()]
            nx.draw_networkx(graph_visualisation, edge_color=edge_colors)
        else:
            nx.draw_networkx(graph_visualisation)
        plt.show()


    # Get amount of strongly connected components, and if don't know it yet, find it
    def getSccompCount(self) -> int:
        if self.solved == True:
            return self.sccomp
        else:
            return self.findSccomp()

    # Returns dict where key - lowlink value, value - all strongly connected nodes with this lowlink value
    def getSccomp(self) -> dict:
        nodes = {}
        for i in range(n):
            if self.low[i] in nodes:
                nodes[self.low[i]].append(i)
            else:
                nodes.update({self.low[i]: [i]})
        return nodes

    def findSccomp(self) -> int:
        for i in range(n):
            if self.visited[i] == False:
                self.dfs(i)
        return self.sccomp_count


    # dfs + algo to find all sccomp, cur - current node we are working with
    # returns lowlink value of this node
    def dfs(self, cur: int):
        if self.solved == True:
            return low[cur]

        self.on_stack[cur] = True
        self.stack.append(cur)
        self.node_counter[cur] = counter
        self.low[cur] = counter
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

    def randomGraph(self, d: float):
        n = self.n
        m = int(d * n * (n-1))
        edges_added = 0

        while edges_added < m:
            v1 = random.randint(0, n-1)
            v2 = random.randint(0, n-1)

            # якщо ребро вже існує, пропускаємо
            if self.graph[v1][v2] == True:
                continue

            self.addEdge(v1, v2)
            edges_added += 1

        return self.graph

    def visualise(self):
        graph_visualisation = nx.DiGraph()

        for edge_from in range(self.n):
            added = False
            for edge_to in range(self.n):
                if self.graph[edge_from][edge_to] == True:
                    added = True
                    if self.solved == True:
                        # if the compononents are SC, they are all connected with GREEN edges, but if they are in different groups, the edge is RED
                        edge_color = 'green'
                        if self.low[edge_from] != self.low[edge_to]:
                            edge_color = 'red'

                        # Add labels with SCC group numbers
                        graph_visualisation.add_edge(edge_from + f" Group {self.low[edge_from]}",
                                                     edge_to + f" Group {self.low[edge_to]}", color=edge_color)

                        graph_visualisation.nodes[edge_from]['group'] = str(self.low[edge_from])
                        graph_visualisation.nodes[edge_to]['group'] = str(self.low[edge_to])
                    else:
                        # if we haven't tested the graph for SCC, then all edges are BLACK
                        graph_visualisation.add_edge(edge_from, edge_to)

            # lonely node - just put it without edges
            if added == False:
                edge_name = edge_from
                if self.solved == True:
                    edge_name += f" Group {self.low[edge_from]}"

                graph_visualisation.add_node(edge_from)


        # Get the edge colors data to draw with them if we have performed SCC algo
        if self.solved == True:
            edge_colors = [graph_visualisation[edge_from][edge_to]['color'] for edge_from, edge_to in graph_visualisation.edges()]
            nx.draw_networkx(graph_visualisation, edge_color=edge_colors)
        else:
            nx.draw_networkx(graph_visualisation)
        plt.show()


    # Get amount of strongly connected components, and if don't know it yet, find it
    def getSccompCount(self) -> int:
        if self.solved == True:
            return self.sccomp
        else:
            return self.findSccomp()

     # Returns dict where key - lowlink value, value - all strongly connected nodes with this lowlink value
    def getSccomp(self) -> dict:
        nodes = {}
        for i in range(n):
            if self.low[i] in nodes:
                nodes[low[i]].append(i)
            else:
                nodes.update({self.low[i]: [i]})
        return nodes

    def findSccomp(self) -> int:
        for i in range(n):
            if self.visited[i] == False:
                self.dfs(i)
        return self.sccomp_count


    # dfs + algo to find all sccomp, cur - current node we are working with
    # returns lowlink value of this node
    def dfs(self, cur: int):
        if self.solved == True:
            return low[cur]

        self.on_stack[cur] = True
        self.stack.append(cur)
        self.node_counter[cur] = counter
        self.low[cur] = counter
        self.counter += 1

        # check all edges
        for i in range(n):
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


# міні-тест
graph = GraphList(3)
graph.randomGraph(0.58)
print("Рандомний граф: ")
for i, neighbors in enumerate(graph.graph):
    print(f"{i} - {neighbors}")

graph.visualise()