from MCTS import MCTS
import numpy as np
from Shared.Consts import BLACK, WHITE
from Shared.Functions import xy_to_index
from GoGame.GoSimulator import GoSimulator
import random
import time


def addBoardtoBoards(board,boards,turn_counter):
    m = boards.shape[1]
    board_temp = np.reshape(board,-1)
    boards_temp = np.reshape(boards,-1)
    new_boards_temp = np.append(boards,board)
    new_boards = np.reshape(new_boards_temp, [turn_counter,m,m])
    return new_boards

class Selfplay:
    def __init__(self, model, player, n=5, start_boards=None):
        self.model = model
        self.game = GoSimulator(n)
        self.player = player
        self.n = n

    def playGame(self):
        n = self.n
        game = self.game
        player = self.player
        boards = np.zeros([2,n,n])

        game.set_board_from_prev_boards(boards, player)
        print(game.board)

        print('------------- START -------------\n')

        turn_counter = 2
        check_pass = 0
        mcts = MCTS(self.model, player, start_boards=boards)

        ### --- Start game --- ###

        while True:
            pi = mcts.search_for_pi(iterations=20)
            # print(pi)

            # Find position of next play that maximises pi
            arg_pi_max = (np.argwhere(pi==np.max(pi)))
            arg_pi_max = arg_pi_max.flatten()

            arg_max = random.choice(arg_pi_max) # to deal with multiple maximums
            # print('arg_max ',arg_max)

            if arg_max == 25: # PASS
                print(player, ' PASSES \n')
                board, next_player = game.pass_move()
                check_pass = check_pass + 1

            else:
                move_y, move_x = divmod(arg_max, 5) # finds position of move on board and makes play
                print('Best move x:', move_x)
                print('Best move y:', move_y,'\n')
                # Plays the best move
                print(player, ' MOVES \n')
                board, next_player = game.play(move_x,move_y)
                check_pass = 0

            mcts.set_move(arg_max)
            turn_counter = turn_counter + 1

            # Add board to boards
            boards = addBoardtoBoards(board,boards,turn_counter)
            player = next_player

            game.set_board_from_prev_boards(boards, player)
            print(game.board)
            print('---------------------------------\n')
            black_lead = game.black_score_lead()

            # Check win condition
            if check_pass >=2:
                print('GAME OVER FROM 2 PASSES')
                break 

            if turn_counter == 5 * 5 * 2:
                print('GAME OVER FROM TURN LIMIT REACHED')
                break

            # time.sleep(0.001)
        print(player, ' WINS!')
        black_lead = game.black_score_lead()
        return black_lead, boards