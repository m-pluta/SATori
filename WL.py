# Imports
import timeit
import numpy as np
from collections import Counter
from itertools import product, chain
from printUtils import printTime
from vsdc48 import load_dimacs, containsComplementPair

def orderVars(vars):
    order = []
    for var in vars.most_common():
        if -1 * var[0] not in order:
            order.append(var[0])
    return order

def createPartialAssignment(vars):
    return dict.fromkeys([abs(var) for var in vars], 0)
'''
The watched literal dict
The initial unit_literals
The frequency order of variables
'''
def dictify(clause_set):
    # Count all literals
    vars = Counter(chain.from_iterable(clause_set))
    order = orderVars(vars)
    
    # Initialise each key in the dict with an empty list
    watched_literals = {}
    for var in order:
        watched_literals[var] = []
        watched_literals[-1 * var] = []

    print(watched_literals)
    # Potential alternative:
    # watched_literals = dict.fromkeys(vars.keys(), [])
    
    # List for unit literals found in the initial clause_set
    initial_unit_literals = set()

    for clause in clause_set:
        if len(clause) == 1:
            initial_unit_literals.add(clause[0])
            continue
        watched_literals[clause[0]].append(clause)
        watched_literals[clause[1]].append(clause)

    return watched_literals, initial_unit_literals, order

def dpll_sat_solve(clause_set, partial_assignment=[]):
    dict, u_literals, orderVars = dictify(clause_set)
    p_assignment = createPartialAssignment(orderVars)
    result = backtrack(dict, p_assignment, u_literals, orderVars)
    return result if result else False

def backtrack(dict, partial_assignment, u_literals, orderVars):
    # if u_literals:
    #     dict = unit_propagate(dict, u_literals)
        # Add unit literals

    if 0 not in partial_assignment.values():
        return partial_assignment
    
    # if Φ contains an empty clause then
    #     return false

    nextVariable = getNextVariable(orderVars, partial_assignment)

    for t in [1, -1]:
        branchLiteral = t * nextVariable
        units = setVar(dict, branchLiteral, partial_assignment)
        result = backtrack(dict, partial_assignment, units, orderVars)
        if result:
            return result
        partial_assignment[abs(branchLiteral)] = 0

    return

def setVar(dict, var, partial_assignment):
    units = set()
    partial_assignment[abs(var)] = var

    for clause in dict[-1 * var]:
        isUnit, newLiteral = nextWatchLiteral(dict, clause, partial_assignment)
        if isUnit:
            units.add(newLiteral)
        elif newLiteral:
            dict[newLiteral].append(clause)
            dict[-1 * var].remove(clause)

def nextWatchLiteral(dict, clause, partial_assignment):
    unassigned_variables = getUnassignedVariables(clause, partial_assignment)
    if len(unassigned_variables) == 1:
        return True, unassigned_variables[0]
    
    for var in unassigned_variables:
        if clause not in dict[var]:
            return False, var
        
    return False, None

def getUnassignedVariables(clause, partial_assignment):
    return [literal for literal in clause if partial_assignment[abs(literal)] == 0]

def getNextVariable(orderVars, partial_assignment):
    for var in orderVars:
        if partial_assignment[abs(var)] == 0:
            return var
    return None

def unit_propagate(dict, u_literals):
    return dict

clauses = load_dimacs('instances/customSAT.txt')


print(dpll_sat_solve(clauses))

# printTime(np.mean(timeit.repeat('dictify(clauses)', globals=globals(), number=100, repeat=100)))