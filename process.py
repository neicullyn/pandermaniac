import json
import networkx as nx
import time


# main thing we need to fill in
# we need to return a list of nodes with length num_seeds
def select_nodes(node_dict, num_seeds):
	start = time.time()
	nodes_chosen = [str(i+5) for i in range(num_seeds)]

	# convert dict to networkx graph structure
	G = nx.Graph()
	for node in node_dict:
		for to_node in node_dict[node]:
			G.add_edge(node, to_node)


	neighbor_dict = {}
	for node in G.nodes():
		to_visit = [node]
		visited_neighbors = {}
		for i in range(3):
			next_visit = []
			for n_v in to_visit:
				neighbors = G.neighbors(n_v)
				for nb in neighbors:
					if nb not in visited_neighbors:
						visited_neighbors[nb] = None
						next_visit.append(nb)
			to_visit = next_visit
		neighbor_dict[node] = len(visited_neighbors)




	# close_dict = nx.closeness_centrality(G)
	# lengh_dict = nx.shortest_path_length(G)
	result_list = []
	for node, value in neighbor_dict.items():
		result_list.append((value, node))
	result_list.sort(reverse=True)
	print(result_list[:num_seeds])
	# for item in close_list:
		# print(item)

	print('{}'.format(time.time()-start))

	# return nodes_chosen
	return [pair[1] for pair in result_list[:num_seeds]]













# ----------------------- no need to touch ----------------
def read_file(fin_name):
	with open(fin_name, 'r') as fin:
		node_dict = json.load(fin)
	return node_dict

def write_file(fin_name, nodes):
	RECURSIONS = 50
	fout_name = fin_name[:-4] + 'out.txt'
	with open(fout_name, 'w') as fout:
		for i in range(RECURSIONS):
			for node in nodes:
				fout.write(node+'\n')

	print('Finished writing to {}'.format(fout_name))


def process_file(fin_name):
	node_dict = read_file(fin_name)
	num_seeds = int(fin_name.split('.')[1])
	nodes_chosen = select_nodes(node_dict, num_seeds)
	write_file(fin_name, nodes_chosen)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('f_name', default='2.5.01')
	args = parser.parse_args()
	fin_name = args.f_name + '.json'

	process_file(fin_name)