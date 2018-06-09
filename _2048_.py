
'''2048 game module'''
from random import random
from _board_ import Board

class Game():
    '''2048 game class'''
    def __init__(self):
        '''game object creation'''
        self.high_score = 0
        self.high_score_moves = 0
        self.act = 0
        self.bck = 1
        self.board = None
        self.game_over = False
        self.won = False
        self.last_gen = None
        self.undo = True
        self.game_init()
        try:
            with open('2048.hs', 'r') as f:
                data = f.read()
                if data:
                    h_s, hs_ms = data.split(';')
                    self.high_score, self.high_score_moves = int(h_s), int(hs_ms)
        except IOError:
            pass

    def game_init(self):
        '''game init'''
        self.score = 0
        self.moves = 0
        self.boards = (Board(), Board())
        self.act = 0
        self.bck = 1
        self.board = self.boards[self.act]
        self.undo = False
        self.last_gen = None
        self.game_over = False
        self.won = False
        self.history = []
        self.history.append(('INIT', self.gen(2)))
        self.history.append(('INIT', self.gen(2)))
        self.boards[self.bck].clone(self.board)

    def switch_boards(self):
        '''switch boards'''
        self.act, self.bck = self.bck, self.act
        self.board = self.boards[self.act]

    def do_undo(self):
        '''just undo'''
        self.undo = True
        self.switch_boards()


    def move(self, tmp, score, concat):
        '''internal function called after move'''
        self.last_gen = None
        self.score += score
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_moves = self.moves
        self.boards[self.bck].clone(tmp)
        self.switch_boards()
        self.moves += 1
        if score == 2048:
            self.won = True
        if not concat:
            self.gen()
        self.undo = False
        if self.board.is_full():
            self.is_game_over()
        

    def gen(self, val=0):
        '''generates random value'''
        if not self.boards[self.act].is_full():
            row, col = self.board.get_zero_random_pos()
            if not val:
                val = 2 if random() > .1 else 4
            self.boards[self.act].set_val(row, col, val)
            self.last_gen = (row, col, val)


    def is_game_over(self):
        '''check if there are no movement'''
        game_over = True

        for row in range(3):
            for col in range(3):
                val0 = self.board.get_val(row, col)
                val_r = self.board.get_val(row, col+1)
                val_d = self.board.get_val(row+1, col)

                if val0 == val_r or val0 == val_d:
                    game_over = False

            if self.board.get_val(3, row) == self.board.get_val(3, row+1) or self.board.get_val(row, 3) == self.board.get_val(row+1, 3):
                game_over = False
        
        self.game_over = game_over

    def restart(self):
        '''create new game'''
        self.game_init()


    def up(self):
        '''move up'''
        tmp = Board()
        score = 0
        concat = False
        for col in range(4):

            nums = [x for x in self.boards[self.act].get_col(col) if x > 0]
            result = []
            ix = 0
            v2 = 0
            l = len(nums)
            while ix < l:
                v1 = nums[ix]
                if ix == l-1:
                    result.append(v1)
                    ix += 1
                else:
                    v2 = nums[ix+1]
                    if v1 == v2:
                        result.append(v1*2)
                        score += v1*2
                        ix += 2
                        concat = True
                    else:
                        result.append(v1)
                        ix += 1

            for c, n in enumerate(result):
                tmp.set_val(c, col, n)

        if not tmp.are_equal(self.board):
            self.move(tmp, score, concat)

    def down(self):
        '''move down'''
        tmp = Board()
        score =  0
        concat = False
        for col in range(4):

            nums = [x for x in self.boards[self.act].get_col(col) if x > 0]
            result = []
            ix = len(nums) - 1
            v2 = 0
            while ix >= 0:
                v1 = nums[ix]
                if ix == 0:
                    result.append(v1)
                    ix -= 1
                else:
                    v2 = nums[ix-1]
                    if v1 == v2:
                        result.append(v1*2)
                        score += v1*2
                        concat = True
                        ix -= 2
                    else:
                        result.append(v1)
                        ix -= 1
            
            for c, n in enumerate(result):
                tmp.set_val(3-c, col, n)

        if not tmp.are_equal(self.board):
            self.move(tmp, score, concat)


    def left(self):
        '''move left'''
        tmp = Board()
        score = 0
        concat = False
        for row in range(4):
            nums = [x for x in self.boards[self.act].get_row(row) if x > 0]
            result = []
            ix = 0
            v2 = 0
            l = len(nums)
            while ix < l:
                v1 = nums[ix]
                if ix == l-1:
                    result.append(v1)
                    ix += 1
                else:
                    v2 = nums[ix+1]
                    if v1 == v2:
                        result.append(v1*2)
                        score += v1*2
                        ix += 2
                        concat = True
                    else:
                        result.append(v1)
                        ix += 1
            
            for c, n in enumerate(result):
                tmp.set_val(row, c, n)

        if not tmp.are_equal(self.board):
            self.move(tmp, score, concat)


    def right(self):
        '''move right'''
        tmp = Board()
        score = 0
        concat = False
        for row in range(4):
            nums = [x for x in self.boards[self.act].get_row(row) if x > 0]
            result = []
            ix = len(nums) - 1
            v2 = 0
            while ix >= 0:
                v1 = nums[ix]
                if ix == 0:
                    result.append(v1)
                    ix -= 1
                else:
                    v2 = nums[ix-1]
                    if v1 == v2:
                        result.append(v1*2)
                        score += v1*2
                        ix -= 2
                        concat = True
                    else:
                        result.append(v1)
                        ix -= 1
            
            for c, n in enumerate(result):
                tmp.set_val(row, 3-c, n)

        if not tmp.are_equal(self.board):
            self.move(tmp, score, concat)

    def test(self):
        '''test'''
        self.board.test()
