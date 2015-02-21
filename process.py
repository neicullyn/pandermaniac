import json
# import networkx


# main thing we need to fill in
# we need to return a list of nodes with length num_seeds
def select_nodes(node_dict, num_seeds):
	print(node_dict)
	nodes_chosen = [str(i+5) for i in range(num_seeds)]

	return nodes_chosen













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