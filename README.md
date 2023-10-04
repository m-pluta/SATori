# SAT Solver

This project, developed during my first year at university for coursework, implements a SAT solver for the Boolean Satisfiability Problem (SAT). It incorporates several advanced techniques inspired by research papers I discovered online.

The solver utilizes the "watched literal" technique, significantly improving performance over brute force or standard DPLL methods. Additionally, it employs the "Last-Encountered-Free-Variable" heuristic and includes a single iteration of "Pure Literal Elimination" at the outset, enhancing solving efficiency.

While Pure Literal Elimination may not offer asymptotic advantages, due to my preprocessing, it proves beneficial during the initial solving phase.

## Usage

The project contain two main files which are `vsdc48.py` and `regularDPLL.py`.

- `vsdc48.py` contains the most optimised algorithm.

- `regularDPLL.py` contains my version of the standard DPLL algorithm which I used to compare my optimised algorithm to.

The sat instances are contained within the /sat_instances folder

```python

# Load the clause set
clauses = load_dimacs('sat_instances/8queens.txt')

# Find one (of potentially many) variable assignments that solves the clause set
solution = dpll_sat_solve(clauses)

print(solution)
```

The `regularDPLL.py` contains a different algorithm under the same name 'dpll_sat_solve'

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
