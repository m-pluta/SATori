from WL import dpll_sat_solve
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
    fileName = f'sat_instances/uf20/uf20-0{fileCount}.cnf'
    print(fileCount)
    sat_instance = load_dimacs(fileName)
    result = dpll_sat_solve(sat_instance)
    if not result:
        print(fileName)
        sys.exit()

print("flat50")
for fileCount in range(1, 1000):
    if fileCount != 73:
        fileName = f'sat_instances/flat50/flat50-{fileCount}.cnf'
        print(fileCount)
        sat_instance = load_dimacs(fileName)
        result = dpll_sat_solve(sat_instance)
        if not result:
            print(fileName)
            sys.exit()

print("CBS")
for clauseCount in [403]:
    for backboneSize in [10, 30, 50, 70, 90]:
        mainFileName = f'CBS_k3_n100_m{clauseCount}_b{backboneSize}'
        for (fileCount) in range(0, 1000):
            print(fileCount)
            fileName = f'sat_instances/{mainFileName}/{mainFileName}_{fileCount}.cnf'
            sat_instance = load_dimacs(fileName)
            result = dpll_sat_solve(sat_instance)
            if not result:
                print(fileName)
                sys.exit()

print("sw100")
for p in range(0,2):
    mainFileName = f'sat_instances/sw100-8-lp{p}-c5/SW100-8-{p}/sw100'
    for (fileCount) in range(1, 101):
        if fileCount != 16:
            print(fileCount)
            fileName = f'{mainFileName}-{fileCount}.cnf'
            sat_instance = load_dimacs(fileName)
            result = dpll_sat_solve(sat_instance)
            if not result:
                print(fileName)
                sys.exit()
            

