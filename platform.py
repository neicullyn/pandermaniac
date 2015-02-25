import json
import strategy
import time
import os
import sim
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
        json_dict = convert_json_dict('maps\\' + map_name)
        
        with open('maps\\' + '.'.join(parser[0:3]) + '.data', 'r') as input_file:
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
    
    map_info = load_maps('test_maps.txt')
    
    # load default strategies from the folder
    default_strategies = []
    default_strategies_files = os.listdir('training\\default_strategies\\')
    
    for file_name in default_strategies_files:
        s = strategy.Strtg()
        s.read_from_file('training\\default_strategies\\' + file_name)
        default_strategies.append(s) 
        
    for s in default_strategies:
        print s
        
#     os.makedirs('training\\iterations\\0\\')
#     for i in range(16):
#         s = strategy.Strtg()
#         s.random_weight(strategy.preprocess({}))
#         s.write_to_file('training\\iterations\\0\\' + '{}.json'.format(i))
    last_step_strategies = []
    last_step_dir = 'training\\iterations\\0\\'
    last_step_strategies_names = os.listdir(last_step_dir)
    for file_name in last_step_strategies_names:
        s = strategy.Strtg()
        s.read_from_file(last_step_dir + file_name)
        last_step_strategies.append(s)
    
    for s in last_step_strategies:
        print s
    
    map_name, map_data, json_dict, n_players, n_seeds = map_info[2]
    nodes1 = last_step_strategies[0].get_nodes(map_data, n_players, n_seeds)
    nodes2 = last_step_strategies[1].get_nodes(map_data, n_players, n_seeds)
    
    nodes = {'strategy1': [nodes1],
             'strategy2': [nodes2]}
    
    start_time = time.time()
    print sim.run(json_dict, nodes, 1)
    end_time = time.time()
    print end_time - start_time
    
        