# Imports
import numpy as np
import copy
import re
from itertools import product

def load_dimacs(filepath):
    # Open file and read lines
    file = open(filepath, 'r')
    lines = file.readlines()

    # Read all clauses
    clauses = []
    for line in lines:
        # Split clause into literals
        clause = line.split(' ')

        # If it's not a comment or the metadata
        if not re.match(r"^c|p$", clause[0]):
            # Remove line-separator '0'
            clause.pop()
            # Convert all elements in clause to ints and append clause
            clauses.append([int(i) for i in clause])

    return clauses



# Return satisfying truth assignment for given clause set or return False if it isn't satisfiable
def simple_sat_solve(clause_set):
    # Find all variables in the clause set (a variable and it's complement are the same)
    variables = np.unique(np.array([np.abs(literal) for clause in clause_set for literal in clause]))

    # Generate all possible truth assignment permutations of length=len(variables)
    # e.g. for length=3, [[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]
    truth_assignments = list(product([1, -1], repeat=len(variables)))
  
    # Loop through all possible truth assignments and return it if it satisfies the clause set
    for truth_assignment in truth_assignments:
        # Combine each variable with its corresponding truth value
        assignment = [var*truth for var,truth in zip(variables,truth_assignment)]

        # Check if it satisfies the clause set
        if check_truth_assignment(clause_set, assignment):
            return assignment
    
    # None of the truth assignments satisfy the clause set
    return False

def check_truth_assignment(clause_set, assignment):
    setA = set(assignment)
    # Loop through each clause
    for clause in clause_set:
        # If the clause and truth assignment do not have a literal in common then clause is not satisfied
        if (setA.isdisjoint(clause)):
            return False
    # Return true if all clauses were satisfied
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


def branching_sat_solver(clause_set, partial_assignment=[]):
    return

def branching_sat_solver_wrapped(clause_set, partial_assignment, remaining_variables):
    return

def branchOn(clause_set, literal):
    i = 0
    while (i < len(clause_set)):
        clause = clause_set[i]
        if literal in clause:
            del clause_set[i]
            continue
        elif (-1 * literal) in clause:
            clause.remove(-1 * literal)
            if (clause == []):
                return (False, [])
        i += 1

    return (True, clause_set)


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




# clauses = load_dimacs('instances/unsat.txt')
clauses = load_dimacs('instances/sat.txt')
# clauses = load_dimacs('instances/W_2,3_ n=8.txt')
# clauses = load_dimacs('instances/PHP-5-4.txt')
# clauses = load_dimacs('instances/LNP-6.txt')
# clauses = load_dimacs('instances/8queens.txt')


# print(unit_propagate([[1,2,3],[2,3],[1],[3],[5],[7,8,9],[-1,-3,-5,11],[-3,13], [-1,-5, 6],[2,4,5]]))
# print(unit_propagate(clauses))

# import timeit
# assignment = [1, 2, -3, -4, 5, 6, -7, -8, -9, -10, 11, 12, -13, -14, 15, 16]
# print('Slow')
# print(np.mean(np.array(timeit.repeat('check_truth_assignment(clauses, assignment)', globals=globals(), number=100, repeat=10000))))
# print('Fast')
# print(np.mean(np.array(timeit.repeat('check_truth_assignment_fast(clauses, assignment)', globals=globals(), number=100, repeat=10000))))

print(branchOn(clauses, -2))