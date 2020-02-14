from tictactoe import TicTacToe


def get_move(board: TicTacToe):
    if board.turn == 0:
        return 1, 1
    elif board.turn == 2:
        if (2, 1) in board.moves[1] or (3, 1) in board.moves[1]:
            return 1, 2
        elif (2, 3) in board.moves[1]:
            return 2, 2
        elif (3, 3) in board.moves[1] or (2, 3) in board.moves[1]:
            return 1, 3
        else:
            return 2, 1
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
        print(f"Player: {board.get_symbol(board.turn % board.players + 2)}")
        print(board.print_board())
        try:
            move = map(lambda x: int(x), input(">> ").replace("(", "").replace(")", "").split(","))
        except (TypeError, ValueError):
            print("Please use numbers in the form (x,y)")
        else:
            if len(list(move)) != 2:
                print("Please make a move in the form (x,y)")
            else:
                valid = board.make_move(position=(next(move), next(move)))
                print("")
    print(f"Player {board.get_symbol(player=(board.turn - 1) % board.players + 1)} wins!!")
    print(board.print_board())
    return (board.turn - 1) % board.players + 1 if not board.cats else 0


def main():
    game = TicTacToe()
    play_x(game)


if __name__ == '__main__':
    main()
