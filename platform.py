import json
import strategy
import time
import os
import sim
import random
import multiprocessing as mp


##RANK_LOOK_UP_TABLE = {0: 20, 
##                    1: 15, 
##                    2: 12, 
##                    3: 9, 
##                    4: 6, 
##                    5: 4, 
##                    6: 2, 
##                    7: 1}
RANK_LOOK_UP_TABLE = {0: 4, 
                    1: 3, 
                    2: 2, 
                    3: 1, 
                    4: 0, 
                    5: 0, 
                    6: 0, 
                    7: 0}

def work_sim(args):
    return sim.run(*args)

def get_score(sim_res, stg_idx):
    if len(sim_res) > 1:
        print('Dangerous! Right now I only write code compatible with one game run')
        exit(0)
    sim_res = sim_res[0][0]
    # sim_res will look like {"strategy1": 243, "strategy6": 121, ... }
    stg_rank = (sorted(sim_res, key=sim_res.get, reverse=True)).index(str(stg_idx))
    if stg_rank in RANK_LOOK_UP_TABLE:
        return RANK_LOOK_UP_TABLE[stg_rank]
    return 0

def convert_json_dict(fin_name):
    with open(fin_name, 'r') as fin:
        node_dict = json.load(fin)
    return node_dict

def load_maps(map_list_name):
    map_name_list = []
    
    print 'reading map list...'
    with open(map_list_name) as maps_name_file:
        content = maps_name_file.readlines()
        for line in content:
            map_name_list.append(line.strip())
            
    print 'there are {} maps'.format(len(map_name_list))
    
    i = 0
    #map_info: map_name, map_data, json_dict, n_players, n_seeds
    map_info = []        
    for map_name in map_name_list:
        start_time = time.time()
        
        i += 1 
        parser = map_name.split('.')
        n_players = int(parser[0])
        n_seeds = int(parser[1])
        print 'loading map {}:{}\t n_players={}\t n_seeds={}...'.format(i, map_name, n_players, n_seeds),
        # json_dict = convert_json_dict('maps\\' + map_name)
        json_dict = convert_json_dict(os.path.join('maps', map_name))
        
        # with open('maps\\' + '.'.join(parser[0:3]) + '.data', 'r') as input_file:
        with open(os.path.join('maps', '.'.join(parser[0:3])) + '.data', 'r') as input_file:
            data = json.load(input_file)
            data['graph'] = strategy.build_graph(json_dict)
        
        end_time = time.time()
        print 'finished in {:.3f} seconds'.format(end_time - start_time)
        map_info.append((map_name, data, json_dict, n_players, n_seeds))
    print '{} maps are loaded'.format(i)
    
    return map_info
        
def preprocess_maps(map_list_name):
    map_name_list = []
    
    print 'reading map list...'
    with open(map_list_name) as maps_name_file:
        content = maps_name_file.readlines()
        for line in content:
            map_name_list.append(line.strip())
            
    print 'there are {} maps'.format(len(map_name_list))
    
    i = 0        
    for map_name in map_name_list:
        start_time = time.time()
        
        i += 1 
        parser = map_name.split('.')
        n_players = int(parser[0])
        n_seeds = int(parser[1])
        print 'preprocessing map {}:{}, n_players={}, n_seeds={}...'.format(i, map_name, n_players, n_seeds),
        json_dict = convert_json_dict('maps\\' + map_name)
        data = strategy.preprocess(json_dict, False)
        
        end_time = time.time()
        
        with open('maps\\' + '.'.join(parser[0:3]) + '.data', 'w') as output_file:
            del data['graph']
            json.dump(data, output_file, sort_keys=True, indent=4)
            
        print 'finished in {:.3f} seconds'.format(end_time - start_time)
    
