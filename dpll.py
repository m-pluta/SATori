# Imports
import numpy as np
import timeit
from vsdc48 import load_dimacs

def dpll_sat_solve(clause_set, partial_assignment=[]):
    variables = get_variables(clause_set)

    nextVariable = variables[0]
    for truth_assignment in [1,-1]:
        literal = truth_assignment * nextVariable
        result = dpll_backtrack(clause_set, variables, partial_assignment + [literal])
        if result:
            return result

    return False

def get_variables(clause_set):
    return np.unique(np.array([np.abs(literal) for clause in clause_set for literal in clause]))

def dpll_backtrack(clause_set, variables, partial_assignment):
    branch_data = branch(clause_set, partial_assignment[-1])
    if not (branch_data[0] or branch_data[1]):
        return
    if branch_data[0]:
        return partial_assignment

    branched_clause_set = branch_data[1]

    nextVariable = variables[len(partial_assignment)]
    for truth_assignment in [1,-1]:
        literal = truth_assignment * nextVariable
        result = dpll_backtrack(branched_clause_set, variables, partial_assignment + [literal])
        if result:
            return result

    return

def branch(clause_set, branchOn):
    new_clause_set = []
    
    for clause in clause_set:
        if branchOn not in clause:
            clause_copy = clause[:]
            if (-1 * branchOn) in clause_copy:
                clause_copy.remove(-1 * branchOn)

                if (clause_copy == []):
                    return (False, None)
            
            new_clause_set.append(clause_copy)

    if new_clause_set == []:
        return (True, None)
    else:
        return (False, new_clause_set)

def UP(clause_set, unit_literals):
    # unit_literals = [clause[0] for clause in clause_set if len(clause) == 1]
    # Return if no unit literals to propagate over
    if not unit_literals:
        return clause_set

    new_clause_set = []
    for clause in clause_set:
        clause_copy = clause[:]
        for unit_literal in unit_literals:
            if unit_literal in clause_copy:
                clause_copy = []
                break
            elif (-1 * unit_literal) in clause_copy:
                clause_copy.remove(-1 * unit_literal)

        if clause_copy:
            new_clause_set.append(clause_copy)
    
    return new_clause_set


# clauses = load_dimacs('instances/unsat.txt')
# clauses = load_dimacs('instances/sat.txt')
# clauses = load_dimacs('instances/customSAT.txt')
# clauses = load_dimacs('instances/W_2,3_ n=8.txt')
# clauses = load_dimacs('instances/PHP-5-4.txt')
# clauses = load_dimacs('instances/LNP-6.txt')
clauses = load_dimacs('instances/8queens.txt')

print(np.mean(np.array(timeit.repeat('dpll_sat_solve(clauses)', globals=globals(), number=1, repeat=1))))