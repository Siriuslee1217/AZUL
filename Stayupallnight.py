
from model import *
from utils import *
from difficultyEvaluation import *
import numpy as np
class PlayerL(Player):
    def __init__(self, _id):
        super().__init__(_id)
        self.round = 0
        self.factory_tile_number = 0
        self.count = 0
        self.returns = 0


    def SelectMove(self, moves, game_state):
        # Select move that involves placing the most number of tiles
        # in a pattern line. Tie break on number placed in floor line.

        scores, number = self.Simulate(game_state)

        best_move = moves[number]

        return best_move

    def Simulate(self, game_state):

        simulate_state = copy.deepcopy(game_state)

        player_num = len(game_state.players)

        my_player_state = copy.deepcopy(simulate_state.players[self.id])

        if not simulate_state.TilesRemaining():
            score, used = self.ScoreRound(simulate_state)

            self.returns += 1
            # print("returns:")
            # print(self.returns
            score += self.WholeFuture(simulate_state)
            score += self.NumOnLines(simulate_state)
            return score, 0

        available_moves = my_player_state.GetAvailableMoves(simulate_state)

        values = self.MoveToValue(available_moves, simulate_state, self.id)
        v = copy.deepcopy(values)
        v.sort(reverse=True)
        # print(v)
        scores = {}
        self.best_move_here = None
        self.max = -100
        for i in range(len(values)):

            if (len(values) >= 3 and values[i] >= v[2]) or len(values) < 3:

                gs = copy.deepcopy(simulate_state)
                gs.ExecuteMove(self.id, available_moves[i])

                for j in range(player_num - 1):
                    player_id = (self.id + j + 1) % player_num
                    if gs.TilesRemaining():
                        available_moves_others = gs.players[player_id].GetAvailableMoves(gs)

                        gs.ExecuteMove(player_id, self.BestMove(available_moves_others, gs, player_id))
                    else:
                        score, used = self.ScoreRound(gs)
                        score += self.WholeFuture(gs)
                        score += self.NumOnLines(gs)
                        return score, 0

                scores[i] = self.Simulate(gs)[0]
                if scores[i] >= self.max:
                    self.max = scores[i]
                    self.best_move_here = i


        # if scores.__len__() == 0:
        #     self.returns += 1
        #     num = values.index(max(values))
        #     self.best_move_here = num
        #     gs = copy.deepcopy(simulate_state)
        #     gs.ExecuteMove(self.id, available_moves[num])
        #     print("qqqqqqqqqqq")
        #     return self.Simulate(gs)

        # self.returns += 1
        # print("returns2:")
        # print(self.returns)
        # print(scores)

        return scores[self.best_move_here], self.best_move_here


    def MoveToValue(self, moves, game_state, id):
        values = []
        for move in moves:
            gs = copy.deepcopy(game_state)
            values.append(self.EvaluateMove(move, gs, id))

        return values

    def BestMove(self, moves, game_state, id):
        values = self.MoveToValue(moves, game_state, id)

        max_value = max(values)
        best_move = moves[values.index(max_value)]

        return best_move

    def EvaluateMove(self, move, game_state, id):

        player_state = copy.deepcopy(game_state.players[id])
        grid_state = copy.deepcopy(player_state.grid_state).tolist()
        grid_scheme = copy.deepcopy(player_state.grid_scheme).tolist()

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

            row_im *= (number_line / (row + 1 - player_state.lines_number[row]))
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
            column_im *= (number_line / (row + 1 - player_state.lines_number[row]))
            column_fu *= (number_line/ (15 - column_num - player_state.lines_number[row])) * 7

            # for i in range(len(player_state.lines_tile)):
            #     if player_state.lines_tile[i] == tile_type and i != row and player_state.lines_number[i] != i + 1:
            #         color_num += player_state.lines_number[i]

            color_fu = (number_line/ (15 - color_num - player_state.lines_number[row])) * 10
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

    def WholeFuture(self, game_state):
        player_state = copy.deepcopy(game_state.players[self.id])
        grid_state = copy.deepcopy(player_state.grid_state).tolist()
        grid_scheme = copy.deepcopy(player_state.grid_scheme).tolist()

        for i in range(len(grid_state)):
            if player_state.lines_number[i] != i + 1:
                if player_state.lines_tile[i] != -1:
                    grid_state[i][grid_scheme[i].index(player_state.lines_tile[i])] = 0

        row = {}
        column = {}
        color = {}

        for i in range(grid_state.__len__()):
            row[i] = 0
            column[i] = 0
            color[i] = 0
            for j in range(grid_state[0].__len__()):
                row[i] += grid_state[i][j]
                column[i] += grid_state[j][i]
                color[i] += grid_state[j][(i + j) % 5]

            row[i] /= 5
            row[i] *= 2

            column[i] /= 5
            column[i] *= 7/3


            color[i] /= 5
            color[i] *= 10/4

        sum = 0
        for i in range(grid_state.__len__()):
            sum += row[i]
            sum += column[i]
            sum += color[i]

        return sum

    def LinesNotFull(self, game_state):
        player_state = game_state.players[self.id]

        lines_not_full = 0
        for row in range(5):
            if player_state.lines_number[row] != 0:
                if player_state.lines_number[row] != row + 1:
                    lines_not_full += (row + 1 - player_state.lines_number[row])/ (row + 1)

        return  lines_not_full

    def NumOnLines(self, game_state):
        player_state = game_state.players[self.id]

        num_on_lines = 0
        for row in range(5):
                if player_state.lines_number[row] != row + 1:
                    num_on_lines += player_state.lines_number[row]/ (row+1)

        return num_on_lines

    def ScoreRound(self, game_state):
        player_state = game_state.players[self.id]

        used_tiles = []

        score_inc = 0

        # 1. Move tiles across from pattern lines to the wall grid
        for i in range(player_state.GRID_SIZE):
            # Is the pattern line full? If not it persists in its current
            # state into the next round.
            if player_state.lines_number[i] == i + 1:
                tc = player_state.lines_tile[i]
                col = int(player_state.grid_scheme[i][tc])

                # Record that the player has placed a tile of type 'tc'
                player_state.number_of[tc] += 1

                # Clear the pattern line, add all but one tile into the
                # used tiles bag. The last tile will be placed on the
                # players wall grid.
                for j in range(i):
                    used_tiles.append(tc)

                player_state.lines_tile[i] = -1
                player_state.lines_number[i] = 0

                # Tile will be placed at position (i,col) in grid
                player_state.grid_state[i][col] = 1

                # count the number of tiles in a continguous line
                # above, below, to the left and right of the placed tile.
                above = 0
                for j in range(col - 1, -1, -1):
                    val = player_state.grid_state[i][j]
                    above += val
                    if val == 0:
                        break
                below = 0
                for j in range(col + 1, player_state.GRID_SIZE, 1):
                    val = player_state.grid_state[i][j]
                    below += val
                    if val == 0:
                        break
                left = 0
                for j in range(i - 1, -1, -1):
                    val = player_state.grid_state[j][col]
                    left += val
                    if val == 0:
                        break
                right = 0
                for j in range(i + 1, player_state.GRID_SIZE, 1):
                    val = player_state.grid_state[j][col]
                    right += val
                    if val == 0:
                        break

                # If the tile sits in a contiguous vertical line of
                # tiles in the grid, it is worth 1*the number of tiles
                # in this line (including itself).
                if above > 0 or below > 0:
                    score_inc += (1 + above + below)

                # In addition to the vertical score, the tile is worth
                # an additional H points where H is the length of the
                # horizontal contiguous line in which it sits.
                if left > 0 or right > 0:
                    score_inc += (1 + left + right)

                # If the tile is not next to any already placed tiles
                # on the grid, it is worth 1 point.
                if above == 0 and below == 0 and left == 0 \
                        and right == 0:
                    score_inc += 1

        # Score penalties for tiles in floor line
        penalties = 0
        for i in range(len(player_state.floor)):
            penalties += player_state.floor[i] * player_state.FLOOR_SCORES[i]
            player_state.floor[i] = 0

        used_tiles.extend(player_state.floor_tiles)
        player_state.floor_tiles = []

        # Players cannot be assigned a negative score in any round.
        score_change = score_inc + penalties

        player_state.score += score_change
        player_state.player_trace.round_scores[-1] = score_change

        return (player_state.score, used_tiles)
    # immediate reward有计算问题！！
# 用execute配合scoreround更好
