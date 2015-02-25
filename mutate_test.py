from strategy import Strtg, mutate, swap, cross, generate_mutation_group
from strategy import preprocess

if __name__ == '__main__':
    data = preprocess({}, False)
    print data
     
    s1 = Strtg()
    s1.random_weight(data)
    
    s2 = Strtg()
    s2.random_weight(data)
    
    src_group = [s1, s2]
    mutate_group = generate_mutation_group(src_group, 16)
    s1.write_to_file('sta.json')
    for x in src_group:
        print x
    for x in mutate_group:
        print x