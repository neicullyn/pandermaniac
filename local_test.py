import sim
import json
import time
from strategy import Strtg, preprocess

def convert_txt_list(fin_name, num_seeds, num_games):
	result_list = []
	games_played = 0
	with open(fin_name, 'r') as fin:
		i = 0
		nodes_one_game = []
		for line in fin:
			i += 1
			nodes_one_game.append(line.strip())
			if i % num_seeds == 0:
				result_list.append(nodes_one_game)
				nodes_one_game = []
				games_played += 1
				if games_played == num_games:
					break
	return result_list


def convert_json_dict(fin_name):
	with open(fin_name, 'r') as fin:
		node_dict = json.load(fin)
	return node_dict


def local_run(json_file, f1_player, f2_player):
	NUM_GAMES = 1
	num_seeds = int(json_file.split('.')[1])
# 	f1_player = convert_txt_list(f1_name, num_seeds, NUM_GAMES)
# 	f2_player = convert_txt_list(f2_name, num_seeds, NUM_GAMES)

	nodes = {'strategy1': f1_player,
			'strategy2': f2_player}

	graph = convert_json_dict(json_file)
	result = sim.run(graph, nodes, NUM_GAMES)
	print(result)

# if __name__ == '__main__':
# 	import argparse
# 	parser = argparse.ArgumentParser()
# 	parser.add_argument('json_file')
# 	parser.add_argument('f1')
# 	parser.add_argument('f2')
# 	args = parser.parse_args()
# 
# 	local_run(args.json_file, args.f1, args.f2)

if __name__ == '__main__':
# 	json_file = '8.20.01.json'
# 	json_file = '8.35.2.json'
# 	json_file = '4.5.01.json'
	json_file = '2.5.01.json'
# 	json_file = '4.10.01.json'
	node_dict = convert_json_dict(json_file)
	
	start_time = time.time()
	data = preprocess(node_dict)
	end_time = time.time()
	print 'preprocess: {}'.format(end_time - start_time)
	
	strategy1 = Strtg()
	strategy1.random_weight(data)
# 	strategy1.read_from_file('strtg\\beat_degree.json')
	for key in strategy1.weights:
		strategy1.weights[key] = 0
	strategy1.weights['closeness_centrality'] = 0.8
	strategy1.weights['clustering'] = 0.12
	strategy1.weights['neighbor_number_1'] = 0.5
	strategy1.weights['neighbor_number_2'] = 0.2
	strategy1.weights['neighbor_number_3'] = 0.04
	strategy1.weights['between_node'] = 0.4
	strategy1.write_to_file('strtg\\beat_degree.json')
 	
	print strategy1.weights
	strategy2 = Strtg()
	strategy2.random_weight(data)
	print strategy2.weights
# 	for key in strategy2.weights:
# 		strategy2.weights[key] = 0
# 	strategy2.weights['degree_centrality'] = 1
# 	strategy2.weights['closeness_centrality'] = 1
# 	strategy2.read_from_file('strtg\\beat_degree2.json')

	start_time = time.time()
	player1 = [strategy1.get_nodes(data, 2, 35)]
	player2 = [strategy2.get_nodes(data, 2, 35)]
	end_time = time.time()
	print 'two strategy: {}'.format(end_time - start_time)
	
	start_time = time.time()
	local_run(json_file, player1, player2)
	end_time = time.time()
	print 'run graph: {}'.format(end_time - start_time)