from copy import deepcopy

import numpy as np
import pandas as pd

SIZE = 15

# Reference
# https://skywalker0803r.medium.com/%E8%92%99%E5%9C%B0%E5%8D%A1%E7%BE%85%E6%90%9C%E7%B4%A2%E6%B3%95-ee7de77940ef
# https://blog.csdn.net/Dina_p/article/details/83932410


def get_opponent(mark):
    return '⬤' if mark == '◯' else '◯'


# 盤面記錄結構
class State:
    def __init__(self, board, player):
        self.current_player = player
        self.board = board

    # TODO 變得更聰明
    def get_posible_actions(self):
        _actions = []
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] == self.current_player:
                    for dy in [-2, -1, 0, 1, 2]:
                        for dx in [-2, -1, 0, 1, 2]:
                            if dx != 0 and dy != 0 and \
                                (0 <= i+dy < SIZE) and (0 <= j+dx < SIZE) and \
                                    self.board[i+dy][j+dx] == '。':
                                _actions.append(f'{j+dx},{i+dy}')
        return _actions

    def get_state_result(self):

        max_count = 0
        checkerboard = self.board

        for i in range(SIZE):
            for j in range(SIZE):
                if checkerboard[i][j] != '。':

                    if i + 1 < SIZE and i + 2 < SIZE and i + 3 < SIZE and i + 4 < SIZE:
                        if checkerboard[i][j] == checkerboard[i + 1][j] and checkerboard[i][j] == checkerboard[i + 2][
                            j] and checkerboard[i][j] == checkerboard[i + 3][j] and checkerboard[i][j] == \
                                checkerboard[i + 4][j]:
                            return True, checkerboard[i][j]
                        else:
                            count1 = 0
                            if checkerboard[i][j] == checkerboard[i + 1][j]:
                                count1 += 1
                            if checkerboard[i][j] == checkerboard[i + 2][j]:
                                count1 += 1
                            if checkerboard[i][j] == checkerboard[i + 3][j]:
                                count1 += 1
                            if checkerboard[i][j] == checkerboard[i + 4][j]:
                                count1 += 1
                            if count1 > max_count:
                                max_count = count1

                    if j + 1 < SIZE and j + 2 < SIZE and j + 3 < SIZE and j + 4 < SIZE:
                        if checkerboard[i][j] == checkerboard[i][j + 1] and checkerboard[i][j] == checkerboard[i][
                            j + 2] and checkerboard[i][j] == checkerboard[i][j + 3] and checkerboard[i][j] == \
                                checkerboard[i][j + 4]:
                            return True, checkerboard[i][j]
                        else:
                            count2 = 0
                            if checkerboard[i][j] == checkerboard[i][j + 1]:
                                count2 += 1
                            if checkerboard[i][j] == checkerboard[i][j + 2]:
                                count2 += 1
                            if checkerboard[i][j] == checkerboard[i][j + 3]:
                                count2 += 1
                            if checkerboard[i][j] == checkerboard[i][j + 4]:
                                count2 += 1
                            if count2 > max_count:
                                max_count = count2

                    if i + 1 < SIZE and i + 2 < SIZE and i + 3 < SIZE and i + 4 < SIZE and j + 1 < SIZE and j + 2 < SIZE and j + 3 < SIZE and j + 4 < SIZE:
                        if checkerboard[i][j] == checkerboard[i + 1][j + 1] and checkerboard[i][j] == \
                                checkerboard[i + 2][j + 2] and checkerboard[i][j] == checkerboard[i + 3][j + 3] and \
                                checkerboard[i][j] == checkerboard[i + 3][j + 4]:
                            return True, checkerboard[i][j]
                        else:
                            count3 = 0
                            if checkerboard[i][j] == checkerboard[i + 1][j + 1]:
                                count3 += 1
                            if checkerboard[i][j] == checkerboard[i + 2][j + 2]:
                                count3 += 1
                            if checkerboard[i][j] == checkerboard[i + 3][j + 3]:
                                count3 += 1
                            if checkerboard[i][j] == checkerboard[i + 4][j + 4]:
                                count3 += 1
                            if count3 > max_count:
                                max_count = count3
        return False, '。'

    def get_next_state(self, action):
        x, y = action.split(",")
        new_state = State(self.board, self.current_player)
        new_state.board[int(y)][int(x)] = self.current_player
        return new_state

