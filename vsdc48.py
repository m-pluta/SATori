# Imports
import numpy as np
import copy
import re
from itertools import product


# Open file and read lines
file = open('W_2,3_ n=8.txt', 'r')
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


def branching_sat_solve(clause_set, partial_assignment=[]):
    if check_truth_assignment(clause_set, partial_assignment):
        return partial_assignment

    # Find all variables in the clause set (a variable and it's complement are the same)
    variables = np.unique(np.array([np.abs(literal) for clause in clause_set for literal in clause]))
    num_variables = len(variables)

    lenPartial = len(partial_assignment)

    if lenPartial == num_variables:
        return []

    for i in [1, -1]:
        potential_solution = branching_sat_solve(clause_set, partial_assignment + [i * variables[lenPartial]])
        if potential_solution != []:
            return potential_solution

    return []


# Testing
print(branching_sat_solve(clauses))