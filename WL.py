# Imports
import timeit
import numpy as np
from collections import Counter
from itertools import product, chain
from printUtils import printTime
from vsdc48 import load_dimacs, containsComplementPair, check_truth_assignment

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

    for branchLiteral in [nextVariable, -1 * nextVariable]:
        units = setVar(dict, branchLiteral, partial_assignment)
        if units == False:
            continue
        result = backtrack(dict, partial_assignment, units, orderVars)
        if result:
            return result
        partial_assignment[abs(branchLiteral)] = 0
        # Unset all the units found before switching branch

    # Unset all u_literals before backtracking

    return False

def setVar(dict, var, partial_assignment):
    units = set()
    partial_assignment[abs(var)] = var
    
    newList = []
    for clause in dict[-1 * var]:
        if isClauseSat(clause, partial_assignment):
            newList.append(clause)
            continue
        unassigned_variables = [literal for literal in clause if partial_assignment[abs(literal)] == 0]
        if not unassigned_variables:
            return False
        elif len(unassigned_variables) == 1:
            units.add(unassigned_variables[0])
            newList.append(clause)
        else:
            newLiteral = nextWatchLiteral(dict, clause, unassigned_variables)
            dict[newLiteral].append(clause)
    
    dict[-1 * var] = newList
    
    return units

def nextWatchLiteral(dict, clause, unassigned_variables):
    for var in unassigned_variables:
        if clause not in dict[var]:
            return var
    return None

def isClauseSat(clause, partial_assignment):
    for literal in clause:
        if partial_assignment[abs(literal)] == literal:
            return True
    return False

def getNextVariable(orderVars, partial_assignment):
    for var in orderVars:
        if partial_assignment[abs(var)] == 0:
            return var
    return None

def unit_propagate(dict, u_literals):
    return dict

clauses = load_dimacs('instances/sat.txt')

sol = dpll_sat_solve(clauses)
print(sol)
if sol:
    print(check_truth_assignment(clauses, sol))

# printTime(np.mean(timeit.repeat('dictify(clauses)', globals=globals(), number=100, repeat=100)))