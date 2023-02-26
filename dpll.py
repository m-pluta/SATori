# Imports
import numpy as np
import timeit
from vsdc48 import load_dimacs
from collections import Counter
from itertools import chain

def getNextBranchVariable(clause_set):
    return Counter(chain.from_iterable(clause_set)).most_common(1)[0][0]

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

def dpll_solve(clause_set, partial_assignment=[]):
    # If first branch then we check initial clause_set
    new_clause_set = clause_set
    if not partial_assignment:
        if [] in clause_set:
            return False
    else:
        branch_data=branch(clause_set, partial_assignment[-1])
        
        if not (branch_data[0] or branch_data[1]):
            return False
        if branch_data[0]:
            return partial_assignment

        new_clause_set = branch_data[1]
    
    # Unit propagate with deletetion

    # Choose next branching variable
    nextVariable = getNextBranchVariable(new_clause_set)

    for truth_assignment in [1,-1]:
        literal = truth_assignment * nextVariable
        result = dpll_solve(new_clause_set, partial_assignment + [literal])
        if result:
            return result

    return False

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

def containsComplementPair(literals):
    for literal in literals:
        if -1 * literal in literals:
            return True
    return False

# clauses = load_dimacs('instances/unsat.txt')
# clauses = load_dimacs('instances/sat.txt')
# clauses = load_dimacs('instances/customSAT.txt')
# clauses = load_dimacs('instances/W_2,3_ n=8.txt')
# clauses = load_dimacs('instances/PHP-5-4.txt')
# clauses = load_dimacs('instances/LNP-6.txt')
clauses = load_dimacs('instances/8queens.txt')

# print("dpll", np.mean(np.array(timeit.repeat('dpll_solve(clauses)', globals=globals(), number=1, repeat=1))))

print(dpll_solve(clauses))