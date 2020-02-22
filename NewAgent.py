
from model import *
from utils import *
from difficultyEvaluation import *
import numpy as np
class PlayerD(Player):
    def __init__(self, _id):
        super().__init__(_id)
        self.round = 0
        self.factory_tile_number = 0


    def SelectMove(self, moves, game_state):
        # Select move that involves placing the most number of tiles
        # in a pattern line. Tie break on number placed in floor line.
        tiles = 0
        for factory in game_state.factories:
            tiles += factory.total

        if tiles > self.factory_tile_number:
            self.round += 1

        self.factory_tile_number = tiles
        player_state = game_state.players[self.id]
        #mid:from center or factory
        #fid: factory id
        #tgrab: tileGrab
        values = []
        for move in moves:
            values.append(self.EvaluateMove(move, player_state, game_state))

        max_value = max(values)
        best_move = moves[values.index(max_value)]
        # print(moves)
        #
        # print(best_move)
        # print(max_value)

        return best_move
    def EvaluateMove(self, move, player_state, game_state):

        grid_state = player_state.grid_state.tolist()
        grid_scheme = player_state.grid_scheme.tolist()

        mid, fid, tgrab = move

        tile_type = tgrab.tile_type
        number_line = tgrab.num_to_pattern_line
        num_floor = tgrab.num_to_floor_line
        row = tgrab.pattern_line_dest

        column = grid_scheme[row].index((tile_type))


        penalty = 0

        if 0 in player_state.floor:
            floor_index = player_state.floor.index(0)
            floor_scores = player_state.FLOOR_SCORES

            if floor_index < 6:

                for i in range(num_floor):
                    if floor_index + i <= 6:
                        penalty += floor_scores[floor_index + i]



        if number_line > 0:

            for i in range(len(grid_state)):
                if player_state.lines_number[i] != i + 1:
                    if player_state.lines_tile[i] != -1:

                        grid_state[i][grid_scheme[i].index(player_state.lines_tile[i])] = 0


            grid_state[row][column] = 1
            row_im, row_fu, column_im, column_fu = self.countReward(player_state.grid_state, row, column)
            # print("here")
            # print(row_fu)
            # print((number_line / (row + 1 - player_state.lines_number[row])))
            # print(row_fu)
            # print(column_im)
            # print(column_fu)


            row_num, column_num, color_num = self.countNumber(grid_state, grid_scheme, row, column, tile_type)

            row_im *= (number_line + player_state.lines_number[row]/ (row + 1))
            row_fu *= (number_line/( (row + 1) * 5 - row_num - player_state.lines_number[row]) ) * 2


            for i in range(len(player_state.lines_tile)):
                if player_state.lines_tile[i] != -1 and i != row:

                    if grid_scheme[i].index(player_state.lines_tile[i]) == column and player_state.lines_number[i] != i + 1:
                        column_num += player_state.lines_number[i]
            #             print("hahahah")
            #             print(i)
            #             print(player_state.lines_tile[i])
            #             print( player_state.lines_number[i])
            #
            # print(grid_state)
            # print(grid_scheme)
            # print(tile_type)
            # print(row)
            # print(column)
            # print(player_state.lines_number[row])
            # print(number_line)
            # print(column_num)
            column_im *= (number_line + player_state.lines_number[row] / (row + 1))
            column_fu *= (number_line/ (15 - column_num - player_state.lines_number[row])) * 7

            # for i in range(len(player_state.lines_tile)):
            #     if player_state.lines_tile[i] == tile_type and i != row and player_state.lines_number[i] != i + 1:
            #         color_num += player_state.lines_number[i]

            color_fu = (number_line + player_state.lines_number[row]/ (15 - color_num)) * 10
            # print(row_im)
            # print(row_fu)
            # print(column_im)
            # print(column_fu)


            total_reward = row_im + row_fu + column_im + column_fu + color_fu



            if ((number_line / (row + 1 - player_state.lines_number[row])) != 1):
                total_reward *= 0.2



            # print(total_reward)
            #
            # if (game_state.first_player_taken == False) and mid == Move.TAKE_FROM_CENTRE:
            #     total_reward -= 1
        else:
            total_reward = 0
        # print(move)
        # print(total_reward + penalty)
        return total_reward + penalty


    def countNumber(self, grid_state, grid_scheme, row, column, tile_type):
        row_num = 0
        for i in range(len(grid_state[row])):
            if grid_state[row][i] == 1:
                if i != column:
                    row_num += (row + 1)

        column_num = 0
        for i in range(len(grid_state)):
            if grid_state[i][column] == 1:
                if i != row:
                    column_num += (i + 1)
                    # print(column_num)

        color_num = 0
        for i in range(len(grid_state)):
            if grid_state[i][grid_scheme[i].index(tile_type)] == 1:
                if i != row:
                    color_num += (i + 1)

        return row_num, column_num, color_num




    def countReward(self, grid_state, row, column):

        have = []

        for i in range(len(grid_state[row])):
            if grid_state[row][i] == 1:
                have.append(i)

        row_im, row_fu = self.countSerial(have, column)

        have = []
        for i in range(len(grid_state)):
            if grid_state[i][column] == 1:
                have.append(i)

        column_im, column_fu = self.countSerial(have, row)

        return row_im, row_fu, column_im, column_fu

    def countSerial(self, have, flag):
        serial_before = 0
        serial_after = 0

        for i in range(len(have) - 1):
            if have[i] < flag:

                if have[i + 1] == (have[i] + 1):
                    serial_before += 1
                else:
                    serial_before = 0
            if have[i] >= flag:

                if have[i + 1] == (have[i] + 1):
                    serial_after += 1
                else:
                    break

        immediate_reward = serial_before + serial_after + 1
        future_reward = len(have)

        return immediate_reward, future_reward

