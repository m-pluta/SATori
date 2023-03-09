# Imports
import timeit
import numpy as np
from collections import Counter
from itertools import chain
from printUtils import printTime
from vsdc48 import load_dimacs, containsComplementPair, check_truth_assignment

class WL_Solver:
    # Main variables
    clause_set = None
    vars = None
    initial_unit_iterals = set()
    dict = {}
    partial_assignment = None
    varOrder = []

    # Initialises the SAT solver
    def __init__(self, clause_set):
        self.clause_set = clause_set
        self.dictify()
        self.createPartialAssignment()

    # Return the watched literal dict, initial unit_literals, frequency order of variables
    def dictify(self):
        # Count all literals
        self.vars = Counter(chain.from_iterable(self.clause_set))

        # Order the variables
        self.orderVars()
        
        # Initialise each literal in the dict with an empty list
        self.initialiseWatchedLiterals()

        # Go through each clause set and identify them as a unit clause or give them two watched-literals
        for clause in self.clause_set:
            if len(clause) == 1:
                self.initial_unit_literals.add(clause[0])
                continue
            if clause not in self.dict[clause[0]]:
                self.dict[clause[0]].append(clause)
                self.dict[clause[1]].append(clause)

    # Returns the variables ordered in descending order of occurrence given a Counter object
    def orderVars(self):
        # Order the variables in descending order of occurrence
        for var in self.vars.most_common():
            # If the literal's complement is already in the order then don't append it
            if -var[0] not in self.varOrder:
                self.varOrder.append(var[0])
        
    def initialiseWatchedLiterals(self):
        for var in self.varOrder:
            self.dict[var] = []
            self.dict[-var] = []
        # Potential alternative:
        # watched_literals = dict.fromkeys(vars.keys(), [])

    # Initialises a dictionary with 0s for each variable
    def createPartialAssignment(self):
        self.partial_assignment = dict.fromkeys([abs(var) for var in self.varOrder], 0)

    def solve(self):
        # Attempt to find solution
        result = self.backtrack(self.initial_unit_iterals)
        
        # If there is a result, convert it from dictionary to list 
        return [i for i in result.values()] if result else False

    def unit_propagate(self, units):
        # Init
        units_propagated = [] # Unit literals that have so far been set to true
        u_literals = list(units)

        while u_literals:
            # If there is complement pair in the literal list then there is a conflict
            # e.g. if 1 and -1 are in the list then both of them cannot be true
            if containsComplementPair(u_literals):
                # Unassign all the variables that have been so far set to true during unit prop and return
                self.unassignVars(units_propagated)
                return False
            
            # Dequeue next unit literal
            var = u_literals.pop(0)

            # Set the unit literal to true and add new unit literals to the queue
            newUnits = self.setVar(var)
            u_literals.extend(list(newUnits))

            units_propagated.append(var)

        return units_propagated

    # Main function
    def backtrack(self, u_literals):
        # Unit propagate over all the unit literals
        if u_literals:
            # Unit Propagate functions returns all units that were recursively propagated
            # i.e. Provided units could have led to more unit literals
            u_literals = self.unit_propagate(u_literals)
            if not u_literals:
                # If the unit prop returned False then there was a ComplementPair conflict
                return

        # If the partial assignment is full then return it, it must be correct
        if 0 not in self.partial_assignment.values():
            return self.partial_assignment
        

        # if Φ contains an empty clause then
        #     return false


        nextVariable = self.getNextVariable()

        # Branch to the positive and negative literals
        for branchLiteral in [nextVariable, -nextVariable]:
            # Set the variable
            units = self.setVar(branchLiteral)

            # If the branching variable led to an empty clause
            # then try the other variable, or backtrack by exiting for each loop
            if units == False:
                continue

            # Branch on the variable that was set
            result = self.backtrack(units)
            if result:
                return result
            
            # Unassign the set variable if it didnt lead to a solution
            self.partial_assignment[abs(branchLiteral)] = 0

        # Unset all the unit literals before backtracking
        self.unassignVars(u_literals)
        return False

    # Sets the variable, updates the dict and partial_assignment
    def setVar(self, var):
        units = set() # Units found while setting the variable
        self.partial_assignment[abs(var)] = var # Set the variable in the partial_assignment
        
        newList = [] # Clauses that should remain in the watch literal
        for clause in self.dict[-var]:
            # If the clause is already true then it keep being watched by that literal, and skip it
            if self.isClauseSat(clause):
                newList.append(clause)
                continue
            
            unassigned_variables = [literal for literal in clause if self.partial_assignment[abs(literal)] == 0]
            
            # The clause is unsat and has no free variables so it is an empty clause
            if not unassigned_variables:
                return False
            # The clause is unsat but has one free variable so it is a unit literal
            elif len(unassigned_variables) == 1:
                units.add(unassigned_variables[0])
                newList.append(clause)
            # The clause is unsat and has >1 free variable so it is possible to switch the watch literal
            else:
                newLiteral = self.nextWatchLiteral(clause, unassigned_variables)
                self.dict[newLiteral].append(clause)
        
        self.dict[-var] = newList # Update the dict
        return units # Return all the unit literals that have been found

    # Given a list of variables to unassign, they are set to 0 in the partial assignment
    def unassignVars(self, vars):
        for var in vars:
            self.partial_assignment[abs(var)] = 0

    # Determines which literal in a clause should be watched
    def nextWatchLiteral(self, clause, unassigned_variables):
        for var in unassigned_variables:
            # If the literal is not a watched literal already
            if clause not in self.dict[var]:
                return var
        return None

    # Checks if a given clause is True
    def isClauseSat(self, clause):
        for literal in clause:
            # Check if any variable in the partial assignment satisfies the clause
            if self.partial_assignment[abs(literal)] == literal:
                return True
        return False

    # Returns the most common free variable
    def getNextVariable(self):
        for var in self.varOrder:
            # Returns variable if it is free
            if self.partial_assignment[abs(var)] == 0:
                return var
        return None
    
def dpll_sat_solve(clause_set, partial_assignment=[]):
    solver = WL_Solver(clause_set)
    return solver.solve()

clauses = load_dimacs('instances/8queens.txt')

sol = dpll_sat_solve(clauses)
print(sol)
if sol:
    print(check_truth_assignment(clauses, sol))

printTime(np.mean(timeit.repeat('dpll_sat_solve(clauses)', globals=globals(), number=1, repeat=100)))