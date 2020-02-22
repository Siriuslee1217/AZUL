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

class MctsPlayer(Player):
    def __init__(self, _id):
        super().__init__(_id)
        self.round = 0
        # self.file = open("records test final.txt", "a", encoding="utf-8")
        self.factory_tile_number = 0

    def SelectMove(self, moves, game_state):
        myPlayer = game_state.players[self.id]
        floorConditioin = myPlayer.floor
        floorNum = 0
        grid_reward = self.requirementAnalysis(myPlayer)
        moves_list = {}

        for i in floorConditioin:
            if i == 1:
                floorNum += 1

        for aMove in moves:
            reward = self.moveEvaluation(aMove, myPlayer, grid_reward, floorNum)
            moves_list[aMove] = reward
        moves_list = sorted(moves_list.items(), key=lambda item: item[1], reverse=True)

            # print("----------")
            # print(mid)
            # print("fid: ",fid)
            # print("tgrab:")
            # print(tgrab.tile_type)
            # print(tgrab.number)
            # print(tgrab.pattern_line_dest)
            # print(tgrab.num_to_pattern_line)
            # print(tgrab.num_to_floor_line)
            # print("----------")

        # for ply in game_state.players:
        #     self.requirementAnalysis(ply)
        # print(moves_list)
        tiles = 0
        for factory in game_state.factories:
            tiles += factory.total

        if tiles > self.factory_tile_number:
            self.round += 1
            my_grid = game_state.players[self.id].grid_state

            others_grid = []
            for i in range(len(game_state.players)):
                if i != self.id:
                    others_grid.append(game_state.players[i].grid_state)
            result = ""

            for line in my_grid:
                result += " ".join(str(i) for i in line)
                result += " "

            # for grid in others_grid:
            #     for lin in grid:
            #         result += " ".join(str(i) for i in line)
            #         result += " "

            # self.file.write(str(self.round) + " ")
            # self.file.writelines(result + " " + "\n")

        self.factory_tile_number = tiles;
        return moves_list[0][0]

    def moveEvaluation(self, move, myPlayer, grid_reward, floorNum):
        mid, fid, tgrab = move
        i = tgrab.pattern_line_dest
        negtivePoint = 0
        floorNegtive = [-1, -1, -2, -2, -2, -3, -3]
        floorAdding = tgrab.num_to_floor_line

        while floorAdding != 0:
            if floorNum < 6:
                negtivePoint += floorNegtive[floorNum]
                floorNum += 1
                floorAdding -= 1
            else:
                break

        if i != -1:
            j = int(myPlayer.grid_scheme[i][tgrab.tile_type])
            reward = grid_reward[i][j] * (tgrab.num_to_pattern_line + myPlayer.lines_number[i]) / (1 + i) + negtivePoint
        else:
            reward = negtivePoint

        if tgrab.num_to_pattern_line + myPlayer.lines_number[i] == i+1:
            reward += i
        return reward

    def requirementAnalysis(self, player):

        grid_reward = numpy.zeros((5, 5))
        grid_future = numpy.zeros((5, 5))

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
        # print("could be complete in this round")

        for i in range(0, 5):
            for j in range(0, 5):
                if grid_reward[i][j] != -1:
                    row =  self.countColumsReward(player, 0, (i, j))
                    colum = self.countRowsReward(player, 0, (i, j))
                    # grid_future[i][j] += self.countFutureReward(player, i, j)
                    grid_reward[i][j] += self.countFutureReward(player, i, j)
                    if row == 1:
                        grid_reward[i][j] += colum
                    elif colum == 1:
                        grid_reward[i][j] += row
                    else:
                        grid_reward[i][j] += colum
                        grid_reward[i][j] += row

        # print("immediate reward ")
        # print(grid_reward)
        # print("future reward")
        # print(grid_future)

        # print("current situation")
        # print(player.lines_tile)
        # print(player.lines_number)
        # print(player.grid_state)

        # print("CountColor")
        # print(self.countColors(player))
        return grid_reward

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