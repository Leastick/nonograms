class Level:
    def __init__(self, path):
        self.rows = []
        self.columns = []
        with open(path, 'r') as f:
            self.n = int(f.readline())
            f.readline()
            for i in range(self.n):
                self.rows.append(list(map(int, f.readline().split())))
            f.readline()
            for i in range(self.n):
                self.columns.append(list(map(int, f.readline().split())))

    def row_iterator(self, field):
        for i in range(self.n):
            yield field[i]

    def column_iterator(self, field):
        for i in range(self.n):
            yield [field[j][i] for j in range(self.n)]

    def find_blocks(self, line):
        blocks = []
        block_len = 0
        for i in range(self.n):
            if line[i]:
                block_len += 1
            else:
                if block_len > 0:
                    blocks.append(block_len)
                block_len = 0
        if block_len > 0:
            blocks.append(block_len)
        return blocks

    def check_answer(self, field):
        for index, row in enumerate(self.row_iterator(field)):
            blocks = self.find_blocks(row)
            if blocks != self.rows[index]:
                return False
        for index, column in enumerate(self.column_iterator(field)):
            blocks = self.find_blocks(column)
            if blocks != self.columns[index]:
                return False
        return True