# MCTS的節點
# 每個節點具有計算本節點權重、取得隨機走步、選擇較佳的節點進行探索、探索未知節點、向根節點更新權重、從本節點繼續下棋 等功能
class Node:
    def __init__(self, state, parent=None):
        # 儲存盤面
        self.state = deepcopy(state)
        # 可以探索的走步
        self.untried_actions = state.get_posible_actions()
        # 父節點
        self.parent = parent
        # 儲存哪接走步可以到哪個子節點
        self.children = {}
        # 計算權重用
        self.R = 0      # 該節點的贏的次數
        self.N = 0      # 該節點的總次數
                        # 總次數可以由父節點取得

    # 計算本節點權重
    def weight_func(self, c_param=1.4):
        if self.N != 0:
            # c_param 講義上是寫1，網路上有各種不同的參數，是可能可以變聰明的點
            w = -self.R / self.N + c_param * np.sqrt(2 * np.log(self.parent.N) / self.N)
        else:
            w = 0.0
        return w

    # 取得隨機走步
    @staticmethod
    def get_random_action(actions):
        _index = np.random.choice(range(len(actions)))
        return actions[_index]

    # 選擇較佳的節點進行探索
    def select(self, c_param=1.4):
        weights = [child_node.weight_func(c_param) for child_node in self.children.values()]
        action = pd.Series(data=weights, index=self.children.keys()).idxmax()
        next_node = self.children[action]
        return action, next_node

    # 探索未知節點
    def expand(self):
        # 未知節點
        action = self.untried_actions.pop()
        # 獲得下下看的局面
        next_board = self.state.board.copy()
        x, y = action.split(',')
        next_board[int(y)][int(x)] = self.state.current_player
        state = State(next_board, get_opponent(self.state.current_player))
        # 產生出新的child
        child_node = Node(state, self)
        self.children[action] = child_node
        return child_node

    # 向根節點更新權重
    def update(self, winner):
        # 更新自己
        self.N += 1
        opponent = get_opponent(self.state.current_player)
        if winner == self.state.current_player:
            self.R += 1
        elif winner == opponent:
            self.R -= 1

        # 向上更新
        if self.is_root_node():
            self.parent.update(winner)

    # 從本節點繼續下棋
    def rollout(self):
        current_state = deepcopy(self.state)

        # 下到有結果
        while True:
            is_over, winner = current_state.get_state_result()

            if is_over:
                break

            # 隨便亂下
            posible_actions = current_state.get_posible_actions()
            action = Node.get_random_action(posible_actions)
            current_state = current_state.get_next_state(action)
        # 回傳贏家
        return winner

    # 已探索完成
    def is_full_expand(self):
        return len(self.untried_actions) == 0

    # 向上更新節點權重用
    def is_root_node(self):
        return self.parent


# 操作樹的主要結構
class MCTS:

    def __init__(self):
        self.root = None
        self.current_node = None

    # 進行1000次
    def simulation(self, count=1000):

        for _ in range(count):
            leaf_node = self.simulation_policy()
            winner = leaf_node.rollout()
            leaf_node.update(winner)

    # 模擬時，實際的運作流程
    def simulation_policy(self):

        current_node = self.current_node
        while True:
            is_over, _ = current_node.state.get_state_result()
            if is_over:
                break
            if current_node.is_full_expand():
                _, current_node = current_node.select()
            else:
                return current_node.expand()
        leaf_node = current_node
        return leaf_node

    # 啟動思考，回傳走步
    def take_action(self, current_state):
        # 建立第一個節點
        if not self.root:
            self.root = Node(current_state, None)
            self.current_node = self.root
        else:
            for child_node in self.current_node.children.values():
                if child_node.state == current_state:
                    self.current_node = child_node
                else:
                    self.current_node = self.root
        # 進行模擬
        self.simulation(200)
        action, next_node = self.current_node.select(0.0)
        self.current_node = next_node
        return action
