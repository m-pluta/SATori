# Imports
import numpy as np
import copy
import re

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

def branching_sat_solve(clause_set, partial_assignment=[]):
    # Find all variables in the clause set (a variable and it's complement are the same)
    variables = np.unique(np.array([np.abs(literal) for clause in clause_set for literal in clause]))

    nextVariable = variables[0]
    for truth_assignment in [1,-1]:
        literal = truth_assignment * nextVariable
        result = backtrack(clause_set, variables, partial_assignment + [literal])
        if result:
            return result

    return False


def backtrack(clause_set, variables, partial_assignment):
    branched_clause_set = branch(clause_set, partial_assignment)
    if not (branched_clause_set[0] or branched_clause_set[1]):
        return
    if branched_clause_set[0]:
        return partial_assignment

    nextVariable = variables[len(partial_assignment)]
    for truth_assignment in [1,-1]:
        literal = truth_assignment * nextVariable
        result = backtrack(branched_clause_set[1], variables, partial_assignment + [literal])
        if result:
            return result

    return

# (True, None) if partial_assignment satisfies the clause_set
# (False, None) if there was an empty clause created in the clause_set
# (False, new_clause_set) if the branch was successful
def branch(clause_set, partial_assignment):
    new_clause_set = []
    branchLiteral = partial_assignment[-1]
    
    for clause in clause_set:
        if branchLiteral not in clause:
            clause_copy = copy.copy(clause)
            if (-1 * branchLiteral) in clause_copy:
                clause_copy.remove(-1 * branchLiteral)

                if (clause_copy == []):
                    return (False, None)
            
            new_clause_set.append(clause_copy)

    if new_clause_set == []:
        return (True, None)
    else:
        return (False, new_clause_set)



# clauses = load_dimacs('instances/unsat.txt')
# clauses = load_dimacs('instances/sat.txt')
# clauses = load_dimacs('instances/W_2,3_ n=8.txt')
# clauses = load_dimacs('instances/PHP-5-4.txt')
# clauses = load_dimacs('instances/LNP-6.txt')
clauses = load_dimacs('instances/8queens.txt')

import timeit
print(np.mean(np.array(timeit.repeat('branching_sat_solve(clauses)', globals=globals(), number=1, repeat=1))))