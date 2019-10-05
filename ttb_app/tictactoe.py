from enum import IntEnum
import copy
import random

class Token(IntEnum):
    NONE = 0
    P1 = 1
    P2 = 2

class UTTTError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)

class UltimateTicTacToe:
    """It's ULTIMATE"""
    def __init__(self):
        self.init_board()

    def init_board(self):
        self.big_board = [Token.NONE for _ in range(9)]
        self.little_boards = [copy.deepcopy(self.big_board) for _ in range(9)]
        self.player_turn = Token.P1
        self.moves = []
        self.winner = Token.NONE
        self.space = -1
    
    def random_move(self):
        if self.needs_board():
            self.select_board(random.randint(0, 8))
        self.place(random.randint(0, 8))
    
    def get_board_tuples(self):
        return zip(self.big_board, self.little_boards)
    
    def game_over(self):
        return self.winner != Token.NONE
    
    def get_winner(self):
        if self.winner == Token.NONE:
            raise UTTTError("There's no winner")
        return "X" if self.winner == Token.P1 else "O"
    
    def get_player(self):
        return "X" if self.player_turn == Token.P1 else "O"
    
    def needs_board(self):
        return self.space == -1 or self.big_board[self.space] != Token.NONE

    def select_board(self, space):
        if not self.needs_board():
            raise UTTTError("You shouldn't need to select a board right now")
        if space < 0 or space > 8:
            raise UTTTError("That space ain't in bounds.")
        if self.big_board[space] != Token.NONE:
            raise UTTTError("That space has already been won.")
        self.space = space
    
    def place(self, space):
        if self.needs_board():
            raise UTTTError("You can't place without a board")
        bx = self.space // 3
        by = self.space % 3
        lx = space // 3
        ly = space % 3
        self.validate_move(bx, by, lx, ly)
        self.place_token(self.player_turn, bx, by, lx, ly)
        self.switch_player()
        self.moves.append((bx, by, lx, ly))

    def place_token(self, token, bx, by, lx, ly):
        self.little_boards[bx*3+by][lx*3+ly] = token
        self.space = lx * 3 + ly
        if self.board_won_by_token(self.little_boards[bx*3+by], token):
            self.big_board[bx*3+by] = token
            if self.board_won_by_token(self.big_board, token):
                self.winner = token
    
    def undo(self):
        if len(self.moves) < 1:
            raise UTTTError("No moves to undo.")
        bx,by,lx,ly = self.moves.pop()
        self.little_boards[bx*3+by][lx*3+ly] = Token.NONE
        self.switch_player()
        self.space = self.moves[-1][2] * 3 + self.moves[-1][3]
    
    def switch_player(self):
        self.player_turn = Token.P2 if self.player_turn == Token.P1 else Token.P1
    
    def board_won_by_token(self, board, token):
        for i in range(3):
            l = []
            for j in range(3):
                l.append(board[i*3+j])
            if all(x == token for x in l):
                return True
        for i in range(3):
            l = []
            for j in range(3):
                l.append(board[j*3+i])
            if all(x == token for x in l):
                return True
        l = []
        for i in range(3):
            l.append(board[i*3+i])
        if all(x == token for x in l):
            return True
        l = []
        for i in range(3):
            l.append(board[i*3+2-i])
        if all(x == token for x in l):
            return True
        return False
    
    def validate_move(self, bx, by, lx, ly):
        if self.needs_board():
            raise UTTTError("Gotta set a board first bud.")
        if bx < 0 or bx > 2 or by < 0 or by > 2 or lx < 0 or lx > 2 or ly < 0 or ly > 2:
            raise UTTTError("Not a valid spot. All values gotta be between 0 and 2 inclusive.")
        if self.big_board[bx*3+by] != Token.NONE:
            raise UTTTError("That little board has already been won.")
        if self.little_boards[bx*3+by][lx*3+ly] != Token.NONE:
            raise UTTTError("There's already a token placed at that spot.")
    
    def __repr__(self):
        x = f"""
            {self.print_big_row(0)}
            -------------------------
            {self.print_big_row(1)}
            -------------------------
            {self.print_big_row(2)}
            """
        return x
    
    def print_big_row(self, row):
        return f"""{self.print_little_row(row * 3, 0)}  |  {self.print_little_row(row * 3 + 1, 0)}  |  {self.print_little_row(row * 3 + 2, 0)}
            {self.print_little_row(row * 3, 1)}  |  {self.print_little_row(row * 3 + 1, 1)}  |  {self.print_little_row(row * 3 + 2, 1)}
            {self.print_little_row(row * 3, 2)}  |  {self.print_little_row(row * 3 + 1, 2)}  |  {self.print_little_row(row * 3 + 2, 2)}"""
        
    def print_little_row(self, lb, row):
        if self.big_board[lb] == Token.P1:
            return ["XX XX", " XXX ", "XX XX"][row]
        if self.big_board[lb] == Token.P2:
            return ["OOOOO", "OO OO", "OOOOO"][row]
        
        ret = f"""{self.little_boards[lb][row*3+0]}|{self.little_boards[lb][row*3+1]}|{self.little_boards[lb][row*3+2]}"""
        ret = ret.replace("1", "X").replace("2", "O")
        if row < 2:
            return ret.replace("0", "_")
        else:
            return ret.replace("0", " ")

if __name__ == "__main__":
    print("Starting game of Ultimate Tic-Tac-Toe")
    uttt = UltimateTicTacToe()
    while not uttt.game_over():
        print(uttt)
        try:
            if uttt.needs_board():
                print(f"Which board do you want to place in? You're player {uttt.get_player()}.\nOptions: 'u' to undo, 'h' for help, or move in form 'space' (1 <= s <= 9)\n")
            else:
                print(f"What's your move? You're {uttt.get_player()} placing on board {uttt.space + 1}\nOptions: 'u' to undo, 'h' for help, or move in form 'space' (1 <= s <= 9)\n")
            s = input().strip()
            print()
            if s.lower() == "undo" or s.lower() == "u":
                uttt.undo()
                continue
            if s.lower == "help" or s.lower() == "h":
                print("""Spaces arranged in form:
            1|2|3
            4|5|6
            7|8|9
            """)
            m = int(s) - 1
            if uttt.needs_board():
                uttt.select_board(m)
            else:
                uttt.place(m)
        except UTTTError as e:
            print("No can do baby:", e)
        #except Exception as e:
        #    print("Unexpected Error:", e)
    
    print(f"Yay player {uttt.get_winner()}!")
    print(uttt)
    print(f"Player {uttt.get_winner()} won!")