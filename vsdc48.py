# Imports
import numpy as np
import copy
import re
from itertools import product

def openSAT(filepath):
    # Open file and read lines
    file = open(filepath, 'r')
    lines = file.readlines()

    # Read metadata from DIMACS file
    result = re.search(r"^p cnf (\d+) (\d+)$", lines[0])
    numVariable = result.groups()[0]
    numClause = result.groups()[1]

    # Read all clauses
    clauses = []
    for i in range(1, len(lines)): # Skip first line metadata at index 0
        # Split clause in literals
        clause = lines[i].split(' ')

        # If it's not a comment
        if clause[0] != 'c':
            # Remove line-separator '0' 
            clause.pop()
            # Convert all elements in clause to ints and append clause
            clauses.append([int(i) for i in clause])
    
    return (numVariable, numClause, clauses)


# Return satisfying truth assignment for given clause set or return False if it isnt satisfiable
def simple_sat_solve(clause_set):
    # Find all variables in the clause set (a variable and it's complement are the same)
    variables = np.unique(np.array([np.abs(literal) for clause in clause_set for literal in clause]))
    num_variables = len(variables)

    # Generate all possible truth assignment permutations of length=num_variables
    # e.g. for length=3, [[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]
    truth_assignments = list(product([1, -1], repeat=num_variables))
  
    # Loop through all possible truth assignment and return it if it satisfies the clause set
    for truth_assignment in truth_assignments:
        # Combine each variable with its corresponding truth value
        assignment = [var*truth for var,truth in zip(variables,truth_assignment)]

        # Check if it satisfies the clause set
        if check_truth_assignment(clause_set, assignment):
            return assignment
    
    # None of the truth_assignments satisfy the clause set
    return False


# Return true if the truth assignment satisfies the given clause set
def check_truth_assignment(clause_set, assignment):
    setA = set(assignment)
    # Loop through each clause
    for clause in clause_set:
        setB = set(clause)
        # If the clause and truth assignment do not have a literal in common then clause is not satisfied
        if (not setA.intersection(setB)):
            return False
    # Return true if all clauses were satisfied
    return True

def check_truth_assignment_fast(clause_set, assignment):
    setA = set(assignment)
    for clause in clause_set:
        if (setA.isdisjoint(clause)):
            return False
    return True

def branching_sat_solve(clause_set, partial_assignment=[]):
    # Find all variables in the clause set (a variable and it's complement are the same)
    variables = np.unique(np.array([np.abs(literal) for clause in clause_set for literal in clause]))

    result = branching_sat_solve_wrapped(clause_set, partial_assignment, variables)

    return result if result else False


def branching_sat_solve_wrapped(clause_set, partial_assignment, variables):
    if check_truth_assignment(clause_set, partial_assignment):
        return partial_assignment

    lenPartial = len(partial_assignment)

    if lenPartial == len(variables):
        return []

    for i in [1, -1]:
        potential_solution = branching_sat_solve_wrapped(clause_set, partial_assignment + [i * variables[lenPartial]], variables)
        if potential_solution != []:
            return potential_solution

    return []

def unit_propagate(clause_set, unit_literals=None):
    if unit_literals == None:
        unit_literals = [clause[0] for clause in clause_set if len(clause) == 1] # All unit literals in clause set

    if not unit_literals:
        return clause_set

    i = 0 # Index of clause
    j = 0 # Index of unit_literal
    new_unit_literals = []

    while i < len(clause_set):
        if len(clause_set[i]) != 1:
            if unit_literals[j] in clause_set[i]:
                # Remove the clause
                clause_set.pop(i)
                # i remains the same
                # j = 0
                j = 0
            elif (-1 * unit_literals[j]) in clause_set[i]:
                # Remove the variable from clause
                clause_set[i].remove(-1 * unit_literals[j])
                if (len(clause_set[i]) == 1):
                    new_unit_literals += clause_set[i]
                    i += 1
                    j = 0
                else:
                    # Check next unit literal
                    j += 1
                    if j >= len(unit_literals):
                    # If so increment i, set j = 0
                        i += 1
                        j = 0   
            else:
                # Increment j
                j += 1
                # Check if j > len(unit_literals)
                if j >= len(unit_literals):
                # If so increment i, set j = 0
                    i += 1
                    j = 0     
        else:
            i += 1

    if len(new_unit_literals) > 0:
        return unit_propagate(clause_set, new_unit_literals)
    else:
        return clause_set


# Testing

# clauses = openSAT('instances/unsat.txt')
# clauses = openSAT('instances/sat.txt')
clauses = openSAT('instances/W_2,3_ n=8.txt')
# clauses = openSAT('instances/PHP-5-4.txt')
# clauses = openSAT('instances/LNP-6.txt')
# clauses = openSAT('instances/8queens.txt')

# print(unit_propagate([[1,2,3],[2,3],[1],[3],[5],[7,8,9],[-1,-3,-5,11],[-3,13], [-1,-5, 6],[2,4,5]]))
print(unit_propagate(clauses[2]))

print(branching_sat_solve(clauses[2]))