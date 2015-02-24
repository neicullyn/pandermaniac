#     if debug:
#         print 'computing closeness_centrality...'
#     table = {}
#     for node in G.Nodes():
#         table[node.GetId()] = snap.GetClosenessCentr(G, node.GetId())
#     data['closeness_centrality'] = table
    
#     if debug:
#         print 'computing distances...'
#     table = {}
#     for node in G.Nodes():
#         d = snap.TIntH()
#         key_val_vector = snap.TIntPrV()
#         snap.GetShortPath(G, node.GetId(), d, False, 3)
#         d.GetKeyDatPrV(key_val_vector)
#         
#         table_d = {}
#         table[node.GetId()] = table_d
#         for pair in key_val_vector:
#             key = pair.Val1.Val
#             val = pair.Val2.Val
#             table_d[key] = val
#     data['distances'] = table