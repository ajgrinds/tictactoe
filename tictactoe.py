class TicTacToe:
    """A full tic tac toe game class"""
    def __init__(self, players: int = 2):
        """
        :param players: The number of players in the game. Default 2
        :type players: int
        :param board_size: The length of one side of the board. Default 3
        :type board_size: int
        Defaults to a 3 size board and 2 players.
        """
        self.board = self.new_board(players + 1)
        self.players = players
        self.turn = 0

    def __str__(self) -> str:
        """
        :rtype: str
        """
        return self.print_board()

    def win(self) -> bool:
        """
        Scans the entire board to see if a player has won
        :rtype: bool
        """
        win = False
        for row in range(len(self.board) - 2):
            # can't win vertically if there isn't three spots left
            for column in range(len(self.board[row]) - 2):
                player = self.board[row][column]
                if player is not None:
                    if player == self.board[row][column + 1] == self.board[row][column + 2]:
                        # win horizontal
                        win = player
                    elif player == self.board[row + 1][column + 1] == self.board[row + 2][column + 2]:
                        # win down right
                        win = player
                    elif player == self.board[row + 1][column] == self.board[row + 2][column]:
                        # win vertical
                        win = player
                    elif player == self.board[row + 1][column - 1] == self.board[row + 2][column - 2]:
                        # win down left
                        win = player
                    if win:
                        break
            if self.board[row][-2] is not None:
                # Check last 2 columns
                if self.board[row][-2] == self.board[row + 1][-2] == self.board[row + 2][-2]:
                    # win vertical in second to last column
                    win = self.board[row][-2]
                elif len(self.board) > 3 and self.board[row][-2] == self.board[row + 1][-3] == self.board[row + 2][-4]:
                    # win down left in second to last column
                    win = self.board[row][-2]
            if self.board[row][-1] is not None:
                if self.board[row][-1] == self.board[row + 1][-1] == self.board[row + 2][-1]:
                    # win vertical in last column
                    win = self.board[row][-1]
                elif self.board[row][-1] == self.board[row + 1][-2] == self.board[row + 2][-3]:
                    win = self.board[row][-1]
            if win:
                break
        # Check last 2 rows
        if not win:
            for column in range(len(self.board[-1]) - 2):
                player = self.board[-1][column]
                if player is not None:
                    if player == self.board[-1][column + 1] == self.board[-1][column + 2]:
                        # win horizontal
                        win = player
                player = self.board[-2][column]
                if player is not None:
                    if player == self.board[-2][column + 1] == self.board[-2][column + 2]:
                        # win horizontal
                        win = player
                if win:
                    break
        return win

    def print_board(self) -> str:
        """
        Returns a string printing the entire board
        :rtype: str
        """
        board_str = "".join([f"\t{j + 1}\t" for j in range(len(self.board[0]))]) + "\n"
        for i in range(len(self.board)):
            board_str += f"{i + 1}"
            for j in range(len(self.board[i])):
                if j == len(self.board[i]) - 1:
                    board_str += f"\t{self.board[i][j]}\t" if self.board[i][j] is not None else "\t\t"
                else:
                    board_str += f"\t{self.board[i][j]}\t|" if self.board[i][j] is not None else "\t\t|"
            if i != len(self.board) - 1:
                board_str += "\n"
                for j in range(len(self.board[i])):
                    if j == len(self.board[i]) - 1:
                        board_str += "\t⏤\t"
                    else:
                        board_str += "\t⏤\t|"
            board_str += "\n"
        return board_str[:-1]

    def play(self) -> int:
        """
        Plays the game until a player wins based on the win function
        :return: The player that won
        :rtype: int
        """
        self.turn = 0
        cats = False
        while not self.win() and not cats:
            print(f"Player: {self.get_symbol(self.turn % self.players + 1)}")
            print(self.print_board())
            move = input(">> ").replace("(", "").replace(")", "").split(",")
            if len(move) != 2:
                print("Please make a move in the form (x,y)")
            else:
                try:
                    move[0] = int(move[0])
                    move[1] = int(move[1])
                except (TypeError, ValueError):
                    print("Please use numbers in the form (x,y)")
                else:
                    valid = self.make_move(player=self.turn % self.players + 1, position=(move[0], move[1]))
                    if valid:
                        self.turn += 1
                    print("")
            if self.turn == len(self.board)**2:
                cats = True
        print(f"Player {self.get_symbol(player=(self.turn - 1) % self.players + 1)} wins!!")
        print(self.print_board())
        return (self.turn - 1) % self.players + 1 if not cats else 0

    def make_move(self, player: int, position: tuple) -> bool:
        """
        Adds a move to the board. Should not be called
        :param player: The player who's move it is
        :type player: int
        :param position: The x,y position of the move
        :type position: tuple(int, int)
        :return: True if the move is legal
        :rtype: bool
        """
        valid = False
        if len(position) != 2:
            print("Please make a move in the form (x,y)")
        elif len(self.board) >= position[0] > 0 and len(self.board[0]) >= position[1] > 0:
            # move is possible
            if self.board[position[0] - 1][position[1] - 1] is not None:
                print("There is already someone there")
            else:
                # move is legal
                self.board[position[0] - 1][position[1] - 1] = self.get_symbol(player)
                valid = True
        else:
            print(f"The bounds for this board are ({len(self.board)}, {len(self.board[0])})")
        return valid

    @staticmethod
    def new_board(size: int) -> list:
        return [[None for i in range(size)] for j in range(size)]

    @staticmethod
    def get_symbol(player: int):
        """Define symbols for players here. If not here just uses the number (what player: player does)"""
        return {player: player,
                1: "X",
                2: "O"
                }[player]


if __name__ == '__main__':
    num_players = input("How many players? ")
    game = TicTacToe(players=int(num_players))
    game.play()
