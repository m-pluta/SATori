# Imports
import timeit
import numpy as np
from collections import Counter
from itertools import product, chain
from printUtils import printTime
from vsdc48 import load_dimacs, containsComplementPair

# Returns the variables ordered in descending order of occurrence given a Counter object
def orderVars(vars):
    order = []
    # Order the variables in descending order of occurrence
    for var in vars.most_common():
        # If the literal's complement is already in the order then don't append it
        if -1 * var[0] not in order:
            order.append(var[0])
    return order

# Initialises a dictionary with 0s for each variable
def createPartialAssignment(vars):
    return dict.fromkeys([abs(var) for var in vars], 0)

# Return the watched literal dict, initial unit_literals, frequency order of variables
def dictify(clause_set):
    # Count all literals
    vars = Counter(chain.from_iterable(clause_set))

    # Order the variables
    order = orderVars(vars)
    
    # Initialise each literal in the dict with an empty list
    watched_literals = {}
    for var in order:
        watched_literals[var] = []
        watched_literals[-1 * var] = []
    # Potential alternative:
    # watched_literals = dict.fromkeys(vars.keys(), [])
    
    # List for unit literals found in the initial clause_set
    initial_unit_literals = set()

    # Go through each clause set and identify them as a unit clause or give them two watched literals
    for clause in clause_set:
        if len(clause) == 1:
            initial_unit_literals.add(clause[0])
            continue
        watched_literals[clause[0]].append(clause)
        watched_literals[clause[1]].append(clause)

    return watched_literals, initial_unit_literals, order

def dpll_sat_solve(clause_set, partial_assignment=[]):
    # Setup DPLL
    dict, u_literals, orderVars = dictify(clause_set)

    # Initialise partial assignment
    p_assignment = createPartialAssignment(orderVars)
    result = backtrack(dict, p_assignment, u_literals, orderVars)
    return [i for i in result.values()] if result else False

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
        # Unset all the units found before switching branch

    # Unset all u_literals before backtracking

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
    
    return units

def nextWatchLiteral(dict, clause, partial_assignment):
    unassigned_variables = [literal for literal in clause if partial_assignment[abs(literal)] == 0]
    if len(unassigned_variables) == 1:
        return True, unassigned_variables[0]
    
    for var in unassigned_variables:
        if clause not in dict[var]:
            return False, var
        
    return False, None

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