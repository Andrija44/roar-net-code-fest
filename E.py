import math

class Problem:
    def __init__(self, villageNum, cords, candleLenght, burnRate):
        self.villageNum = villageNum
        self.cords = cords
        self.candleLenght = candleLenght
        self.burnRate = burnRate

        self.lb = 0

    def __str__(self):
        return f"Villages: {self.villageNum}\nCords: {self.cords}\nCandle lenght: {self.candleLenght}\nBurn rates: {self.burnRate}\nlb: {self.lb}"

    # construct empty solution
    def empty_solution(self):
        return Solution(self, [], 0, 0, self.lb)

    # construct neigbourhood (next available moves)
    def construction_neighbourhood(self):
        return Neighbourhood(self)

    @classmethod
    def from_textio(cls, f):
        villageCnt = int(f.readline())
        cords = []
        candleLen = []
        burnRate = []
        cords.append(list(map(int, f.readline().split(" "))))

        for line in f:
            splitLine = line.split(" ")
            cords.append(list(map(int, splitLine[:2])))
            candleLen.append(int(splitLine[2]))
            burnRate.append(int(splitLine[3]))

        return cls(villageCnt, cords, candleLen, burnRate)

class Solution:
    def __init__(self, problem, visited, curr, distance, lb):
        self.problem = problem # instance of Problem class
        self.visited = visited # current solution
        self.curr = curr
        self.distance = distance
        self.lb = lb

    def __str__(self):
        return f"\tVisited: {self.visited}\n\tlb: {self.lb}\n\tDistance: {self.distance}"

    def objective_value(self): # value of the best solution
        for elem in range(1, self.problem.villageNum):
            if elem in self.visited:
                continue
            dist = abs(self.problem.cords[self.curr][0] - self.problem.cords[elem][0]) + abs(self.problem.cords[self.curr][1] - self.problem.cords[elem][1])
            if (self.problem.candleLenght[elem - 1] - (self.distance + dist) * self.problem.burnRate[elem - 1]) > 0:
                return None
        return self.lb

    def lower_bound(self):
        return self.lb
    
    def to_textio(self, f) -> None: # output the current solution
        f.write('\n'.join(str(elem) for elem in self.visited))

class Neighbourhood:
    def __init__(self, problem):
        self.problem = problem # instance of the Problem class

    def moves(self, solution):
        if len(solution.visited) < (self.problem.villageNum - 1):
            for i in range(1, self.problem.villageNum):
                if i == solution.curr or i in solution.visited:
                    continue
                dist = abs(self.problem.cords[solution.curr][0] - self.problem.cords[i][0]) + abs(self.problem.cords[solution.curr][1] - self.problem.cords[i][1])
                if (self.problem.candleLenght[i - 1] - (solution.distance + dist) * self.problem.burnRate[i - 1]) <= 0:
                    continue
                yield Move(self, i)

class Move:
    def __init__(self, neighbourhood, village):
        self.neighbourhood = neighbourhood # instance of Neighbourhood class
        self.village = village
        self.lb_incr = None # lower bound increment for the current move
    
    def __str__(self):
        return f"Select node {self.village}"

    def lower_bound_increment(self, solution):
        if self.lb_incr is None:
            dist = abs(solution.problem.cords[solution.curr][0] - solution.problem.cords[self.village][0]) + abs(solution.problem.cords[solution.curr][1] - solution.problem.cords[self.village][1])
            dist += solution.distance
            self.lb_incr = solution.problem.candleLenght[self.village - 1] - (solution.problem.burnRate[self.village - 1] * dist)
            if self.lb_incr < 0:
                self.lb_incr = 0
                return math.inf
        return 1 / self.lb_incr
    
    def apply_move(self, solution):
        solution.visited.append(self.village)
        solution.distance += abs(solution.problem.cords[solution.curr][0] - solution.problem.cords[self.village][0]) + abs(solution.problem.cords[solution.curr][1] - solution.problem.cords[self.village][1])
        solution.curr = self.village
        solution.lb += self.lb_incr
        # print(f"In village {self.village}, lb_incr: {self.lb_incr} and solution\n{solution}")
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

    # print(f"-- Problem --\n{problem}")

    solution = alg.greedy_construction(problem)

    solution.to_textio(sys.stdout)
    # print(f"-- Solution --\n{solution}")