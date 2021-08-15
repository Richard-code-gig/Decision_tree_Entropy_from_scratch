from collections import Counter, defaultdict
from math import log

"""This programme tries to describe the principle of decision tree from scratch"""
"""From scratch means no external library like NumPy, Pandas or scikit-learn is used"""
"""The design was made simple to make it appropriate for the targetted audience"""

data = [
       ['sunny', 'hot', 'high'],
       ['sunny', 'hot', 'high'],
       ['overcast', 'hot', 'high'],
       ['rainy', 'mild', 'high'],
       ['rainy', 'cool', 'normal'],
       ['overcast', 'cool', 'normal'],
       ['sunny', 'mild', 'normal'],
]   

def entropy(label):
    return sum(-x * log (x, 2) for x in label if x)    

def distinct_prob(data):
    label = [x for row in data for x in row]
    total_count = len(data)
    prob_count =  [count/total_count for count in Counter(label).values()]
    return prob_count
    
def gain(data):
    total_count = len(data)
    labels = [x for x in data]
    counts = [val for _, _, val in labels]
    prob_count =  [count/total_count for count in Counter(counts).values()]
    return entropy(prob_count)

def make_dict(data):
    s1 = defaultdict(list)
    for arr in data:
        key = arr[0]
        s1[key].append(arr[2]) 
    return s1

def make_dict2(data):
    s1 = defaultdict(list)
    for arr in data:
        key = arr[1]
        s1[key].append(arr[2]) 
    return s1

def list_of_make_dict(elem):
    s1 = []
    turn_dict = make_dict(elem)
    for i, v in turn_dict.items():
        s1.append([i, v])   
    return s1

def list_of_make_dict2(elem):
    s1 = []
    turn_dict = make_dict2(elem)
    for i, v in turn_dict.items():
        s1.append([i, v])   
    return s1

def count_elem(data):
    x = list_of_make_dict(data)
    s = defaultdict(list)
    for i in x:
        a, b = i
        count = Counter(b)
        s[a].append(count)
    return s

def count_elem2(data):
    x = list_of_make_dict2(data)
    s = defaultdict(list)
    for i in x:
        a, b = i
        count = Counter(b)
        s[a].append(count)
    return s


def prob_of_elem(attr, data):
    if attr == 'sunny' or attr == 'overcast' or attr == 'rainy':
        a = count_elem(data)
    else:
        a = count_elem2(data)
    for i in a[attr]:
        partition = [i['high'], i['normal']]
    total_count = sum(partition)
    prob_count =  [count/total_count for count in partition]
    return prob_count

def gain_elem(attr, data):
    ent_elem = prob_of_elem(attr, data)
    hg, nm = ent_elem
    try:
       ent_hg = -hg * log(hg, 2)
    except ValueError:
        ent_hg = 0
    try:
        ent_nm = -nm * log(nm, 2)
    except ValueError:
        ent_nm = 0
    return ent_hg + ent_nm
         
def gain_data(attr1, attr2, data):
    s = []
    s1 = []
    for i in attr1:
        s.append(gain_elem(i, data))
    for x in attr2:
        s1.append(gain_elem(x, data))
    return s, s1
    
def gain_overcast(data):
     return gain_elem('overcast', data)

def gain_rainy(data):
     return gain_elem('rainy', data)

def total_prob_elem(attr, data):
    label = [x for row in data for x in row]
    total_count = len(data)
    for i, v in Counter(label).items():
        if i == attr:
            return v/total_count

def total_info_gain(attr1, data):
    s = []
    s1 = []
    for i in attr1:
        s.append(total_prob_elem(i, data))
        s1.append(gain_elem(i, data))
    return sum(val1 * val2 for val1, val2 in zip(s, s1))


attr1 = ['sunny', 'overcast', 'rainy']
attr2 = ['hot', 'mild', 'cool']
each_gain = gain_data(attr1, attr2, data)
ent_attr1 = gain(data) - total_info_gain(attr1, data)
ent_attr2 = gain(data) - total_info_gain(attr2, data)

if ent_attr1 > ent_attr2:
    root_max = max(each_gain[0])
    if root_max == each_gain[0][0]:
        root_result = 'sunny'
    elif root_max == each_gain[0][1]:
        root_result = 'overcast'
    else:
        root_result = 'rainy'
    print(f'The root node is {root_result} from the first row')
else:
    root_max2 = max(each_gain[1])
    if root_max2 == each_gain[1][0]:
        root_result2 = 'hot'
    elif root_max2 == each_gain[1][1]:
        root_result2 = 'mild'
    else:
        root_result2 = 'cool'
    print(f'The root node is {root_result2} from the second row')