from tictactoe import TicTacToe


class NotTwoPlayerGameError(Exception):
    pass


def get_move(board: TicTacToe) -> tuple[int, int]:
    """
    Gets the next move the engine would play in any scenario
    :return: the move to be played in the form x,y
    :rtype: tuple
    """
    if not board.players == 2:
        raise NotTwoPlayerGameError("The game must be 2 player if you want to use the engine")
    if board.turn == 0:
        return 1, 1
    elif board.turn == 1:
        if (2, 2) == board.moves[1]:
            return 1, 1
        else:
            return 2, 2
    elif board.turn == 2:
        if (2, 1) == board.moves[1] or (1, 2) == board.moves[1] or (2, 3) == board.moves[1] or (3, 2) == board.moves[1]:
            return 2, 2
        elif (3, 1) == board.moves[1]:
            return 1, 3
        elif (1, 3) == board.moves[1] or (3, 3) == board.moves[1]:
            return 3, 1
        else:
            return 3, 3
    elif board.turn == 4:
        if (1, 2) in board.moves[0]:
            if (1, 3) in board.moves[1]:
                return 2, 2
            else:
                return 1, 3
        elif (2, 1) in board.moves[0]:
            if (3, 1) in board.moves[1]:
                if (2, 2) in board.moves[1]:
                    return 1, 3
                else:
                    return 2, 2
            else:
                return 3, 1
        elif (1, 3) in board.moves[0]:
            if (1, 2) in board.moves[1]:
                if (2, 3) in board.moves[1]:
                    return 2, 2
                else:
                    return 1, 3
            else:
                return 1, 2
    elif board.turn == 6:
        if (1, 2) in board.moves[0] and (2, 2) in board.moves[0]:
            if (3, 2) in board.moves[1]:
                return 3, 3
            else:
                return 3, 2
        elif (2, 1) in board.moves[0] and (2, 2) in board.moves[0]:
            if (2, 3) in board.moves[1]:
                return 3, 3
            else:
                return 2, 3
        elif (2, 1) in board.moves[0] and (1, 3) in board.moves[0]:
            if (1, 2) in board.moves[1]:
                if (3, 2) in board.moves[1]:
                    return 1, 3
                else:
                    return 3, 2
            else:
                return 1, 2
        elif (2, 2) in board.moves[0] and (3, 1) in board.moves[0]:
            if (2, 1) in board.moves[1]:
                return 3, 1
            else:
                return 2, 1
        elif (2, 1) in board.moves[0] and (2, 2) in board.moves[0]:
            if (2, 3) in board.moves[1]:
                return 3, 3
            else:
                return 2, 2
        elif (3, 1) in board.moves[0] and (1, 3) in board.moves[0]:
            if (1, 2) in board.moves[1]:
                return 2, 2
            else:
                return 1, 2
    else:
        if (3, 3) in board.moves[1]:
            return 2, 3
        else:
            return 3, 3


def play_x(board: TicTacToe) -> int:
    """
    Plays the game until a player wins based on the win function
    :return: The player that won
    :rtype: int
    """
    while not board.winner and not board.cats:
        board.make_move(position=get_move(board))
        print(f"Player: {board.get_symbol(board.turn % board.players + 1)}")
        print(board.print_board())
        try:
            move = list(map(lambda x: int(x), input(">> ").replace("(", "").replace(")", "").split(",")))
        except (TypeError, ValueError):
            print("Please use numbers in the form (x,y)")
        else:
            if len(move) != 2:
                print("Please make a move in the form (x,y)")
            else:
                while not board.make_move(position=tuple(move)):
                    move = list(map(lambda x: int(x), input(">> ").replace("(", "").replace(")", "").split(",")))
                print("")
    print(f"Player {board.get_symbol(player=board.winner)} wins!!")
    print(board.print_board())
    return (board.turn - 1) % board.players + 1 if not board.cats else 0


def main():
    game = TicTacToe()
    play_x(game)


if __name__ == '__main__':
    main()
