from django.db import models
from ttb_app.tictactoe import UltimateTicTacToe, UTTTError, Token

# Create your models here.
class DjangoBoard(models.Model):
    big_board_state = models.CharField(max_length=10)
    little_boards_state = models.CharField(max_length=100)
    player_turn_state = models.IntegerField()
    # TODO: add move serialization
    winner_state = models.IntegerField()
    space_state = models.IntegerField()

    def __init__(self):
        self.big_board_state = "---------"
        self.little_boards_state = "---------------------------------------------------------------------------------"
        self.player_turn_state = Token.P1
        self.winner_state = Token.NONE
        self.space_state = -1

    def set_state_from_uttt(self, uttt):
        self.big_board_state = self.deboardify(uttt.big_board)
        self.little_boards_state = "".join(self.deboardify(arr) for arr in uttt.little_boards)
        self.player_turn_state = uttt.player_turn
        self.winner_state = uttt.winner
        self.space_state = uttt.space
    
    def boardify(self, nine_length_string):
        return [self.char_to_token(c) for c in nine_length_string]
    
    def deboardify(self, array):
        return "".join(self.token_to_char(t) for t in array)
    
    def get_utt_from_state(self):
        uttt = UltimateTicTacToe()
        uttt.big_board = self.boardify(self.big_board_state)
        uttt.little_boards = [self.boardify(self.little_boards_state[start*9:start*9+9]) for start in range(9)]
        uttt.player_turn = self.player_turn_state
        uttt.winner = self.winner_state
        uttt.space = self.space_state
        return uttt
    
    def token_to_char(self, token):
        if token == Token.NONE:
            return " "
        elif token == Token.P1:
            return "X"
        elif token == Token.P2:
            return "O"
        else:
            return "-"
    
    def char_to_token(self, char):
        if char == "X":
            return Token.P1
        elif char == "O":
            return Token.P2
        else:
            return Token.NONE

    def get_board_tuples(self):
        board_tuples = self.get_utt_from_state().get_board_tuples()
        #ret = []
        #for x,y in board_tuples:
        #    t = (self.token_to_char(x), self.deboardify(y))
        #    ret.append(t)
        ret = list(board_tuples)
        return ret

    def __repr__(self):
        return repr(self.get_utt_from_state())