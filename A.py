class Problem:
    def __init__(self, peoNum, connNum, fees, connections):
        self.peoNum = peoNum # number of people (vertices)
        self.connNum = connNum # number of connections (edges)
        self.fees = fees # price of vertex
        self.connections = connections # list of connections (edges)

        self.lb = 0 # starting lower bound

    def __str__(self):
        return f"People: {self.peoNum}, Connections: {self.connNum}\nFees: {self.fees}\nConnections: {self.connections}"

    # construct empty solution
    def empty_solution(self):
        return Solution(self, [], 0, self.lb)

    # construct neigbourhood (next available moves)
    def construction_neighbourhood(self):
        return Neighbourhood(self)

    @classmethod
    def from_textio(cls, f): # create instance of the class and populate it with data from the input file
        people, conns = map(int, f.readline().split(" "))
        fees = list(map(int, f.readline().split(" ")))
        conn = []
        for line in f:
            conn.append(list(map(int, line.split(" "))))

        return cls(people, conns, fees, conn)

class Solution:
    def __init__(self, problem, selected, k, lb):
        self.problem = problem # instance of Problem class
        self.selected = selected # current solution
        self.k = k # current connection (index in the connections list)
        self.lb = lb # lower bound of the current solution

    def __str__(self):
        return f"\tSelected: {self.selected}\n\tLB: {self.lb}"

    def objective_value(self): # value of the best solution
        for conns in self.problem.connections:
            if any(elem in self.selected for elem in conns):
                return self.lb
        return None

    def lower_bound(self):
        return self.lb
    
    def to_textio(self, f) -> None: # output the current solution
        f.write(' '.join(str(elem) for elem in self.selected))

class Neighbourhood:
    def __init__(self, problem):
        self.problem = problem # instance of the Problem class

    def moves(self, solution):
        if solution.k < len(self.problem.connections):
            elems = self.problem.connections[solution.k] # take vertices in current connection
            if any(elem in solution.selected for elem in elems): # check if one of the vertices is in the list selected
                elems = list(set(solution.selected) & set(elems))
            for elem in elems: # generate move for each applicable vertex
                yield Move(self, elem)

class Move:
    def __init__(self, neighbourhood, v):
        self.neighbourhood = neighbourhood # instance of Neighbourhood class
        self.v = v # vertex
        self.lb_incr = None # lower bound increment for the current move
    
    def __str__(self):
        return f"Select node {self.v}"
    
    def lower_bound_increment(self, solution):
        if self.lb_incr is None:
            self.lb_incr = solution.problem.fees[self.v - 1] # (we are working on maximization)
        return self.lb_incr
    
    def apply_move(self, solution):
        solution.k += 1 # increase the counter to the next connection
        if self.v not in solution.selected: # check if the current vertex is in the list selected, if not add it
            solution.lb += self.lower_bound_increment(solution)
            solution.selected.append(self.v)
        return solution

# default api call
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