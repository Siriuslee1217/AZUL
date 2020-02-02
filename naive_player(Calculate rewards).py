# Written by Michelle Blom, 2019
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
from model import *
from utils import *

class NaivePlayer(Player):
    def __init__(self, _id):
        super().__init__(_id)

    def SelectMove(self, moves, game_state):
        # Select move that involves placing the most number of tiles
        # in a pattern line. Tie break on number placed in floor line.
        most_to_line = -1
        corr_to_floor = 0

        best_move = None

        for mid,fid,tgrab in moves:
            print("----------")
            print(mid)
            print("fid: ",fid)
            print("tgrab:")
            print(tgrab.tile_type)
            print(tgrab.number)
            print(tgrab.pattern_line_dest)
            print(tgrab.num_to_pattern_line)
            print(tgrab.num_to_floor_line)
            print("----------")

            if most_to_line == -1:
                best_move = (mid,fid,tgrab)
                most_to_line = tgrab.num_to_pattern_line
                corr_to_floor = tgrab.num_to_floor_line
                continue

            if tgrab.num_to_pattern_line > most_to_line:
                best_move = (mid,fid,tgrab)
                most_to_line = tgrab.num_to_pattern_line
                corr_to_floor = tgrab.num_to_floor_line
            elif tgrab.num_to_pattern_line == most_to_line and \
                tgrab.num_to_pattern_line < corr_to_floor:
                best_move = (mid,fid,tgrab)
                most_to_line = tgrab.num_to_pattern_line
                corr_to_floor = tgrab.num_to_floor_line

        for ply in game_state.players:
            self.requirementAnalysis(ply)

        return best_move


    def requirementAnalysis(self, player):

        grid_reward = numpy.zeros((5, 5))
        grid_future = numpy.zeros((5, 5))

        print("----------")
        print("Evaluating")
        for i in range(0, 5):
            if player.lines_tile[i] != -1:
                for j in range(0, 5):
                    if j != player.grid_scheme[i][player.lines_tile[i]] or player.lines_number[i] == i+1:
                        grid_reward[i][j] = -1
                        grid_future[i][j] = -1
        for i in range(0, 5):
            for j in range(0, 5):
                if player.grid_state[i][j] == 1:
                    grid_reward[i][j] = -1
                    grid_future[i][j] = -1
        print("could be complete in this round")
        print(grid_reward)

        for i in range(0, 5):
            for j in range(0, 5):
                if grid_reward[i][j] != -1:
                    row =  self.countColumsReward(player, 0, (i, j))
                    colum = self.countRowsReward(player, 0, (i, j))
                    grid_future[i][j] += self.countFutureReward(player, i, j)
                    if row == 1:
                        grid_reward[i][j] += colum
                    elif colum == 1:
                        grid_reward[i][j] += row
                    else:
                        grid_reward[i][j] += colum
                        grid_reward[i][j] += row

        print("immediate reward ")
        print(grid_reward)

        print("future reward")
        print(grid_future)

        print("current situation")
        print(player.lines_tile)
        print(player.lines_number)
        print(player.grid_state)

        print("CountColor")
        print(self.countColors(player))

    def countRowsReward(self, player, direction, node):
        x, y = node
        if direction == 0:
            return 1 + self.countRowsReward(player, 1, (x, y-1)) + self.countRowsReward(player, 2, (x, y+1))
        if y > 4 or y < 0:
            return 0
        if player.grid_state[x][y] == 0:
            return 0
        if direction == 1:
            return 1 + self.countRowsReward(player, 1, (x, y-1))
        if direction == 2:
            return 1 + self.countRowsReward(player, 2, (x, y+1))

    def countColumsReward(self, player, direction, node):
        x, y = node
        if direction == 0:
            return 1 + self.countColumsReward(player, 1, (x-1, y)) + self.countColumsReward(player, 2, (x+1, y))
        if x > 4 or x < 0:
            return 0
        if player.grid_state[x][y] == 0:
            return 0
        if direction == 1:
            return 1 + self.countColumsReward(player, 1, (x-1, y))
        if direction == 2:
            return 1 + self.countColumsReward(player, 2, (x+1, y))

    def countFutureReward(self, player, i, j):
        RowBonus = [0, 0.25, 0.25, 0.5, 1]
        ColumBonus = [0, 1, 1, 2, 3]
        ColorBonus = [0, 1, 2, 2, 5]
        rowCount = self.countRows(player)
        columCount = self.countColums(player)
        colorCount = self.countColors(player)
        return RowBonus[rowCount[i]] + ColumBonus[columCount[j]] + ColorBonus[colorCount[self.whatColor(player, i, j)]]

    def countRows(self, player):
        grid_state = player.grid_state
        line = {}
        for i in range(0, 5):
            count = 0
            for j in range(0, 5):
                if grid_state[i][j] == 1:
                    count += 1
            line[i] = count
        # return sorted(line.items(), key=lambda item:item[1], reverse=True)
        return line

    def countColums(self, player):
        grid_state = player.grid_state
        line = {}
        for i in range(0, 5):
            count = 0
            for j in range(0, 5):
                if grid_state[j][i] == 1:
                    count += 1
            line[i] = count
        # return sorted(line.items(), key=lambda item: item[1], reverse=True)
        return line

    def countColors(self, player):
        grid_state = player.grid_state
        line = {Tile.BLUE: 0, Tile.YELLOW: 0, Tile.RED: 0, Tile.BLACK: 0, Tile.WHITE: 0}
        for i in range(0, 5):
            for j in range(0, 5):
                if grid_state[i][j] == 1:
                    line[self.whatColor(player, i, j)] += 1
        return line

    def whatColor(self,player, i, j):
        if j == player.grid_scheme[i][Tile.BLUE]:
            return Tile.BLUE
        elif j == player.grid_scheme[i][Tile.YELLOW]:
            return Tile.YELLOW
        elif j == player.grid_scheme[i][Tile.RED]:
            return Tile.RED
        elif j == player.grid_scheme[i][Tile.BLACK]:
            return Tile.BLACK
        elif j == player.grid_scheme[i][Tile.WHITE]:
            return Tile.WHITE
