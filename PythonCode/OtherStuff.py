__version__ = '0.1.0'

import Config as cfg
import random
import math
from Gameplay import *
from ScaraDriver import *

GAMETYPES = ['standard', 'meme']

def standard_game(scarabot, cam, bot_first: bool):
    scarabot.draw_board()
    game = TacBoard()
    turn = 0 if bot_first else 1

    while True:
        if turn == 0:
            # Pick random corner for first move
            first_move = Move(xindex=random.randint(0,1)*2, yindex=random.randint(0,1)*2)
            game.bot_move(first_move)
            scarabot.draw_move(first_move)
        elif turn % 2 == 0:
            # Bot turn
            scarabot.unpark()
            bot_best_move = game.get_best_move()
            if cfg.DEBUG_MODE:
                print('bot move:', bot_best_move.x, bot_best_move.y)
            game.bot_move(bot_best_move)
            scarabot.draw_move(bot_best_move)
        else:
            # Player turn
            scarabot.park()
            bot_win_possible = game.is_bot_win_possible()
            cam.locate_user_move_prep()
            if bot_win_possible is False:
                swat(cam, scarabot, n=2)
                break
            _ = input('Press enter after moved. TODO auto detect this or something idk...')
            user_move_index = cam.locate_user_move(game.get_free_space_vector())
            if cfg.DEBUG_MODE:
                print('user_move_index:', user_move_index)
            game.user_move(user_move_index)

        if game.win_check() == 1:
            scarabot.draw_win_line(game)
            return
        elif game.win_check() == 2:
            # Tie, should be impossible
            return
        elif game.win_check() == -1:
            # This should also be impossible but idk..
            return

        if cfg.DEBUG_MODE:
            print('Turn:', turn)

        turn += 1


def meme_game(scarabot, cam, bot_first: bool):
    draw_board()

def swat(cam, bot, n=1):
    """ Swat away user hand when seen n times """
    timeout_s = 60
    swats = 0
    t_start = time.time()
    while time.time() < t_start + timeout_s:
        if cam.identify_motion():
            bot.absolute_move(-20,40,300)
            bot.absolute_move(120,40,300)
            bot.absolute_move(-20,40,300)
            bot.park()
            swats += 1

        if swats >= n:
            return
