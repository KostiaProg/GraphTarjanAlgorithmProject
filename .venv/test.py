# що ж, попробую використати все
import math
import json
import main as graph
from testCode import TimeTester as Tester

vertices = [20*(i+1) for i in range(1, 25)]

list_graphs = []
matrix_graphs = []
for v in vertices:
    for d in [0.5, 0.8, 1, 2.0, 5.0, math.log(v), 2*math.log(v), 20, v*0.5, v]:
        d = d/v
        print((v, d))
        l_graphs = []
        m_graphs = []
        for _ in range(10):
            list_graph = graph.Graph.static_randomGraph(v, d)
            l_graphs.append(list_graph)

            matrix_graph = graph.GraphMatrix(v)
            matrix_graph.fromOther(list_graph)
            
            m_graphs.append(matrix_graph)
        list_graphs.append((v, d, l_graphs))
        matrix_graphs.append((v, d, m_graphs))

tester = Tester(None)
l_results = {}
m_results = {}

for (v, d, l_graphs) , (v, d, m_graphs) in zip(list_graphs, matrix_graphs):
    print((v, d))
    for l_graph in l_graphs:
        tester.setFunc(l_graph.findSccomp)
        tester.test()
    l_results[f"{(v , d)}"] = (tester.times, tester.outputs)

    tester.reset()
    
    for m_graph in m_graphs:
        tester.setFunc(m_graph.findSccomp)
        tester.test()
    m_results[f"{(v , d)}"] = (tester.times, tester.outputs)
    
    tester.reset()


with open(".venv/data.json", 'w') as file:
    json.dump((l_results, m_results), file)