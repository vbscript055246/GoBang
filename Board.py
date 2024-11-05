SIZE = 15


class Board:
    def __init__(self):
        self.table = [['。' for i in range(SIZE)] for j in range(SIZE)]
        self.pre_move_x = -1
        self.pre_move_y = -1
        self.history_path = []

    # 回傳勝負
    def result(self):
        return f'{self.table[self.pre_move_y][self.pre_move_x]} Win!!!'

    # 回傳目前步數
    def step(self):
        return len(self.history_path)

    # 顯示盤面
    def show(self):
        for i in range(SIZE):
            print(''.join(self.table[i]))

    # 執行走步，回傳是否成功
    def make_move(self, mark, x=-1, y=-1, s_code=''):
        if x == -1 and y == -1:
            x, y = s_code.split(',')
            x, y = int(x), int(y)

        if 0 <= x < SIZE and 0 <= y < SIZE and self.table[y][x] == '。':
            self.table[y][x] = mark
            self.pre_move_x, self.pre_move_y = x, y
            if x == -1 and y == -1:
                print(f'{mark}: {s_code}')
            else:
                print(f'{mark}: {x},{y}')
            self.history_path.append([mark, s_code])
            return True
        else:
            # print(f"invalid move {y},{x}")
            return False

    # 是否遊戲結束
    def check_connect(self):
        if self.pre_move_x == -1 and self.pre_move_y == -1:
            return False
        # 定出要找的四條線
        way = [[1, 1], [0, 1], [1, 0], [-1, 1]]
        # 根據這四個方向加和減搜索
        for i in range(4):
            dx, dy = way[i][0], way[i][1]
            # 從前一步找起
            check_x, check_y = self.pre_move_x, self.pre_move_y
            mark = self.table[check_y][check_x]
            count = -1
            # 加搜索
            while self.table[check_y][check_x] == mark:
                count += 1
                check_y += dy
                check_x += dx
                if 0 < check_y < SIZE and 0 < check_x < SIZE:
                    continue
                break
            check_x, check_y = self.pre_move_x, self.pre_move_y
            # 減搜索
            while self.table[check_y][check_x] == mark:
                count += 1
                check_y -= dy
                check_x -= dx
                if 0 < check_y < SIZE and 0 < check_x < SIZE:
                    continue
                break
            if count >= 5:
                return True
        return False
