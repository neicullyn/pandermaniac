import sim
import json

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


def local_run(json_file, f1_name, f2_name):
	NUM_GAMES = 1
	num_seeds = int(json_file.split('.')[1])
	f1_player = convert_txt_list(f1_name, num_seeds, NUM_GAMES)
	f2_player = convert_txt_list(f2_name, num_seeds, NUM_GAMES)

	nodes = {'strategy1': f1_player,
			'strategy2': f2_player}

	graph = convert_json_dict(json_file+'.json')
	result = sim.run(graph, nodes, NUM_GAMES)
	print(result)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('json_file')
	parser.add_argument('f1')
	parser.add_argument('f2')
	args = parser.parse_args()

	local_run(args.json_file, args.f1, args.f2)