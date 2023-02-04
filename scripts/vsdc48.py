# Imports
import numpy
import copy
import re


# Open file and read lines
file = open('sat.txt', 'r')
lines = file.readlines()

# Read metadata from DIMACS file
result = re.search(r"^p cnf (\d+) (\d+)$", lines[0])
numVariable = result.groups()[0]
numClause = result.groups()[1]

# Read all clauses
clauses = []
for i in range(1, len(lines)):
    split = lines[i].split(' ')
    if split[0] != 'c':
        split.pop()
        clauses.append(split)


# Testing
print(numVariable)
print(numClause)
print(clauses)