if __name__ == '__main__':
#     preprocess_maps('final_maps.txt')
    main_start_time = time.time()
    
    MAX_ITE = 100
    NUM_DEFAULT = 4
    NUM_WINNING = 16
    NUM_MUTATIONS = 16
    NUM_RANDOMS = 4
    NUM_STRATEGIES = NUM_WINNING + NUM_MUTATIONS + NUM_RANDOMS + NUM_DEFAULT
    map_info = load_maps('final_maps.txt')
    map_info_dict = {}
    for one_map_info in map_info:
        map_info_dict[one_map_info[0]] = one_map_info

    
    # for file_name in default_strategies_files:
    #     s = strategy.Strtg()
    #     s.read_from_file(os.path.join('training', 'default_strategies', file_name))
    #     default_strategies.append(s) 
        
    # load default strategies from the folder
    default_strategies = []
    default_nodes_list = []
    dft_stg_dir_name = os.path.join('training', 'default_strategies')
    default_strategies_dir = os.listdir(dft_stg_dir_name)
    for file_name in default_strategies_dir:
        s = strategy.Strtg()
        s.read_from_file(os.path.join(dft_stg_dir_name, file_name))
        default_strategies.append(s)
        default_nodes = {}
        for one_map_info in map_info:
            map_name, map_data, json_dict, n_players, n_seeds = one_map_info
            default_nodes[map_name] = s.get_nodes(map_data, n_players, n_seeds)
        default_nodes_list.append(default_nodes)


    last_step_strategies = {}


    steps_dir = os.path.join('training', 'iterations')
    ite_folders = [int(ite_folder) for ite_folder in os.listdir(steps_dir) if ite_folder.isdigit()]
    if len(ite_folders) == 1:
        ITE_CUR = 0
    else:
        ite_folders.sort(reverse=True)
        
        #----------------------------------------changed
        ITE_CUR = ite_folders[0]

    for ITE_NUM in range(ITE_CUR, MAX_ITE):
        print('Iteration Number = {}'.format(ITE_NUM))
        last_step_dir = os.path.join('training', 'iterations', str(ITE_NUM))
        last_step_strategies_names = os.listdir(last_step_dir)

        # obtain all strategies and load them into last_step_strategies
        for file_name in last_step_strategies_names:
            s = strategy.Strtg()
            # s.read_from_file(last_step_dir + file_name)
            s.read_from_file(os.path.join(last_step_dir, file_name))
            # last_step_strategies.append(s)
            stg_idx = int(file_name[:-5])
            last_step_strategies[stg_idx] = strategy.mutate(s)
            print stg_idx, last_step_strategies[stg_idx]




        # --------------------- Minfa edited begins ---------------------
        # for every strategy in strategies
        # get strategy nodes for each map 
            # stg_nodes = {map_name: [nodes_chosen]}
            # => stg_nodes_dict = {stg_idx: stg_nodes}
        # let each strategy run every map, randomly selecting other strategy as competitors.
            # for each stg_idx in stg_nodes_dict:
                # map_score = 0
                # for map_name in stg_nodes:
                    # self_nodes_chosen = stg_nodes[map_name]
                    # other_nodes_chosen = ...
                    # nodes = {st1: [self_nodes_chosen], st2: [], ...}
                    # sim.run()
                    # map_score += map score with randomly chosen competitors
                # rank_dict[stg_idx] = map_score
        # choose 16 stg_idx from rank_dict with highest map_score
        stg_nodes_dict = {}
        rank_dict = {}

        # stg_idx will range from 0 to NUM_WINNING
        # stg_nodes = {}  HUGGGGGGGE BUGGGGGG
        for stg_idx, stg in last_step_strategies.items():
#             print stg_idx, stg
            stg_nodes = {}
            for one_map_info in map_info:                
                map_name, map_data, json_dict, n_players, n_seeds = one_map_info
                stg_nodes[map_name] = stg.get_nodes(map_data, n_players, n_seeds)
#                 print stg_nodes[map_name]
            stg_nodes_dict[stg_idx] = stg_nodes
            
#         for k, v in stg_nodes_dict.items():
#             print k, id(v)

        # add more strategies here
        # mutations
        # randoms
        
        last_step_stg_list = last_step_strategies.values()
        mutate_group = strategy.generate_mutation_group(last_step_stg_list, NUM_MUTATIONS)
        for stg_idx in range(NUM_MUTATIONS):
            mut_stg_nodes = {}
            mut_stg_idx = stg_idx + NUM_WINNING
            mut_s = mutate_group[stg_idx]
            for one_map_info in map_info:
                map_name, map_data, json_dict, n_players, n_seeds = one_map_info
                mut_stg_nodes[map_name] = mut_s.get_nodes(map_data, n_players, n_seeds)
            stg_nodes_dict[mut_stg_idx] = mut_stg_nodes
            last_step_strategies[mut_stg_idx] = mut_s


        
        for stg_idx in range(NUM_RANDOMS):
            rand_stg_idx = stg_idx + NUM_WINNING + NUM_MUTATIONS
            s = strategy.Strtg()
            s.random_weight(strategy.preprocess({}))
            rand_stg_nodes = {}
            for one_map_info in map_info:
                map_name, map_data, json_dict, n_players, n_seeds = one_map_info
                rand_stg_nodes[map_name] = s.get_nodes(map_data, n_players, n_seeds)
            stg_nodes_dict[rand_stg_idx] = rand_stg_nodes
            last_step_strategies[rand_stg_idx] = s


        # default_strategies = [s]
        # default_nodes = {map_name: nodes}
        # default_nodes_list = [default_nodes]
        for stg_idx in range(NUM_DEFAULT):
            dft_stg_idx = stg_idx + NUM_WINNING + NUM_MUTATIONS + NUM_RANDOMS
            stg_nodes_dict[dft_stg_idx] = default_nodes_list[stg_idx]
            last_step_strategies[dft_stg_idx] = default_strategies[stg_idx]


        # ---------------------- Below are competitions -------------------
        count = 0
        pool = mp.Pool(4) 
        for stg_idx, stg_nodes in stg_nodes_dict.items():
