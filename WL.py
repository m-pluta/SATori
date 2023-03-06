# Imports
import timeit
import numpy as np
from collections import Counter
from itertools import chain
from printUtils import printTime
from vsdc48 import load_dimacs, containsComplementPair, check_truth_assignment

# Returns the variables ordered in descending order of occurrence given a Counter object
def orderVars(vars):
    order = []
    # Order the variables in descending order of occurrence
    for var in vars.most_common():
        # If the literal's complement is already in the order then don't append it
        if -var[0] not in order:
            order.append(var[0])
    return order

# Initialises a dictionary with 0s for each variable
def createPartialAssignment(vars):
    return dict.fromkeys([abs(var) for var in vars], 0)

def initialiseWatchedLiterals(order):
    watched_literals = {}
    for var in order:
        watched_literals[var] = []
        watched_literals[-var] = []
    return watched_literals
    # Potential alternative:
    # watched_literals = dict.fromkeys(vars.keys(), [])

# Return the watched literal dict, initial unit_literals, frequency order of variables
def dictify(clause_set):
    # Count all literals
    vars = Counter(chain.from_iterable(clause_set))

    # Order the variables
    order = orderVars(vars)
    
    # Initialise each literal in the dict with an empty list
    watched_literals = initialiseWatchedLiterals(order)
    
    # List for unit literals found in the initial clause_set
    initial_unit_literals = set()
    # Go through each clause set and identify them as a unit clause or give them two watched-literals
    for clause in clause_set:
        if len(clause) == 1:
            initial_unit_literals.add(clause[0])
            continue
        watched_literals[clause[0]].append(clause)
        watched_literals[clause[1]].append(clause)

    return watched_literals, initial_unit_literals, order

def dpll_sat_solve(clause_set, partial_assignment=None):
    # Setup DPLL
    dict, u_literals, orderVars = dictify(clause_set)
    # Initialise partial assignment
    partial_assignment = createPartialAssignment(orderVars)

    # Attempt to find solution
    result = backtrack(dict, partial_assignment, u_literals, orderVars)
    
    # If there is a result, convert it from dictionary to list 
    return [i for i in result.values()] if result else False


def unit_propagate(dict, units, partial_assignment):
    # Init
    units_propagated = [] # Unit literals that have so far been set to true
    u_literals = list(units)

    while u_literals:
        # If there is complement pair in the literal list then there is a conflict
        # e.g. if 1 and -1 are in the list then both of them cannot be true
        if containsComplementPair(u_literals):
            # Unassign all the variables that have been so far set to true during unit prop and return
            unassignVars(partial_assignment, units_propagated)
            return False
        
        # Dequeue next unit literal
        var = u_literals.pop(0)

        # Set the unit literal to true and add new unit literals to the queue
        newUnits = setVar(dict, var, partial_assignment)
        u_literals.extend(list(newUnits))

        units_propagated.append(var)

    return units_propagated

# Main function
def backtrack(dict, partial_assignment, u_literals, orderVars):
    # Unit propagate over all the unit literals
    if u_literals:
        # Unit Propagate functions returns all units that were recursively propagated
        # i.e. Provided units could have led to more unit literals
        u_literals = unit_propagate(dict, u_literals, partial_assignment)
        if not u_literals:
            # If the unit prop returned False then there was a ComplementPair conflict
            return

    # If the partial assignment is full then return it, it must be correct
    if 0 not in partial_assignment.values():
        return partial_assignment
    

    # if Φ contains an empty clause then
    #     return false


    nextVariable = getNextVariable(orderVars, partial_assignment)

    # Branch to the positive and negative literals
    for branchLiteral in [nextVariable, -nextVariable]:
        # Set the variable
        units = setVar(dict, branchLiteral, partial_assignment)

        # If the branching variable led to an empty clause
        # then try the other variable, or backtrack by exiting for each loop
        if units == False:
            continue

        # Branch on the variable that was set
        result = backtrack(dict, partial_assignment, units, orderVars)
        if result:
            return result
        
        # Unassign the set variable if it didnt lead to a solution
        partial_assignment[abs(branchLiteral)] = 0

    # Unset all the unit literals before backtracking
    unassignVars(partial_assignment, u_literals)
    return False

# Sets the variable, updates the dict and partial_assignment
def setVar(dict, var, partial_assignment):
    units = set() # Units found while setting the variable
    partial_assignment[abs(var)] = var # Set the variable in the partial_assignment
    
    newList = [] # Clauses that should remain in the watch literal
    for clause in dict[-var]:
        # If the clause is already true then it keep being watched by that literal, and skip it
        if isClauseSat(clause, partial_assignment):
            newList.append(clause)
            continue
        
        unassigned_variables = [literal for literal in clause if partial_assignment[abs(literal)] == 0]
        
        # The clause is unsat and has no free variables so it is an empty clause
        if not unassigned_variables:
            return False
        # The clause is unsat but has one free variable so it is a unit literal
        elif len(unassigned_variables) == 1:
            units.add(unassigned_variables[0])
            newList.append(clause)
        # The clause is unsat and has >1 free variable so it is possible to switch the watch literal
        else:
            newLiteral = nextWatchLiteral(dict, clause, unassigned_variables)
            dict[newLiteral].append(clause)
    
    dict[-var] = newList # Update the dict
    return units # Return all the unit literals that have been found

# Given a list of variables to unassign, they are set to 0 in the partial assignment
def unassignVars(partial_assignment, vars):
    for var in vars:
        partial_assignment[abs(var)] = 0

# Determines which literal in a clause should be watched
def nextWatchLiteral(dict, clause, unassigned_variables):
    for var in unassigned_variables:
        # If the literal is not a watched literal already
        if clause not in dict[var]:
            return var
    return None

# Checks if a given clause is True
def isClauseSat(clause, partial_assignment):
    for literal in clause:
        # Check if any variable in the partial assignment satisfies the clause
        if partial_assignment[abs(literal)] == literal:
            return True
    return False

# Returns the most common free variable
def getNextVariable(orderVars, partial_assignment):
    for var in orderVars:
        # Returns variable if it is free
        if partial_assignment[abs(var)] == 0:
            return var
    return None

clauses = load_dimacs('instances/8queens.txt')

sol = dpll_sat_solve(clauses)
print(sol)
if sol:
    print(check_truth_assignment(clauses, sol))

printTime(np.mean(timeit.repeat('dpll_sat_solve(clauses)', globals=globals(), number=10, repeat=100)))