# Imports
import timeit
import numpy as np
from collections import Counter
from itertools import product, chain
from printUtils import printTime
from vsdc48 import load_dimacs, containsComplementPair

# Returns:
# The watched literal set
# The number of variables
# The frequency order of variables
def dictify(clause_set):
    # Create empty dict
    watched_literals = {}
    # Count all literals
    vars = Counter(chain.from_iterable(clause_set))
    
    # Initial each key in the dict with an empty list
    for var in vars.keys():
        watched_literals[var] = []
    
    # List for unit literals found in the initial clause_set
    initial_unit_literals = []
    # 
    for clause in clause_set:
        if len(clause) == 1:
            initial_unit_literals.append(clause[0])
            continue
        watched_literals[clause[0]].append(clause)
        watched_literals[clause[1]].append(clause)

    return watched_literals, initial_unit_literals, numVars(vars), orderVars(vars)

def numVars(vars):
    # print(len(np.unique(np.array([np.abs(kv) for kv in vars]))))
    return len(np.unique(np.array([np.abs(kv) for kv in vars])))

def orderVars(vars):
    order = []
    for var in vars.most_common():
        if -1 * var[0] not in order:
            order.append(var[0])
    return order

def dpll_sat_solve():
    return

def setVar():
    return







clauses = load_dimacs('instances/8queens.txt')

printTime(np.mean(timeit.repeat('dictify(clauses)', globals=globals(), number=100, repeat=10)))
