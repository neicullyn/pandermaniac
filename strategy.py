import json
import time
from itertools import repeat
import multiprocessing as mp
import networkx as nx
import random

def convert_json_dict(fin_name):
    with open(fin_name, 'r') as fin:
        node_dict = json.load(fin)
    return node_dict

# def build_graph_snap(node_dict):
#     G = snap.TUNGraph().New()
#     for node in node_dict:
#         G.AddNode(int(node))
#     for node in node_dict:
#         for to_node in node_dict[node]:
#             G.AddEdge(int(node), int(to_node))    
#     return G

def build_graph(node_dict):
    G = nx.Graph()
    for node in node_dict:
        for to_node in node_dict[node]:
            G.add_edge(node, to_node)
    return G

def calculate_dist_and_neighbors(args):
    node_dict, node = args
   
    neighbors1 = set()
    neighbors2 = set()
    neighbors3 = set()

    neighbors1.update(node_dict[node])
    for x in neighbors1:
        neighbors2.update(node_dict[x])
        
    neighbors2.difference_update(neighbors1)    
    
    for x in neighbors2:
        neighbors3.update(node_dict[x])
        
    neighbors3.difference_update(neighbors1)  
    neighbors3.difference_update(neighbors2)  
       
    n1 = len(neighbors1)    
    n2 = len(neighbors2)
    n3 = len(neighbors3)
    
   
    return node, n1, n2, n3
    


def preprocess(node_dict, debug=False):
    #default distance
    #if the distance is larger than 3, let the distace be 5
    default_distance = 5
    N = len(node_dict)
    #multiprocessing
    pool = mp.Pool(4)
    #use a dictionary to save data
    
    G = build_graph(node_dict)
    
    data = {}

    data['graph'] = G

    nodes = node_dict.keys()
    
    if debug:
        print 'computing degree_centrality...'
    table = {}
    for node, val in node_dict.items():
        table[node] = 1.0 * len(val) / N    

    data['degree_centrality'] = table

     
    if debug:
        print 'computing distance and number of neighbors...'
      
    args = zip(repeat(node_dict, len(node_dict)), node_dict.keys())
      
    lst = pool.map(calculate_dist_and_neighbors, args)
      
    data['neighbor_number_1'] = {}
    data['neighbor_number_2'] = {}
    data['neighbor_number_3'] = {}
    
    for node, n1, n2, n3 in lst:
        data['neighbor_number_1'][node] = 1.0 * n1 / N
        data['neighbor_number_2'][node] = 1.0 * n2 / N
        data['neighbor_number_3'][node] = 1.0 * n3 / N
        
    if debug:
        print 'computing closeness_centrality...'
        
    table = {}    
    for node in nodes:
        n1, n2, n3 = data['neighbor_number_1'][node] * N, data['neighbor_number_2'][node] * N, data['neighbor_number_3'][node] * N
        c = n1 + n2 * 2 + n3 * 3
        c = c + default_distance * (N - n1 - n2 - n3)
        c = (N - 1) * 1.0 / c
        table[node] = c
    data['closeness_centrality'] = table
    
    if debug:
        print 'computing clustering...'
    table = nx.clustering(G, nodes)
    
    data['clustering'] = table   
    
    return data
          
#     for x in lst:
#         print x
        
    
#     data['closeness_centrality'] = nx.closeness_centrality(G)

class Strtg:
    def __init__(self):
        pass
    
    def random_weight(self, data):
        self.weights = {}
        
        for key in data.keys():
            if key != 'graph':
                self.weights[key] = random.random()
                
        self.weights['between_node'] = random.random()
        self.weights['rand_range'] = random.random()  
        pass
    
    def read_from_file(self, file_name):
        with open(file_name, 'r') as input_file:
            self.weights = json.load(input_file)
    
    def write_to_file(self, file_name):
        with open(file_name, 'w') as output_file:
            json.dump(self.weights, output_file, sort_keys=True, indent=4) 
    
    def get_nodes(self, data, n_player, n_nodes):
        scores = []
        nodes = data['graph'].nodes()
        for node in nodes:
            s = 0
            for key in data.keys():
                if key != 'graph':
                    s += self.weights[key] * data[key][node]
            scores.append((s, node))
            
        scores.sort(reverse=True)
        
        scores = scores[0 : min(n_nodes * 3, len(scores))]
        scores_with_dist = []
        for s, src_node in scores:
            dist = 0
            for ss, dst_node in scores:
                if src_node != dst_node:
                    dist += nx.shortest_path_length(data['graph'], src_node, dst_node)
            dist = 1.0 * dist / (len(scores) - 1) - 1
            scores_with_dist.append((s + dist * self.weights['between_node'], src_node ))
        

        scores_with_dist.sort(reverse=True)
        rst = zip(*scores_with_dist)[1]
                
#         sorted_nodes = list(zip(*scores)[1])
#         
#         determine_nodes = 
        
#         random_range = int(n_nodes * (1 + self.weights['rand_range'] * n_player))
#         random_range = min(random_range, len(nodes))
#         
#         shuffle_nodes = sorted_nodes[0 : random_range]
#         random.shuffle(shuffle_nodes)
        
        return rst
        
    
    
if __name__ == '__main__':
    
    
    input_graph = '8.35.2.json'
#     input_graph = '8.20.01.json'
    node_dict = convert_json_dict(input_graph)
    
    
    start_time = time.time()
    
    data = preprocess(node_dict, debug=True)
    
    end_time = time.time()    
    time_elapsed = end_time - start_time    
    print time_elapsed
    
    
    start_time = time.time()
    
    my_strategy = Strtg()
    
    my_strategy.random_weight(data)
    nodes = my_strategy.get_nodes(data, 8, 4)
    
    end_time = time.time()    
    time_elapsed = end_time - start_time    
    print time_elapsed
    

    