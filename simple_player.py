# Written by Mofan Li, 2020
#
from model import *
from utils import *

class SimplePlayer(Player):
    def __init__(self, _id):
        super().__init__(_id)
        
    def evaluateMove(self, move, game_state):
        playerstate = game_state.players[self.id]
        tgrab = move[2]
        tc = tgrab.tile_type
        col = int(playerstate.grid_scheme[tgrab.pattern_line_dest][tc])
        score_inc = 0
        slots_free = (tgrab.pattern_line_dest + 2) - playerstate.lines_number[tgrab.pattern_line_dest]
        

        # count the number of tiles in a continguous line
        # above, below, to the left and right of the placed tile.
        above = 0
        for j in range(col-1, -1, -1):
            val = playerstate.grid_state[tgrab.pattern_line_dest][j]
            above += val
            if val == 0:
                break
        below = 0
        for j in range(col+1,playerstate.GRID_SIZE,1):
            val = playerstate.grid_state[tgrab.pattern_line_dest][j]
            below +=  val
            if val == 0:
                break
        left = 0
        for j in range(tgrab.pattern_line_dest-1, -1, -1):
            val = playerstate.grid_state[j][col]
            left += val
            if val == 0:
                break
        right = 0
        for j in range(tgrab.pattern_line_dest+1, playerstate.GRID_SIZE, 1):
            val = playerstate.grid_state[j][col]
            right += val
            if val == 0:
                break

        # If the tile sits in a contiguous vertical line of 
        # tiles in the grid, it is worth 1*the number of tiles
        # in this line (including itself).
        if above > 0 or below > 0:
            score_inc = (1 + above + below)

        # In addition to the vertical score, the tile is worth
        # an additional H points where H is the length of the 
        # horizontal contiguous line in which it sits.
        if left > 0 or right > 0:
            score_inc = (1 + left + right)

        # If the tile is not next to any already placed tiles
        # on the grid, it is worth 1 point.                
        if above == 0 and below == 0 and left == 0 \
            and right == 0:
            score_inc = 1
        if tgrab.pattern_line_dest == -1:
            score = -tgrab.num_to_floor_line

        score = (score_inc - tgrab.num_to_floor_line) * (tgrab.num_to_pattern_line / slots_free)

        # reward for first two lines
        if tgrab.pattern_line_dest < 3:
            score += 5
        
        # reward for persueing the same column
        for j in range(playerstate.GRID_SIZE):
            val = playerstate.grid_state[j][col]
            score += val * j

        # reward for persueing the same color
        for j in range(playerstate.GRID_SIZE):
            col = int(playerstate.grid_scheme[j][tc])
            val = playerstate.grid_state[j][col]
            score += val * j
        
        # reward for putting more tile to pattern_line
        score += 3 * tgrab.num_to_pattern_line

        # penalty for not filling all free slots in a pattern line
        if tgrab.num_to_pattern_line < slots_free:
            score -= 5
        return score 

    def SelectMove(self, moves, game_state):
        # Select move that involves placing the most number of tiles
        # in a pattern line. Tie break on number placed in floor line.
        best_move_score = -99
        best_move = None

        for mid,fid,tgrab in moves:
            move_score = self.evaluateMove((mid,fid,tgrab), game_state)
            if best_move_score == -99:
                best_move = (mid,fid,tgrab)
                best_move_score = move_score
                continue

            if move_score > best_move_score:
                best_move = (mid,fid,tgrab)
                best_move_score = move_score

        return best_move
