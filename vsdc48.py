# Theory behind watched literals for Q8 & Q9 from:
# - Original stackexchange post that started the optimisation addiction:
#     - https://cs.stackexchange.com/questions/150557/what-are-efficient-approaches-to-implement-unit-propagation-in-dpll-based-sat-so
# - Research paper which formally explained the watched literal method:
#     - https://www.semanticscholar.org/paper/Optimal-Implementation-of-Watched-Literals-and-More-Gent/ad7fbc3ede6e89491e3b753074efed8705480a33
# - Most useful resource for understanding the watched literal method:
#     - http://haz-tech.blogspot.com/2010/08/whos-watching-watch-literals.html?m=1
# - Worksheet used to dry-run the algorithm on clause sets:
#     - https://www.inf.ed.ac.uk/teaching/courses/inf1/cl/tutorials/2015/tutorial5.pdf
# 
# Potential improvements to current method: 
# - Conflict Driven Clause Learning (CDCL)
# - Watched literals for each clause forced to be in the first two positions of the clause
#   avoiding the use of pointers:
#   https://www.cs.kent.ac.uk/pubs/2010/2970/content.pdf 

# Paper that suggested the use of a heuristic for deciding the branching variable:
# - https://www.sciencedirect.com/science/article/pii/S0004370299000971
#   essentially it explained how the problem of choosing the optimal
#   branching variable was harder than the satisfiability proble itself

# LEFV (Last Encountered Free Variable) heuristic:
# - https://baldur.iti.kit.edu/sat/files/2019/l05.pdf


# Imports
import numpy as np
from collections import Counter, deque
from itertools import product, chain

# Load a file in DIMACS format and return it as a list of lists
def load_dimacs(filepath):
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
    variables = get_variables(clause_set)

    # Generate all possible truth assignment permutations of length=len(variables)
    # e.g. for length=3, [[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]
    all_truth_assignments = list(product([1, -1], repeat=len(variables)))
  
    # Loop through all possible truth assignments and return it if it satisfies the clause set
    for truth_assignment in all_truth_assignments:
        # Combine each variable with its corresponding truth value
        assignment = [var*truth for var,truth in zip(variables,truth_assignment)]

        if check_truth_assignment(clause_set, assignment):
            return assignment
    
    return None

# Return true if a given truth assignment satisfies a clause_set
def check_truth_assignment(clause_set, assignment):
    setA = set(assignment)

    for clause in clause_set:
        # If the clause and truth assignment do not have 
        # a literal in common then clause is not satisfied
        if (setA.isdisjoint(clause)):
            return False
        
    return True

def get_variables(clause_set):
    return np.unique(np.array([np.abs(literal) for clause in clause_set for literal in clause]))



def branching_sat_solve(clause_set, partial_assignment=[]):
    if not clause_set:
        return []
    if [] in clause_set:
        return False
    # Find all variables in the clause set (a variable and it's complement are the same)
    variables = get_variables(clause_set)

    nextVariable = variables[0]
    for literal in [nextVariable,-nextVariable]:
        result = backtrack(clause_set, variables, partial_assignment + [literal])
        if result:
            return result

    return False

def backtrack(clause_set, variables, partial_assignment):
    branched_clause_set = branch(clause_set, partial_assignment)
    if branched_clause_set is None:
        return
    if not branched_clause_set:
        return partial_assignment

    nextVariable = variables[len(partial_assignment)]
    for literal in [nextVariable,-nextVariable]:
        result = backtrack(branched_clause_set, variables, partial_assignment + [literal])
        if result:
            return result

    return

# Returns None if there was an empty clause created in the clause_set
# new_clause_set if the branch was successful, new_clause_set may be empty
def branch(clause_set, partial_assignment):
    new_clause_set = []
    branchLiteral = partial_assignment[-1]
    
    for clause in clause_set:
        if branchLiteral not in clause:
            clause_copy = clause[:]
            if (-branchLiteral) in clause_copy:
                clause_copy.remove(-branchLiteral)

                if (clause_copy == []):
                    return None
            
            new_clause_set.append(clause_copy)

    return new_clause_set



