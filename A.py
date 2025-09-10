class Problem:
    def __init__(self, peoNum, connNum, fees, connections):
        self.peoNum = peoNum
        self.connNum = connNum
        self.fees = fees
        self.connections = connections

        self.ub = 0

    def __str__(self):
        return f"People: {self.peoNum}, Connections: {self.connNum}\nFees: {self.fees}\nConnections: {self.connections}"

    def empty_solution(self):
        return Solution(self, [], 0, self.ub)

    def construction_neighbourhood(self):
        return Neighbourhood(self)

    @classmethod
    def from_textio(cls, f):
        people, conns = map(int, f.readline().split(" "))
        fees = list(map(int, f.readline().split(" ")))
        conn = []
        for line in f:
            conn.append(list(map(int, line.split(" "))))

        return cls(people, conns, fees, conn)

class Solution:
    def __init__(self, problem, selected, k, ub):
        self.problem = problem
        self.selected = selected
        self.k = k
        self.ub = ub

    def __str__(self):
        return f"\tSelected: {self.selected}\n\tUB: {self.ub}"

    def objective_value(self):
        for conns in self.problem.connections:
            if any(elem in self.selected for elem in conns):
                return -self.ub
        return None

    def lower_bound(self):
        return -self.ub
    
    def to_textio(self, f) -> None:
        f.write(' '.join(str(elem) for elem in self.selected))

class Neighbourhood:
    def __init__(self, problem):
        self.problem = problem

    def moves(self, solution):
        if solution.k < len(self.problem.connections):
            elems = self.problem.connections[solution.k]
            if any(elem in solution.selected for elem in elems):
                elems = list(set(solution.selected) & set(elems))
            for elem in elems:
                yield Move(self, elem)

class Move:
    def __init__(self, neighbourhood, v):
        self.neighbourhood = neighbourhood
        self.v = v
        self.ub_incr = None
    
    def __str__(self):
        return f"Select node {self.v}"
    
    def _upper_bound_increment(self, solution):        
        if self.ub_incr is None:
            self.ub_incr = -solution.problem.fees[self.v - 1]
        return self.ub_incr
    
    def lower_bound_increment(self, solution):
        return -self._upper_bound_increment(solution)
    
    def apply_move(self, solution):
        solution.k += 1
        if self.v not in solution.selected:
            solution.ub -= self._upper_bound_increment(solution)
            solution.selected.append(self.v)
        return solution

if __name__ == "__main__":
    import sys
    import roar_net_api.algorithms as alg

    if len(sys.argv) >= 2:
        with open(sys.argv[1], "r") as f:
            problem = Problem.from_textio(f)
    else:
        problem = Problem.from_textio(sys.stdin)

    solution = alg.greedy_construction(problem)

    solution.to_textio(sys.stdout)