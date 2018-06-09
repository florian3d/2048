'''array manipulation class module'''
import array
from random import randrange

class Board():
        '''array manipulation class'''
        def __init__(self, cols=4, rows=4):
            '''object creation'''
            self.cols = cols
            self.rows = rows
            self.board = array.array('I', [0 for i in range(self.cols*self.rows)])   

        def get_val(self, row, col):
            '''returns value'''
            return self.board[row*self.rows+col]


        def set_val(self, row, col, val):
            '''sets value'''
            self.board[row*self.rows+col] = val


        def get_col(self, col):
            '''return column'''
            return array.array('I', self.board[col::self.cols])


        def get_row(self, row):
            '''return row'''
            s = row * self.rows
            return array.array('I', self.board[s:(s+self.cols)])


        def set_col(self, col, values):
            '''sets column'''
            for idx, val in enumerate(values):
                self.board[col+idx*self.cols] = val


        def clone(self, board):
            '''clone the array'''
            for idx, val in enumerate(board.board):
                self.board[idx] = val


        def is_full(self):
            '''return True if array is full (not contains 0 values)'''
            return 0 not in self.board


        def are_equal(self, board):
            '''checks if two arrays are equal'''
            equal = True
            for idx, val in enumerate(board.board):
                if val != self.board[idx]:
                    equal = False
            return equal

        
        def get_zero_random_pos(self):
            '''return random position with zero value'''
            z = [i for i,x in enumerate(self.board) if x==0]
            p = z[randrange(0, len(z))]
            return p//self.cols, p%self.cols

        
        def test(self):
            '''test will be removed in the future'''
            self.board = array.array('I', [8, 4, 16, 32, 64, 128, 256, 512, 32, 16, 8, 4, 512, 0, 0, 0])