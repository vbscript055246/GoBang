
import os
from copy import deepcopy
from time import sleep

import keyboard

SIZE = 15


class Human:
    def __init__(self, table):
        self.table = deepcopy(table)
        self.x = 7
        self.y = 7

    # 印出目前的落子點
    def show(self):
        table = deepcopy(self.table)
        table[self.y][self.x] = '⭗'
        for i in range(SIZE):
            print(''.join(table[i]))

    # 選擇落子點介面
    def select(self):
        self.show()
        while 1:
            sleep(0.1)
            flag = 0
            if keyboard.is_pressed('up'):
                self.y -= 1
                flag = 1
            elif keyboard.is_pressed('down'):
                self.y += 1
                flag = 1
            elif keyboard.is_pressed('left'):
                self.x -= 1
                flag = 1
            elif keyboard.is_pressed('right'):
                self.x += 1
                flag = 1
            elif keyboard.is_pressed('space'):
                os.system("cls")
                break
            if flag:
                self.y = max(self.y, 0)
                self.y = min(self.y, SIZE - 1)
                self.x = max(self.x, 0)
                self.x = min(self.x, SIZE - 1)
                os.system("cls")
                print()
                self.show()


        return f'{self.x},{self.y}'
