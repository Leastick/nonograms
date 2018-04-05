TEXT_BLOCK_COEF = 5


class Field:
    def __init__(self, n, cell_side):
        self.n = n
        self.cell_side = cell_side
        self.state = [[0] * n for _ in range(n)]

    def switch_state(self, x, y):
        self.state[x][y] = (self.state[x][y] + 1) % 3
        return self.state[x][y]

