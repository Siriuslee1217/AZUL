import model as md
from utils import Tile
import random
import copy
class difficultyEvaluation:

    # a summary of all tiles in the factory now
    # return a dictionary, key: tile type, value: number
    def tilesFactory(self, gameState):
        tiles = {}

        for factory in gameState.factories:
            if factory != []:
                if tiles == {}:
                    tiles = self.sumTiles(factory)
                else:
                    tiles_fac = self.sumTiles(factory)
                    for color in tiles.keys():
                        tiles[color] += tiles_fac[color]

        return tiles
    # Tiles chosen for next round in the bag
    # return a list of tiles
    def nextRoundPosibleTiles(self, gameState):
        state = copy.deepcopy(gameState)

        currentbag = state.bag

        _, bag_used = state.ScoreRound()

        if len(gameState.bag) < gameState.NUM_ON_FACTORY and len(bag_used) > 0:
            random.shuffle(gameState.bag_used)
            bagNextRound = currentbag.extend(bag_used)

        else:
            bagNextRound = gameState.bag

        return bagNextRound

    # Tiles possibility next round(num_tileType/ total)
    # return a dictionary, key: tileType, value: possibility next round
    def nextRoundPosibility(self, gameState):
        tiles_NextRound = self.sumTiles(self.nextRoundPosibleTiles(gameState))
        ColorsPossibility = {}

        number = tiles_NextRound["total"]

        for color in tiles_NextRound.keys():
            if color != "total":
                ColorsPossibility[color] = tiles_NextRound[color]/tiles_NextRound["total"]

        return ColorsPossibility

    # number of tiles of different types and a total
    # return a dictionary, key: tile type and a "total", value: number
    def sumTiles(self, bag):
        tiles = {}
        tiles[Tile.RED] = 0
        tiles[Tile.BLACK] = 0
        tiles[Tile.BLUE] = 0
        tiles[Tile.WHITE] = 0
        tiles[Tile.YELLOW] = 0
        for tile in bag:
            tiles[tile] += 1

        tiles["total"] = 0
        for color in tiles.keys():
            if color != "total":
                tiles["total"] += tiles[color]

        return tiles

    # tiles left after a simulation for other players
    # 模拟完毕以后会不会有得分更高的move？
    def tilesPossibleNextPick(self, gameState, myid):
        roundTiles = self.tilesFactory(gameState)
        players = gameState.players
        for playerState in players:
            if playerState.id != myid:
                possibleMove = bestMove(playerState) # 这里可以减很多move的，不一定是best的
                tileType = possibleMove[2].tile_type
                tileNum = possibleMove[2].number
                roundTiles[tileType] -= tileNum

        return roundTiles

    # possible available moves next pick after simulation
    # return a list of moves
    def movesPossibleNextPick(self, gameState, myId):
        state = copy.deepcopy(gameState)

        players = gameState.players

        for playerState in players:
            if playerState.id != myId:
                state.ExecuteMove(playerState.id, bestMove(playerState))

        availableMoves = state.players[myId].GetAvailableMoves(state)
        
        return availableMoves





    # tiles that other players can not place on lines
    # return dictionary, key: playerId, value:unavailable tiles(can only be placed on floor)
    def safeTiles(self, gameState):
        players = gameState.players
        playerUnavailable = {}


        for playerState in players:
            availableTileColors = {}
            playerUnavailable[playerState.id] = []

            moves = playerState.GetAvailableMoves()
            for move in moves:
                for mid, fid, tg in move:

                    # adjust here
                    if tg.num_to_pattern_line > 0:
                        availableTileColors[tg.tile_type] = 1

            tileTypes = [Tile.RED, Tile.BLACK, Tile.BLUE, Tile.WHITE, Tile.YELLOW]

            for tile in tileTypes:
                if tile not in availableTileColors.keys:
                    playerUnavailable[playerState.id].append(tile)

        return playerUnavailable