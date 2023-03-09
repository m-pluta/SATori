from WL import dpll_sat_solve
from vsdc48 import check_truth_assignment
import timeit
import sys

def load_dimacs(filepath):
    # Open file and read lines
    file = open(filepath, 'r')
    lines = file.readlines()
    
    clauses = []
    for line in lines:
        if line[0] == '%':
            break
        if line[0] not in ('c', 'p'):
            clauses.append([int(literal) for literal in line.split() if literal != '0'])
    return clauses

print("uf20")
for fileCount in range(1, 1001):
    fileName = f'instances-sat/uf20-0{fileCount}.cnf'
    print(fileCount)
    sat_instance = load_dimacs(fileName)
    result = dpll_sat_solve(sat_instance)
    if not result:
        print(fileName)
        print('Oops')
        sys.exit()
    # else:
    #     print(check_truth_assignment(sat_instance, result))

print("flat50")
for fileCount in range(1, 1000):
    if fileCount != 73:
        fileName = f'instances-sat2/flat50-{fileCount}.cnf'
        print(fileCount)
        sat_instance = load_dimacs(fileName)
        result = dpll_sat_solve(sat_instance)
        if not result:
            print(fileName)
            print('Oops')
            sys.exit()
        # else:
        #     print(check_truth_assignment(sat_instance, result))

print("CBS")
for clauseCount in [403]:
    for backboneSize in [10, 30, 50, 70, 90]:
        mainFileName = f'CBS_k3_n100_m{clauseCount}_b{backboneSize}'
        for (fileCount) in range(0, 1000):
            print(fileCount)
            fileName = f'{mainFileName}/{mainFileName}_{fileCount}.cnf'
            sat_instance = load_dimacs(fileName)
            result = dpll_sat_solve(sat_instance)
            if not result:
                print(fileName)
                print('Oops')
                sys.exit()
            # else:
            #     print(check_truth_assignment(sat_instance, result))

print("sw100")
for p in range(0,2):
    mainFileName = f'sw100-8-lp{p}-c5/SW100-8-{p}/sw100'
    for (fileCount) in range(1, 101):
        if fileCount != 16:
            print(fileCount)
            fileName = f'{mainFileName}-{fileCount}.cnf'
            sat_instance = load_dimacs(fileName)
            result = dpll_sat_solve(sat_instance)
            if not result:
                print(fileName)
                print('Oops')
                sys.exit()
            else:
                print(check_truth_assignment(sat_instance, result))
            

