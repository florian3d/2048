'''2048 game clone'''
from _2048_ import Game
from math import log2
import pygame
import pygame.font

help = False
w_width, w_height = 630, 730
window = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption('2048')
pygame.mouse.set_visible(True)
pygame.font.init()
game_font = pygame.font.SysFont('Consolas', 48)
osd_font = pygame.font.SysFont('Consolas', 32)
clock = pygame.time.Clock()
_break_ = False
colors = [(45, 15, 65), (61, 20, 89), (77, 26, 112), (94, 31, 136), (116, 39, 150), (151, 52, 144), (184, 66, 140), (219, 80, 135), (233, 106, 141), (238, 139, 151), (243, 172, 162), (249, 205, 172)]
col_white = (255, 255, 255)
offset = 20

help_strings = ('W: UP', 'S: DOWN', 'A: LEFT', 'D: RIGHT', 'R: UNDO', 'N: NEW GAME', 'X: QUIT', 'H: HELP')
help_osd = []
hsw, hsh = 0, 0
for s in help_strings:
    surf = osd_font.render(s, True, (255, 255, 255))
    w = surf.get_width()
    hsw = w if w > hsw else hsw
    hsh += surf.get_height()
    help_osd.append(surf)
help_surf = pygame.Surface((hsw+2*offset, hsh+2*offset))
help_surf.fill((255, 0, 128))
for c, s in enumerate(help_osd):
    help_surf.blit(s, (offset, offset + c*34))

go = game_font.render('GAME OVER', True, (255, 255, 255))
game_over_surf = pygame.Surface((go.get_width()+20, 60))
game_over_surf.fill((255, 64, 64))
game_over_surf.blit(go, (10, 8))

yw = game_font.render('YOU WON!!!', True, (255, 255, 255))
won_surf = pygame.Surface((yw.get_width()+20, 60))
won_surf.fill((255, 128, 0))
won_surf.blit(yw, (10, 8))

game = Game()

while not _break_:
    
    for event in pygame.event.get():
       
        if event.type == pygame.QUIT:
            _break_ = False
        elif event.type == pygame.KEYDOWN:

            # print(event)

            if event.key == pygame.K_x: # x
                _break_ = True
                try:
                    with open('2048.hs', 'w') as f:
                        f.write(f'{game.high_score};{game.high_score_moves}')
                except Exception as ex:
                    pass

            if event.key == pygame.K_n: # RESTART
                game.restart()
            if event.key == pygame.K_h: # HELP
                    help = not help

            if not game.game_over and not game.won:
                
                if event.key == pygame.K_a: # LEFT
                    game.left()
                if event.key == pygame.K_d: # RIGHT
                    game.right()
                if event.key == pygame.K_w: # UP
                    game.up()
                if event.key == pygame.K_s: # DOWN
                    game.down()
                if event.key == pygame.K_r: # UNDO
                    if not game.undo:
                        game.do_undo()

    window.fill((0, 0, 0))

    for i in range(16):

        row, col = i//4, i%4
        x, y = col*150, row*150
        el = game.board.board[i]
        
        cl = 0 if el == 0 else int(log2(el))

        bcl = colors[cl]
        if game.last_gen:
            if row == game.last_gen[0] and col == game.last_gen[1] and el > 0:
                bcl = col_white
        pygame.draw.rect(window, bcl, (x+offset, y+offset, 135, 135), 0)

        if el > 0:
            tcl = colors[cl] if game.last_gen and row == game.last_gen[0] and col == game.last_gen[1] else col_white
            num = game_font.render(str(el) , True, tcl)
            w, h = num.get_width()//2, num.get_height()//2
            window.blit(num, (x+offset+67-w, y+offset+67-h))

    window.blit(osd_font.render(f'HIGH SCORE: {game.high_score} ({game.high_score_moves})', True, col_white), (offset, 620))
    window.blit(osd_font.render(f'SCORE: {game.score}', True, col_white), (offset, 650))
    window.blit(osd_font.render(f'MOVES: {game.moves}', True, col_white), (offset, 680))
    if help:
        window.blit(help_surf, (190, 120))
    if game.game_over:
        window.blit(game_over_surf, (315-game_over_surf.get_width()//2, 280))
    if game.won:
        window.blit(won_surf, (315-game_over_surf.get_width()//2, 280))

    pygame.display.update()
    clock.tick(15) # frames per seconds
