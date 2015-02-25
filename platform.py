import json
import strategy
import time
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
    #map_info: map_name, map_data, n_players, n_seeds, json_dict
    map_info = []        
    for map_name in map_name_list:
        start_time = time.time()
        
        i += 1 
        parser = map_name.split('.')
        n_players = parser[0]
        n_seeds = parser[1]
        print 'loading map {}:{}\t n_players={}\t n_seeds={}...'.format(i, map_name, n_players, n_seeds),
        json_dict = convert_json_dict('maps\\' + map_name)
        
        with open('maps\\' + '.'.join(parser[0:3]) + '.data', 'r') as input_file:
            data = json.load(input_file)
            data['graph'] = strategy.build_graph(json_dict)
        
        end_time = time.time()
        print 'finished in {:.3f} seconds'.format(end_time - start_time)
        map_info.append((map_name, data, n_players, n_seeds, json_dict))
    print '{} maps are loaded'.format(i)
    
    return map_list_name
        
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
    load_maps('all_maps.txt')