import json
import networkx as nx
import time
from local_test import convert_json_dict
from itertools import repeat
import multiprocessing as mp

def build_graph(node_dict):
    G = nx.Graph()
    for node in node_dict:
        for to_node in node_dict[node]:
            G.add_edge(node, to_node)    
    return G

def calculate_neighbors_number(args):
    G, node = args
    
    neighbors1 = set()
    neighbors2 = set()

    neighbors1.update(G.neighbors(node))
    for x in neighbors1:
        neighbors2.update(G.neighbors(x))
        
    neighbors2.difference_update(neighbors1)    
    
    n3 = 0
    for x in neighbors2:
        n3 += len(G.neighbors(x))
        
    n1 = len(neighbors1)    
    n2 = len(neighbors2)
    
    return node, n1, n2, n3
    
    

def preprocess(G, debug=False):
    #multiprocessing
    pool = mp.Pool(4)
    #use a dictionary to save data
    data = {}
   
    data['Graph'] = G
   
    if debug:
        print 'computing degree_centrality...'
    data['degree_centrality'] = nx.degree_centrality(G)
    
    if debug:
        print 'computing number of neighbors...'
    nodes = G.nodes()
    
    args = zip(repeat(G, len(nodes)), nodes)
    
    lst = pool.map(calculate_neighbors_number, args)
    
    data['neighbor_number_1'] = {}
    data['neighbor_number_2'] = {}
    data['neighbor_number_3'] = {}
    
    for node, n1, n2, n3 in lst:
        data['neighbor_number_1'][node] = n1
        data['neighbor_number_2'][node] = n2
        data['neighbor_number_3'][node] = n3
        
    print
        
    
#     data['closeness_centrality'] = nx.closeness_centrality(G)
    
if __name__ == '__main__':
    start_time = time.time()
    
    input_graph = '8.20.01.json'
    node_dict = convert_json_dict(input_graph)
    
    G = build_graph(node_dict)
    
    data = preprocess(G, debug=True)
    
    end_time = time.time()
    
    time_elapsed = end_time - start_time
    
    print time_elapsed
    