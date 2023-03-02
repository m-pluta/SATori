# Imports
import timeit
import numpy as np
from collections import Counter
from itertools import product, chain
from printUtils import printTime

def load_dimacs(filepath):
    # Open file and read lines
    file = open(filepath, 'r')
    lines = file.readlines()
    
    clauses = []
    for line in lines:
        if line[0] not in ('c', 'p'):
            clauses.append([int(literal) for literal in line.split() if literal != '0'])
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
    variables = get_variables(clause_set)

    nextVariable = variables[0]
    for truth_assignment in [1,-1]:
        literal = truth_assignment * nextVariable
        result = backtrack(clause_set, variables, partial_assignment + [literal])
        if result:
            return result

    return False

def get_variables(clause_set):
    return np.unique(np.array([np.abs(literal) for clause in clause_set for literal in clause]))

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
            clause_copy = clause[:]
            if (-1 * branchLiteral) in clause_copy:
                clause_copy.remove(-1 * branchLiteral)

                if (clause_copy == []):
                    return (False, None)
            
            new_clause_set.append(clause_copy)

    if new_clause_set == []:
        return (True, None)
    else:
        return (False, new_clause_set)



def unit_propagate(clause_set, unit_literals=None):
    if unit_literals == None:
        unit_literals = [clause[0] for clause in clause_set if len(clause) == 1] # All unit literals in clause set

    # Might be useless
    if not unit_literals:
        return clause_set

    new_clause_set = []
    new_unit_literals = []
    for clause in clause_set:
        clause_copy = clause[:]
        for unit_literal in unit_literals:
            if unit_literal in clause_copy:
                clause_copy = []
                break
            elif (-1 * unit_literal) in clause_copy:
                clause_copy.remove(-1 * unit_literal)

        if len(clause_copy) == 1:
            new_unit_literals.append(clause_copy[0])
            new_clause_set.append(clause_copy)
        elif clause_copy:
            new_clause_set.append(clause_copy)
    
    if new_unit_literals:
        return unit_propagate(new_clause_set, new_unit_literals)
    else:
        return new_clause_set



# Returns the next variable to branch on, which is the most common one
def getNextBranchVariable(clause_set):
    # Return the most common variable in the clause_set
    return Counter(chain.from_iterable(clause_set)).most_common(1)[0][0]

# Returns None if [] is generated during propagation
# Returns new_clause_set if propagation was successful (could be an empty clause set)
def UP(clause_set, unit_literals):
    # Return original clause_set if no unit literals to propagate over
    if not unit_literals:
        return clause_set

    # Go through each clause and create a copy of it
    new_clause_set = []
    for clause in clause_set:
        clause_copy = clause[:]
        # Check if the clause contains any unit literals
        for unit_literal in unit_literals:
            # If the unit literal is in the clause then remove the whole clause and break
            if unit_literal in clause_copy:
                clause_copy = None
                break
            # If the complemented literal is in the clause then remove the variable
            elif (-1 * unit_literal) in clause_copy:
                clause_copy.remove(-1 * unit_literal)

                if not clause_copy:
                    return None

        # If the clause
        if clause_copy is not None:
            new_clause_set.append(clause_copy)
    
    return new_clause_set

# Main backtracking function
def dpll_sat_solve(clause_set, partial_assignment=[]):
    new_clause_set = clause_set

# Branching on current variable

    # If first dpll_solve recursion
    if not partial_assignment:
        # If clause set is empty then sat
        if not clause_set:
            return []
        # Check if the initial clause_set is unsatisfiable
        if [] in clause_set:
            return False
    else:
        # Branch on the last variable added to the partial assignment
        branch_clause_set=branch(clause_set, partial_assignment[-1])
        if branch_clause_set == None:
            return False
        if not branch_clause_set:
            return partial_assignment

        new_clause_set = branch_clause_set
    
# Unit propagation

    # Unit propagate with deletion
    unit_literals = set([clause[0] for clause in new_clause_set if len(clause) == 1])
    while (unit_literals):
        if containsComplementPair(unit_literals):
            return False
        new_clause_set = UP(new_clause_set, unit_literals)
        if new_clause_set is None:
            return False
        elif not new_clause_set:
            return partial_assignment
        unit_literals = set([clause[0] for clause in new_clause_set if len(clause) == 1])

    if not new_clause_set:
        return partial_assignment

    # Choose next branching variable
    nextVariable = getNextBranchVariable(new_clause_set)

# Branching to next variables

    # Branch on each truth assignment
    for truth_assignment in [1,-1]:
        literal = truth_assignment * nextVariable
        # Store branch result
        result = dpll_sat_solve(new_clause_set, partial_assignment + [literal])
        # If a result was returned then it must be a solution
        if result:
            return result

    return False

# Returns None if [] is generated during branching
# Returns new_clause_set if branching was successful (could be an empty clause set)
def branch(clause_set, branchOn):
    new_clause_set = []
    
    # Go through each clause
    for clause in clause_set:
        # If the exact literal is in the clause then there is no point adding it to the new clause because it gets eliminated
        if branchOn not in clause:
            # Copy the clause
            clause_copy = clause[:]
            if (-1 * branchOn) in clause_copy:
                clause_copy.remove(-1 * branchOn)

                # If the clause is empty after removal then clause_set is unsat and return
                if not clause_copy:
                    return None
            
            new_clause_set.append(clause_copy)

    return new_clause_set

# Returns True if the unit literals contain a complement pair i.e {-1, 1} or {7, -7}
def containsComplementPair(literals):
    # Go through each literal
    for literal in literals:
        # If its complement is in the literal list then there is a complement pair
        if -1 * literal in literals:
            return True
        
    # No complement pairs found
    return False


# clauses = load_dimacs('instances/unsat.txt')
# clauses = load_dimacs('instances/sat.txt')
# clauses = load_dimacs('instances/customSAT.txt')
# clauses = load_dimacs('instances/W_2,3_ n=8.txt')
# clauses = load_dimacs('instances/PHP-5-4.txt')
# clauses = load_dimacs('instances/LNP-6.txt')
clauses = load_dimacs('instances/8queens.txt')

printTime(np.mean(np.array(timeit.repeat('dpll_sat_solve(clauses)', globals=globals(), number=1, repeat=1))))
print(dpll_sat_solve(clauses))