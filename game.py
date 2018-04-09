import pygame
import pygame.font
from _2048_ import Game
from math import log2

help = False
window = pygame.display.set_mode((630, 730))
pygame.display.set_caption('2048')
pygame.mouse.set_visible(True)
pygame.font.init()
font = pygame.font.SysFont('Consolas', 48)
osd = pygame.font.SysFont('Consolas', 32)
clock = pygame.time.Clock()
_break = False
colors = [(45, 15, 65), (61, 20, 89), (77, 26, 112), (94, 31, 136), (116, 39, 150), (151, 52, 144), (184, 66, 140), (219, 80, 135), (233, 106, 141), (238, 139, 151), (243, 172, 162), (249, 205, 172)]
off = 20

help_strings = ('W: UP', 'S: DOWN', 'A: LEFT', 'D: RIGHT', 'R: UNDO', 'N: NEW GAME', 'X: QUIT', 'H: HELP')
help_osd = []
hsw, hsh = 0, 0
for s in help_strings:
    surf = osd.render(s, True, (255, 255, 255))
    w = surf.get_width()
    hsw = w if w > hsw else hsw
    hsh += surf.get_height()
    help_osd.append(surf)
help_surf = pygame.Surface((hsw+2*off, hsh+2*off))
help_surf.fill((255, 0, 128))
for c, s in enumerate(help_osd):
    help_surf.blit(s, (off, off + c*34))

go = font.render('GAME OVER', True, (255, 255, 255))
game_over_surf = pygame.Surface((go.get_width()+20, 60))
game_over_surf.fill((255, 64, 64))
game_over_surf.blit(go, (10, 8))

yw = font.render('YOU WON!!!', True, (255, 255, 255))
won_surf = pygame.Surface((yw.get_width()+20, 60))
won_surf.fill((255, 128, 0))
won_surf.blit(yw, (10, 8))

game = Game()

while not _break:
    
    for event in pygame.event.get():
       
        if event.type == pygame.QUIT:
            _break = False
        elif event.type == pygame.KEYDOWN:

            # print(event)

            if event.key == 120: # x
                _break = True
                try:
                    with open('2048.hs', 'w') as f:
                        f.write(f'{game.high_score};{game.high_score_moves}')
                except Exception as ex:
                    pass

            if event.key == 110: # n
                game.restart()
            if event.key == 104: # h
                    help = not help
            if event.key == 116: # 
                    game.test()

            if not game.game_over and not game.won:
                
                if event.key == 97: # a
                    game.left()
                if event.key == 100: # d
                    game.right()
                if event.key == 119: # w
                    game.up()
                if event.key == 115: # s
                    game.down()
                if event.key == 114: # r undo
                    if not game.undo: game.do_undo()

    window.fill((0, 0, 0))

    for i in range(16):

        row, col = i//4, i%4
        x, y = col*150, row*150
        el = game.board.board[i]
        
        cl = 0 if el == 0 else int(log2(el))

        bcl = colors[cl]
        if game.g:
            if row == game.g[0] and col == game.g[1] and el > 0:
                bcl = (255, 255, 255)
        pygame.draw.rect(window, bcl, (x+off, y+off, 135, 135), 0)

        if el > 0:
            tcl = colors[cl] if game.g and row == game.g[0] and col == game.g[1] else (255, 255, 255)
            # tcol = (255, 255, 0) if (game.g and row == game.g[0] and col == game.g[1]) else (255, 255, 255)
            num = font.render(str(el) , True, tcl)
            w, h = num.get_width()//2, num.get_height()//2
            window.blit(num, (x+off+67-w, y+off+67-h))

    window.blit(osd.render(f'HIGH SCORE: {game.high_score} ({game.high_score_moves})', True, (255, 255, 255)), (20, 620))
    window.blit(osd.render(f'SCORE: {game.score}', True, (255, 255, 255)), (20, 650))
    window.blit(osd.render(f'MOVES: {game.moves}', True, (255, 255, 255)), (20, 680))
    if help:
        window.blit(help_surf, (190, 120))
    if game.game_over:
        window.blit(game_over_surf, (315-game_over_surf.get_width()//2, 280))
    if game.won:
        window.blit(won_surf, (315-game_over_surf.get_width()//2, 280))

    pygame.display.update()
    clock.tick(15)
