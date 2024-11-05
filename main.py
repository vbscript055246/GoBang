import random

from Board import Board
from MCTS import MCTS, State, get_opponent
from Human import Human

SIZE = 15

# 第一步外圍開局，也協助後續搜索可以進行
def start_move_for_COM(game, COM_MARK):
    x, y = random.choice([0, 1, SIZE - 2, SIZE - 1]), random.choice([0, 1, SIZE - 2, SIZE - 1])
    while not game.make_move(COM_MARK, x=x, y=y):
        x, y = random.choice([0, 1, SIZE - 2, SIZE - 1]), random.choice([0, 1, SIZE - 2, SIZE - 1])


if __name__ == '__main__':

    mode = int(input('1.)人機\n2.)機人\n3.)機機\n'))
    
    game = Board()

    if mode == 1 or mode == 2:     # 人 v.s. 機 對戰模式

        COM_MARK = get_opponent('◯') if mode % 2 else '◯'
        while not game.check_connect():
            if game.step() % 2 == mode % 2:
                # COM 回合
                # 前幾步隨機下
                if game.step() <= 1:
                    start_move_for_COM(game, COM_MARK)
                else:   # 使用UCT思考
                    _code = MCTS().take_action(State(game.table, COM_MARK))
                    game.make_move(COM_MARK, s_code=_code)
            else:
                # Human 回合
                # 啟動選擇落子介面
                _code = Human(game.table).select()
                while not game.make_move(COM_MARK, s_code=_code):
                    print('Invalid input')
                    _code = Human(game.table).select()

            game.show()
            COM_MARK = get_opponent(COM_MARK)
        # 印出勝負
        print(game.result())

    elif mode == 3:     # 機機對戰模式

        COM_MARK = '◯'
        while not game.check_connect():
            if game.step() <= 1:    # 前幾步隨機下
                start_move_for_COM(game, COM_MARK)
            else:   # 使用UCT思考
                _code = MCTS().take_action(State(game.table, COM_MARK))
                game.make_move(COM_MARK, s_code=_code)
            game.show()
            COM_MARK = get_opponent(COM_MARK)
        # 印出勝負
        print(game.result())




