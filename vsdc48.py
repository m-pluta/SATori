# Imports
import timeit
import numpy as np
from collections import Counter, deque
from itertools import product, chain

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

def get_variables(clause_set):
    return np.unique(np.array([np.abs(literal) for clause in clause_set for literal in clause]))

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

# None if there was an empty clause created in the clause_set
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

    # If there is no unit-literals
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



# # Returns the next variable to branch on, which is the most common one
# def getNextBranchVariable(clause_set):
#     # Return the most common variable in the clause_set
#     return Counter(chain.from_iterable(clause_set)).most_common(1)[0][0]

# # Returns None if [] is generated during propagation
# # Returns new_clause_set if propagation was successful (could be an empty clause set)
# def UP(clause_set, unit_literals):
#     # Return original clause_set if no unit literals to propagate over
#     if not unit_literals:
#         return clause_set

#     # Go through each clause and create a copy of it
#     new_clause_set = []
#     for clause in clause_set:
#         clause_copy = clause[:]
#         # Check if the clause contains any unit literals
#         for unit_literal in unit_literals:
#             # If the unit literal is in the clause then remove the whole clause and break
#             if unit_literal in clause_copy:
#                 clause_copy = None
#                 break
#             # If the complemented literal is in the clause then remove the variable
#             elif (-unit_literal) in clause_copy:
#                 clause_copy.remove(-unit_literal)

#                 if not clause_copy:
#                     return None

#         if clause_copy is not None:
#             new_clause_set.append(clause_copy)
    
#     return new_clause_set

# # Main backtracking function
# def dpll_sat_solve(clause_set, partial_assignment=[]):
#     new_clause_set = clause_set

# # Branching on current variable

#     # If first dpll_solve recursion
#     if not partial_assignment:
#         # If clause set is empty then sat
#         if not clause_set:
#             return []
#         # Check if the initial clause_set is unsatisfiable
#         if [] in clause_set:
#             return False
#     else:
#         # Branch on the last variable added to the partial assignment
#         branch_clause_set=branchDPLL(clause_set, partial_assignment[-1])
#         if branch_clause_set == None:
#             return False
#         if not branch_clause_set:
#             return partial_assignment

#         new_clause_set = branch_clause_set
    
# # Unit propagation

#     # Unit propagate with deletion
#     unit_literals = set([clause[0] for clause in new_clause_set if len(clause) == 1])
#     while (unit_literals):
#         if containsComplementPair(unit_literals):
#             return False
#         new_clause_set = UP(new_clause_set, unit_literals)
#         if new_clause_set is None:
#             return False
#         elif not new_clause_set:
#             return partial_assignment
#         unit_literals = set([clause[0] for clause in new_clause_set if len(clause) == 1])

#     if not new_clause_set:
#         return partial_assignment

#     # Choose next branching variable
#     nextVariable = getNextBranchVariable(new_clause_set)

# # Branching to next variables

#     # Branch on each truth assignment
#     for literal in [nextVariable,-nextVariable]:
#         # Store branch result
#         result = dpll_sat_solve(new_clause_set, partial_assignment + [literal])
#         # If a result was returned then it must be a solution
#         if result:
#             return result

#     return False

# # Returns None if [] is generated during branching
# # Returns new_clause_set if branching was successful (could be an empty clause set)
# def branchDPLL(clause_set, branchOn):
#     new_clause_set = []
    
#     # Go through each clause
#     for clause in clause_set:
#         # If the exact literal is in the clause then there is no point adding it to the new clause because it gets eliminated
#         if branchOn not in clause:
#             # Copy the clause
#             clause_copy = clause[:]
#             if (-branchOn) in clause_copy:
#                 clause_copy.remove(-branchOn)

#                 # If the clause is empty after removal then clause_set is unsat and return
#                 if not clause_copy:
#                     return None
            
#             new_clause_set.append(clause_copy)

#     return new_clause_set

# Returns True if the unit literals contain a complement pair i.e {-1, 1} or {7, -7}
def containsComplementPair(literals):
    seen = set()
    # Go through each literal
    for literal in literals:
        seen.add(literal)
        # If its complement has already been seen then there is a complement pair
        if -literal in seen:
            return True
        
    # No complement pairs found
    return False








# Returns the variables ordered in descending order of occurrence given a Counter object
def orderVars(vars):
    order = []
    # Order the variables in descending order of occurrence
    for var in vars.most_common():
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
    vars = Counter(chain.from_iterable(clause_set))

    # Order the variables
    order = orderVars(vars)
    
    watched_literals = initialiseWatchedLiterals(order)
    
    initial_unit_literals = set()

    # Go through each clause set and identify them as a unit clause or give them two watched-literals
    for clause in clause_set:
        if len(clause) == 1:
            initial_unit_literals.add(clause[0])
            continue
        if clause not in watched_literals[clause[0]]:
            watched_literals[clause[0]].append(clause)
            watched_literals[clause[1]].append(clause)

    return watched_literals, initial_unit_literals, order

# Main callable function
def dpll_sat_solve(clause_set, partial_assignment=None):
    if not clause_set:
        return []
    if [] in clause_set:
        return False
    
    dict, u_literals, orderVars = dictify(clause_set)
    partial_assignment = createPartialAssignment(orderVars)

    result = backtrackWL(dict, partial_assignment, u_literals, orderVars)
    
    # If there is a result, convert it from dictionary to list 
    return [i for i in result.values()] if result else False