#             print stg_idx
#             print stg_nodes
            if stg_idx >= NUM_STRATEGIES - NUM_DEFAULT:
                continue
            print 'running node {}...'.format(stg_idx),
            count += 1
            
            map_score = 0
            
            
            args_sim = []
            #changed
            for i_boost in range(4):
                for map_name, self_nodes_chosen in stg_nodes.items():
                    nodes = {}
                    nodes[str(stg_idx)] = [self_nodes_chosen]
                    
    
                    # make other_nodes_chosen
                    play_map_info = map_info_dict[map_name]
                    map_name, map_data, json_dict, n_players, n_seeds = play_map_info
                    # other_nodes_chosen_list = []
                    players_in_game = {stg_idx}
                    for one_player in range(2-1):
                        rand_idx = random.randrange(0, NUM_STRATEGIES - NUM_DEFAULT)
                        while rand_idx in players_in_game:
                            rand_idx = random.randrange(0, NUM_STRATEGIES - NUM_DEFAULT)
                        players_in_game.add(rand_idx)
                        other_stg_nodes = stg_nodes_dict[rand_idx]
                        other_nodes_chosen = other_stg_nodes[map_name]
    
                        nodes[str(rand_idx)] = [other_nodes_chosen]
                        # other_nodes_chosen_list.append(other_nodes_chosen)
                    args_sim.append((json_dict, nodes, 1))
                    
            score1 = 0
            sim_res_list = pool.map(work_sim, args_sim)    
            for sim_res in sim_res_list:
                score1 += get_score(sim_res, stg_idx)
                
            score1 = score1 - 12 * len(stg_nodes)
            
            args_sim = []        
            for i_boost in range(1):
                for map_name, self_nodes_chosen in stg_nodes.items():
                    nodes = {}
                    nodes[str(stg_idx)] = [self_nodes_chosen]
                    
    
                    # make other_nodes_chosen
                    play_map_info = map_info_dict[map_name]
                    map_name, map_data, json_dict, n_players, n_seeds = play_map_info
                    # other_nodes_chosen_list = []
                    players_in_game = {stg_idx}
                    for one_player in range(NUM_DEFAULT):
                        rand_idx = NUM_STRATEGIES - NUM_DEFAULT + one_player
                        players_in_game.add(rand_idx)
                        other_stg_nodes = stg_nodes_dict[rand_idx]
                        other_nodes_chosen = other_stg_nodes[map_name]
    
                        nodes[str(rand_idx)] = [other_nodes_chosen]
                        # other_nodes_chosen_list.append(other_nodes_chosen)
                    args_sim.append((json_dict, nodes, 1))
            score2 = 0    
            sim_res_list = pool.map(work_sim, args_sim)    
            for sim_res in sim_res_list:
                # print sim_res[0][0]
#                 print sim_res
                score2 += get_score(sim_res, stg_idx)
            map_score = score1 + score2

            print '{}, {}, {}'.format(score1, score2, map_score)
            rank_dict[stg_idx] = map_score
            
        pool.close()
        pool.join()

        # rank_stg_idx_list is a sorted list of stg_idx
        rank_stg_idx_list = sorted(rank_dict, key=rank_dict.get, reverse=True)
        rank_list = [(stg_idx, rank_dict[stg_idx]) for stg_idx in sorted(rank_dict, key=rank_dict.get, reverse=True)]
        for idx, score in rank_list:
            stg = last_step_strategies[idx]
            print idx, score, stg

        new_path = os.path.join('training', 'iterations', str(ITE_NUM+1))
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        for i in range(NUM_WINNING):
            stg_idx = rank_stg_idx_list[i]
            stg = last_step_strategies[stg_idx]
            stg.write_to_file(os.path.join(new_path, '{}.json'.format(i)))




        # --------------------- Minfa edited ends --------------------


