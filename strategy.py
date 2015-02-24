import json
import snap
import time
from local_test import convert_json_dict
from itertools import repeat
import multiprocessing as mp


def build_graph(node_dict):
    G = snap.TUNGraph().New()
    for node in node_dict:
        G.AddNode(int(node))
    for node in node_dict:
        for to_node in node_dict[node]:
            G.AddEdge(int(node), int(to_node))    
    return G

def calculate_neighbors_number(args):
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
    #multiprocessing
    pool = mp.Pool(4)
    #use a dictionary to save data
    data = {}
   
    G = build_graph(node_dict)
   
    data['Graph'] = G
   
    if debug:
        print 'computing degree_centrality...'
    table = {}
    for node in G.Nodes():
        table[node.GetId()] = snap.GetDegreeCentr(G, node.GetId())
    
    data['degree_centrality'] = table
    
#     if debug:
#         print 'computing closeness_centrality...'
#     table = {}
#     for node in G.Nodes():
#         table[node.GetId()] = snap.GetClosenessCentr(G, node.GetId())
#     data['closeness_centrality'] = table
    
    if debug:
        print 'computing distances...'
    table = {}
    for node in G.Nodes():
        d = snap.TIntH()
        key_val_vector = snap.TIntPrV()
        snap.GetShortPath(G, node.GetId(), d, False, 3)
        d.GetKeyDatPrV(key_val_vector)
        
        table_d = {}
        table[node.GetId()] = table_d
        for pair in key_val_vector:
            key = pair.Val1.Val
            val = pair.Val2.Val
            table_d[key] = val
    data['distances'] = table
        
#     if debug:
#         print 'computing number of neighbors...'
#     table1 = {}
#     table2 = {}
#     table3 = {}
#     for node in G.Nodes():
#         id =node.GetId()
#         n1 = 0
#         n2 = 0
#         n3 = 0
#         dis = data['distances'][id]
#         vals = snap.TIntV()
#         dis.GetDatV(vals)
#         for val in vals:
#             if val == 1:
#                 n1 += 1
#             if val == 2:
#                 n2 += 1
#             if val == 3:
#                 n3 += 1
#         table1[id] = n1
#         table2[id] = n2
#         table3[id] = n3
        
    
                
    
    if debug:
        print 'computing closeness_centrality...'
        

    
    
#     if debug:
#         print 'computing number of neighbors...'
#      
#      
#     args = zip(repeat(node_dict, len(node_dict)), node_dict.keys())
#      
#     lst = pool.map(calculate_neighbors_number, args)
#      
#     data['neighbor_number_1'] = {}
#     data['neighbor_number_2'] = {}
#     data['neighbor_number_3'] = {}
#      
#     for node, n1, n2, n3 in lst:
#         data['neighbor_number_1'][int(node)] = n1
#         data['neighbor_number_2'][int(node)] = n2
#         data['neighbor_number_3'][int(node)] = n3
         
#     for x in lst:
#         print x
        
    
#     data['closeness_centrality'] = nx.closeness_centrality(G)
    
if __name__ == '__main__':
    start_time = time.time()
    
#     input_graph = '8.35.2.json'
    input_graph = '8.20.01.json'
    node_dict = convert_json_dict(input_graph)
    
    
    
    data = preprocess(node_dict, debug=True)
    
    end_time = time.time()
    
    time_elapsed = end_time - start_time
    
    print time_elapsed
    