def unit_propagate(clause_set):
    # All unit literals in clause set
    unit_literals = [clause[0] for clause in clause_set if len(clause) == 1]

    if not unit_literals:
        return clause_set
    
    # Create a queue for the unit_literals
    unit_queue = deque(unit_literals)


    return_clause_set = clause_set
    while unit_queue:
        nextUnit = unit_queue.popleft()
        new_clause_set = []
        for clause in return_clause_set:
            if nextUnit not in clause:
                clause_copy = [literal for literal in clause[:] if literal != -nextUnit]
                if len(clause_copy) == 1:
                    unit_queue.append(clause_copy[0])
                else:
                    new_clause_set.append(clause_copy)

        return_clause_set = new_clause_set

    return return_clause_set



# Returns the variables ordered in descending order of occurrence given a Counter object
def orderVars(vars):
    order = []
    for var in vars:
        if -var[0] not in order:
            order.append(var[0])
    return order

# Initialises a dictionary with 0s for each variable
def createPartialAssignment(vars):
    return dict.fromkeys([abs(var) for var in vars], 0)

# Initialise the dictionary which stores the clauses
def initialiseWatchedLiterals(order):
    watched_literals = {}
    for var in order:
        watched_literals[var] = []
        watched_literals[-var] = []
    return watched_literals

# Return the watched literal dict, initial unit_literals, frequency order of variables
def dictify(clause_set):
    # Count all literals
    most_common_vars = Counter(chain.from_iterable(clause_set)).most_common()

    # Order the variables and create watched literal dict
    order = orderVars(most_common_vars)
    watched_literals = initialiseWatchedLiterals(order)

    # Pure literals (if any) can be handled in the same way as unit literals
    initial_unit_literals = getPureLiterals(most_common_vars)

    # Go through each clause set and identify them as a unit clause
    # or give them two watched-literals
    for clause in clause_set:
        if len(clause) == 1:
            initial_unit_literals.add(clause[0])
            continue
        if clause not in watched_literals[clause[0]]:
            watched_literals[clause[0]].append(clause)
            watched_literals[clause[1]].append(clause)

    return watched_literals, initial_unit_literals, order

# Pure literal elimination from 
# https://www.cs.cornell.edu/courses/cs4860/2009sp/lec-04.pdf
def getPureLiterals(most_common_vars):
    PLs = set()
    # Walrus operator :P so funky
    for var in (vars := {var[0] for var in most_common_vars}):
        if -var not in vars:
            PLs.add(var)
    return PLs

# Main callable function
def dpll_sat_solve(clause_set, partial_assignment=None):
    # Check possible initial conditions
    if not clause_set:
        return []
    if [] in clause_set:
        return False
    
    dict, initial_u_literals, orderVars = dictify(clause_set)
    partial_assignment = createPartialAssignment(orderVars)

    result = backtrackWL(dict, partial_assignment, initial_u_literals, orderVars)
    
    # If there is a result, convert it from dictionary to list 
    return [i for i in result.values()] if result else False

# Iterative unit propagation
def unit_propagateWL(dict, units, partial_assignment):
    units_propagated = [] # Unit literals that have so far been set to true
    u_literals = deque(units)
    mainLEFV = None # Last encountered free variable in the whole unit prop method
    while u_literals:
        nextUnit = u_literals.popleft()

        # Set the unit literal to true and add new unit literals to the queue
        units_propagated.append(nextUnit)
        lefv, newUnits = setVar(dict, nextUnit, partial_assignment)

        if newUnits == False:
            unassignVars(partial_assignment, units_propagated)
            return None, False
        u_literals.extend(newUnits)

        if lefv:
            mainLEFV = lefv

    return mainLEFV, units_propagated

