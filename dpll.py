# Imports
import numpy as np
import timeit
from vsdc48 import load_dimacs

def dpll_sat_solve(clause_set, partial_assignment=[]):
    return

def dpll_backtrack():
    return

def branch():
    return

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

print(np.mean(np.array(timeit.repeat('branching_sat_solve(clauses)', globals=globals(), number=1, repeat=1))))