# Iterative unit propagation
def unit_propagateWL(dict, units, partial_assignment):
    units_propagated = [] # Unit literals that have so far been set to true
    u_literals = list(units)
    lefv = None

    while u_literals:
        # If there is complement pair in the literal list then there is a conflict
        # e.g. if 1 and -1 are in the list then both of them cannot be true
        if containsComplementPair(u_literals):
            # Unassign all the variables that have been so far set to true during unit prop and return
            unassignVars(partial_assignment, units_propagated)
            return lefv, False
        
        nextUnit = u_literals.pop(0)

        lefvArr = [0]    
        # Set the unit literal to true and add new unit literals to the queue
        newUnits = setVarLEFV(dict, nextUnit, partial_assignment, lefvArr)
        u_literals.extend(list(newUnits))
        units_propagated.append(nextUnit)

        if (var:= lefvArr[0]) != 0:
            lefv = var

    return lefv, units_propagated

# Main function
def backtrackWL(dict, partial_assignment, u_literals, orderVars):
    lefv = None
    if u_literals:
        # Unit Propagate functions returns all units that were iteratively propagated over
        # Provided units could have led to more unit literals
        lefv, u_literals = unit_propagateWL(dict, u_literals, partial_assignment)
        if not u_literals:
            # If the unit prop returned False then there was a ComplementPair conflict
            return

    # If the partial assignment is full then return it
    if 0 not in partial_assignment.values():
        return partial_assignment

    nextVariable = lefv if (lefv != None) else getNextVariable(orderVars, partial_assignment)

    for branchLiteral in [nextVariable, -nextVariable]:
        # Set the branch variable
        units = setVar(dict, branchLiteral, partial_assignment)

        # If the branching variable led to an empty clause then try the other variable
        if units == False:
            continue

        # Branch on the variable that was set
        result = backtrackWL(dict, partial_assignment, units, orderVars)
        if result:
            return result
        
        # Unassign the branch variable if it didnt lead to a solution
        partial_assignment[abs(branchLiteral)] = 0

    # Unset all the unit literals before backtracking
    unassignVars(partial_assignment, u_literals)
    return False

# Sets the variable, updates the dict and partial_assignment
def setVar(dict, var, partial_assignment):
    units = set() # Units found while setting the variable
    partial_assignment[abs(var)] = var # Set the variable in the partial_assignment
    
    newList = [] # Clauses that should remain in the watch literal
    for count, clause in enumerate(dict[-var]):
        # If the clause is already true then it keep being watched by that literal, and skip it
        if isClauseSat(clause, partial_assignment):
            newList.append(clause)
            continue
        
        unassigned_variables = [literal for literal in clause if partial_assignment[abs(literal)] == 0]
        
        # The clause is unsat and has no free variables so it is an empty clause
        if not unassigned_variables:
            newList = newList + dict[-var][count:0]
            dict[-var] = newList
            return False
        # The clause is unsat but has one free variable so it is a unit literal
        elif len(unassigned_variables) == 1:
            units.add(unassigned_variables[0])
            newList.append(clause)
        # The clause is unsat and has >1 free variable so it is possible to switch the watch literal
        else:
            if clause == [-47, -42, 38]:
                print(count(dict, clause))
                print()

            newLiteral = nextWatchLiteral(dict, clause, unassigned_variables)
            dict[newLiteral].append(clause)
    
    dict[-var] = newList
    
    # Return all the unit literals that have been found
    return units

# Sets the variable, updates the dict and partial_assignment
def setVarLEFV(dict, var, partial_assignment, lefvArr):
    units = set() # Units found while setting the variable
    partial_assignment[abs(var)] = var # Set the variable in the partial_assignment
    
    newList = [] # Clauses that should remain in the watch literal
    for count, clause in enumerate(dict[-var]):
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
            if clause == [-47, -42, 38]:
                print(count(dict, clause))
                print()

            newLiteral = nextWatchLiteral(dict, clause, unassigned_variables)
            if newLiteral == None:
                print()
            if count(dict, clause) == 3:
                print()
            dict[newLiteral].append(clause)
            lefvArr[0] = newLiteral
    
    if var == -38:
        print()
    dict[-var] = newList
    
    # Return all the unit literals that have been found
    return units

def count(dict, clause):
    count = 0
    for literal in clause:
        if clause in dict[literal]:
            count += 1
    return count


# Given a list of variables, they are set to 0 in the partial assignment (unassigned)
def unassignVars(partial_assignment, vars):
    for var in vars:
        partial_assignment[abs(var)] = 0

# Determines which literal in a clause should be watched
def nextWatchLiteral(dict, clause, unassigned_variables):
    for var in unassigned_variables:
        # If the literal is not already a watched literal
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



fp = 'sat_instances/'

# clauses = load_dimacs(fp +'unsat.txt')
# clauses = load_dimacs(fp +'sat.txt')
# clauses = load_dimacs(fp +'customSAT.txt')
# clauses = load_dimacs(fp +'W_2,3_ n=8.txt')
# clauses = load_dimacs(fp +'PHP-5-4.txt')
# clauses = load_dimacs(fp +'LNP-6.txt')
clauses = load_dimacs(fp +'gt.txt')
# clauses = load_dimacs(fp +'8queens.txt')

# print(dpll_sat_solve(clauses))

print(np.mean(np.array(timeit.repeat('dpll_sat_solve(clauses)', globals=globals(), number=10, repeat=100))))