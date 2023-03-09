from vsdc48 import *

def testSuite1(showResult=True):
    clauses = load_dimacs('instances/unsat.txt')
    result = branching_sat_solve(clauses)
    assert result == False

    clauses = load_dimacs('instances/sat.txt')
    result = branching_sat_solve(clauses)
    assert result == [1, -2]
    clauses = load_dimacs('instances/sat.txt')
    assert check_truth_assignment(clauses, result)

    clauses = load_dimacs('instances/W_2,3_ n=8.txt')
    result = branching_sat_solve(clauses)
    clauses = load_dimacs('instances/W_2,3_ n=8.txt')
    assert check_truth_assignment(clauses, result)

    clauses = load_dimacs('instances/PHP-5-4.txt')
    result = branching_sat_solve(clauses)
    assert result == False

    clauses = load_dimacs('instances/LNP-6.txt')
    result = branching_sat_solve(clauses)
    assert result == False

    clauses = load_dimacs('instances/8queens.txt')
    result = branching_sat_solve(clauses)
    clauses = load_dimacs('instances/8queens.txt')
    assert check_truth_assignment(clauses, result)
    if showResult:
        print('All tests passed')

def testSuite2(showResult=True):
    assert containsComplementPair([-1, 1])
    assert containsComplementPair([-1, -1, -1, 1])
    assert not containsComplementPair([1,2,3])
    assert containsComplementPair([2, 1, 5, -2, 4])
    assert not containsComplementPair([1, 2, 3, 4, 5])
    
    if showResult:
        print('All tests passed')

def testSuite3(showResult=True):
    clauses = load_dimacs('instances/sat.txt')
    assert setVar(clauses, 1) == [[-2]]
    assert setVar(clauses, -1) == [[]]
    assert setVar(clauses, 2) == [[1], [1, -1], [-1]]
    assert setVar(clauses, -2) == [[1], [1, -1]]

    assert setVars(clauses, [1, -2]) == []
    assert setVars(clauses, [1, 2]) == [[]]

    clauses = load_dimacs('instances/dpllSAT.txt')
    assert testDPLLsolution(clauses, [1])
    assert testDPLLsolution(clauses, [5])
    assert not testDPLLsolution(clauses, [3])

    clauses = load_dimacs('instances/8queens.txt')
    assignment = [1,-11,-12,13,-18,-23]
    assert not testDPLLsolution(clauses, assignment)
    assert testDPLLsolution(clauses, assignment + [-26])
    assert testDPLLsolution(clauses, assignment + [-26, -2])

    if showResult:
        print('All tests passed')

def testSuite4(showResult=True):
    clauses = load_dimacs('instances/unsat.txt')
    assert dpll_sat_solve(clauses) == False
    clauses = load_dimacs('instances/sat.txt')
    assert dpll_sat_solve(clauses) == []
    assert testDPLLsolution(clauses, [])
    clauses = load_dimacs('instances/customSAT.txt')
    assert dpll_sat_solve(clauses) == [3]
    assert testDPLLsolution(clauses, [3])
    clauses = load_dimacs('instances/W_2,3_ n=8.txt')
    assert dpll_sat_solve(clauses) == [-4, -13, -10]
    assert testDPLLsolution(clauses, [-4, -13, -10])
    clauses = load_dimacs('instances/PHP-5-4.txt')
    assert dpll_sat_solve(clauses) == False
    clauses = load_dimacs('instances/LNP-6.txt')
    assert dpll_sat_solve(clauses) == False
    clauses = load_dimacs('instances/8queens.txt')
    assert dpll_sat_solve(clauses) == [-28, -37, -29, -43, -18, -38, -12, -46, -27, -23, -49, -8, -35, -13, -55, -44, -2, -57, -24, -54, -39, -10, -59, -4, -33, -21, 30, -47, -36, -61, -41, -56, -1, -45]
    assert testDPLLsolution(clauses, [-28, -37, -29, -43, -18, -38, -12, -46, -27, -23, -49, -8, -35, -13, -55, -44, -2, -57, -24, -54, -39, -10, -59, -4, -33, -21, 30, -47, -36, -61, -41, -56, -1, -45])

    if showResult:
        print('All tests passed')

def runAllTests():
    testSuite1(False)
    testSuite2(False)
    testSuite3(False)
    testSuite4(False)

    print("All tests completed successfully")

def testDPLLsolution(clause_set, dpllSol):
    clause_set = setVars(clause_set, dpllSol)

    unit_literals = set([clause[0] for clause in clause_set if len(clause) == 1])
    while (unit_literals):
        clause_set = UP(clause_set, unit_literals)
        if clause_set is None:
            return False
        unit_literals = set([clause[0] for clause in clause_set if len(clause) == 1])

    return True if clause_set == [] else False

def setVars(clause_set, vars):
    for var in vars:
        clause_set = setVar(clause_set, var)
    return clause_set

def setVar(clause_set, var):
    new_clause_set = []
    
    for clause in clause_set:
        if var not in clause:
            clause_copy = clause[:]
            if (-1 * var) in clause_copy:
                clause_copy.remove(-1 * var)
            new_clause_set.append(clause_copy)

    return new_clause_set


# runAllTests()

# clauses = load_dimacs('instances/unsat.txt')
# clauses = load_dimacs('instances/sat.txt')
# clauses = load_dimacs('instances/customSAT.txt')
clauses = load_dimacs('instances/W_2,3_ n=8.txt')
# clauses = load_dimacs('instances/PHP-5-4.txt')
# clauses = load_dimacs('instances/LNP-6.txt')
# clauses = load_dimacs('instances/8queens.txt')

# print("dpll", np.mean(np.array(timeit.repeat('dpll_sat_solve(clauses)', globals=globals(), number=1, repeat=1))))

# print(dpll_sat_solve(clauses))
