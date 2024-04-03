import pulp


class LinearCore:
    hours = 8  # 每天可工作时长为8h
    days = 22  # 每月工作22天
    fine = 0.5  # 每月库存费

    price = [10, 9, 3, 5, 11, 9, 8]  # 第i件商品可获得的利润

    F = [[600, 800, 200, 0, 700, 300, 200],
         [500, 600, 300, 300, 500, 200, 250],
         [200, 500, 400, 200, 500, 0, 300],
         [300, 400, 0, 400, 300, 500, 100],
         [0, 200, 300, 200, 900, 200, 0],
         [400, 300, 100, 300, 800, 400, 100]]  # 第i月，第j个商品的销售限额

    Time = [[0.6, 0.7, 0, 0.3, 0.6, 0, 0.5],
            [0.1, 0.1, 0, 0.3, 0, 0.6, 0],
            [0.2, 0, 0.4, 0, 0.2, 0, 0.6],
            [0.05, 0.08, 0, 0.06, 0.1, 0, 0.08],
            [0, 0, 0.01, 0, 0.05, 0.08, 0.05]]  # 第j个商品在第num号机器上所需的加工时间

    Machine = [[4, 3, 4, 2, 1],
               [6, 2, 4, 2, 1],
               [6, 3, 4, 1, 1],
               [6, 3, 3, 2, 1],
               [5, 2, 4, 2, 1],
               [6, 3, 3, 2, 0]]  # 第i月，第num号机器的数量

    def __int__(self):
        pass

    def reset_f(self, F):
        self.F = F

    def reset_time(self,Time):
        self.Time = Time

    def reset_machine(self,Machine):
        self.Machine = Machine

    def reset_price(self,price):
        self.price = price

    def solveP(self):
        K = [pulp.LpVariable(f'k_{i}', lowBound=0) for i in range(6)]
        N = [[pulp.LpVariable(f'N_{j}_{i}', lowBound=0, cat='Integer') for j in range(7)] for i in range(6)]
        M = [[pulp.LpVariable(f'M_{j}_{i}', lowBound=0, cat='Integer') for j in range(7)] for i in range(6)]
        X = [[pulp.LpVariable(f'X_{j}_{i}', lowBound=0, cat='Integer') for j in range(7)] for i in range(6)]

        prob = pulp.LpProblem("Maximize Profit", pulp.LpMaximize)

        prob += K[5] + sum(N[5][j] * self.price[j] for j in range(7)) - self.fine * sum(X[5][j] for j in range(7))

        for j in range(7):
            prob += X[5][j] + M[5][j] - N[5][j] == 60
        # 1月初不存在零件库存量
        for j in range(7):
            prob += X[0][j] == 0
        # 初始利润为0
        prob += K[0] == 0

        for i in range(6):
            for j in range(7):
                prob += X[i][j] <= 100
                prob += X[i][j] >= 0
                prob += M[i][j] >= 0
                prob += N[i][j] >= 0

        for i in range(5):
            for j in range(7):
                prob += X[i + 1][j] == X[i][j] + M[i][j] - N[i][j]

        for i in range(5):
            prob += K[i + 1] == K[i] + sum(N[i][j] * self.price[j] for j in range(7)) - sum(X[i][j] * self.fine for j in range(7))

        for i in range(6):
            for j in range(7):
                prob += N[i][j] <= self.F[i][j]
                prob += N[i][j] <= X[i][j] + M[i][j]

        for i in range(6):
            for num in range(5):
                prob += sum(self.Time[num][j] * M[i][j] for j in range(7)) <= self.hours * self.days * self.Machine[i][num]

        prob.solve()

        return pulp.value(prob.objective)