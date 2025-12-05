import json
import matplotlib.pyplot as plt


with open(".venv/data.json", 'r') as file:
    list_graphs, matrix_graphs = json.load(file)

Rlist_graphs   = {}
Rmatrix_graphs = {}
V_list = []
D_dict = {}

for (Lv_d, list_graph), (Mv_d, matrix_graph) in zip(list_graphs.items(), matrix_graphs.items()):
    v_l , d_l = Lv_d[1:-1].split(',')
    v_l = int  (v_l)
    d_l = float(d_l)
    Rlist_graphs[(v_l, d_l)] = {"min": (min(list_graph[0]), min(list_graph[1])), "max": (max(list_graph[0]), max(list_graph[1])), "average": (sum(list_graph[0])/len(list_graph[0]), sum(list_graph[1])/len(list_graph[1]))}
    
    v_m , d_m = Mv_d[1:-1].split(',')
    v_m = int  (v_m)
    d_m = float(d_m)
    Rmatrix_graphs[(v_l, d_l)] = {"min": (min(matrix_graph[0]), min(matrix_graph[1])), "max": (max(matrix_graph[0]), max(matrix_graph[1])), "average": (sum(matrix_graph[0])/len(matrix_graph[0]), sum(matrix_graph[1])/len(matrix_graph[1]))}
    
    if v_l in D_dict:
        D_dict[v_l].append(d_l)
    else: 
        V_list.append(v_l)
        D_dict[v_l] = [d_l]


for g_type, graphs in [("list", Rlist_graphs), ("matrix", Rmatrix_graphs)]:
    for v in V_list:
        maxes   = []
        mins    = []
        average = []
        
        r_maxes   = []
        r_mins    = []
        r_average = []

        for d in D_dict[v]:
            data = graphs[v, d]
            maxes.append    (data["max"][0])
            mins.append     (data["min"][0])
            average.append  (data["average"][0])
            
            r_maxes.append    (data["max"][1])
            r_mins.append     (data["min"][1])
            r_average.append  (data["average"][1])        

        plt.plot(D_dict[v], maxes  , "--r")
        plt.plot(D_dict[v], mins   , "--r")
        plt.plot(D_dict[v], average, "r")

        plt.title(f"for {v} nodes for {g_type} graph")
        plt.ylabel(f"Time for {d} density")
        plt.xlabel("Density")
        plt.savefig(f".venv/graphs/{g_type}_{v}_{d}.png")
        plt.close()