# Main backtracking function
def backtrackWL(dict, partial_assignment, u_literals, orderVars, lefv=None):
    if u_literals:
        lefv, u_literals = unit_propagateWL(dict, u_literals, partial_assignment)

         # If the unit prop returned False then there was a conflict (empty clause generated)
        if not u_literals:
            return

    # If all variables have been assigned a value
    if 0 not in partial_assignment.values():
        return partial_assignment

    # Choose next branching variable
    nextVariable = lefv if lefv else getNextVariable(orderVars, partial_assignment)

    for branchLiteral in [nextVariable, -nextVariable]:
        # Set the branch variable
        lefv, units = setVar(dict, branchLiteral, partial_assignment)

        # If the branching variable led to an empty clause then try the other variable
        if units == False:
            continue

        # Branch on the variable that was set
        if result := backtrackWL(dict, partial_assignment, units, orderVars, lefv):
            return result
        
        # Unassign the branch variable if it didn't lead to a solution
        partial_assignment[abs(branchLiteral)] = 0

    # Unset all the unit literals before backtracking
    unassignVars(partial_assignment, u_literals)
    return False

# Add variable to the partial_assignment, Resolve all possible problematic clauses
def setVar(dict, var, partial_assignment):
    lefv = None
    units = set()
    partial_assignment[abs(var)] = var
    
    removed = 0 # How many clauses have been assigned a new watch literal, used as an offset
    newList = dict[-var].copy() # Clauses that should remain in the watch literal

    for count, clause in enumerate(dict[-var]):
        if isClauseSat(clause, partial_assignment):
            continue
        
        unassigned_variables = [literal for literal in clause if partial_assignment[abs(literal)] == 0]
        
        # The clause is unsat and has no free variables = empty clause
        if not unassigned_variables:
            dict[-var] = newList
            return None, False   
        # The clause is unsat but has one free variable = unit literal
        elif len(unassigned_variables) == 1:
            units.add(unassigned_variables[0])
        # The clause is unsat and has >1 free variable so it is possible to switch the watch literal
        else:
            lefv = nextWatchLiteral(dict, clause, unassigned_variables)
            dict[lefv].append(clause)
            newList.pop(count - removed)
            removed += 1
    
    dict[-var] = newList
    
    return lefv, units

# Set all variables in a given list to 0 in the partial assignment (unassigned)
def unassignVars(partial_assignment, vars):
    for var in vars:
        partial_assignment[abs(var)] = 0

# Chooses the next freely available watch literal for the clause
def nextWatchLiteral(dict, clause, unassigned_variables):
    for var in unassigned_variables:
        # If the literal is not already a watched literal
        if clause not in dict[var]:
            return var
    return None

# Checks if a given clause is True
def isClauseSat(clause, partial_assignment):
    for literal in clause:
        if partial_assignment[abs(literal)] == literal:
            return True
    return False

# Returns the most common free variable
def getNextVariable(orderVars, partial_assignment):
    for var in orderVars:
        if partial_assignment[abs(var)] == 0:
            return var
    return None



# import timeit

fp = 'sat_instances/'

# clauses = load_dimacs(fp +'unsat.txt')
clauses = load_dimacs(fp +'sat.txt')
# clauses = load_dimacs(fp +'customSAT.txt')
# clauses = load_dimacs(fp +'W_2,3_ n=8.txt')
# clauses = load_dimacs(fp +'PHP-5-4.txt')
# clauses = load_dimacs(fp +'LNP-6.txt')
# clauses = load_dimacs(fp +'gt.txt')
# clauses = load_dimacs(fp +'8queens.txt')
# clauses = load_dimacs(fp + 'n=100.txt')


# print(np.mean(np.array(timeit.repeat('dpll_sat_solve(clauses)', globals=globals(), number=10, repeat=100))))

sol = dpll_sat_solve(clauses)
print(sol)
if sol:
    print(check_truth_assignment(clauses, sol))
