class TicTacToe:
    def __init__(self):
        self.board = self.new_board(3)

        # NEED TO UPDATE WITH COMMANDS
        self.commands = self.get_commands()

    def __str__(self):
        return ""

    def get_commands(self):
        return {"play": self.play,
                "help": self.help}

    def play(self):
        pass

    def help(self):
        """Prints a list of all available commands"""
        print("All available commands are:")
        for command in self.commands:
            print(f"  {command}\n\t {self.commands[command].__doc__}")

    def new_command(self) -> bool:
        valid = False
        command = input(">>> ").split(" ")
        if command[0] not in self.commands:
            print("That's not a valid command. Use 'help' to print a list of the commands")
        else:
            if len(self.commands[command[0]].__annotations__) != len(command) + 1:
                print(f"Please use the correct arguments {self.commands[command[0]].__doc__}")
            else:


    def make_move(self, player: int, position: tuple) -> bool:
        valid = False
        if len(position) != 2:
            print("Please make a move in the form (x,y)")
        elif len(self.board) >= position[0] > 0 and len(self.board[0]) >= position[1] > 0:
            # move is possible
            if self.board[position[0] - 1][position[1] - 1] is not None:
                print("There is already someone there")
            else:
                # move is legal
                self.board[position[0] - 1][position[1] - 1] = player
                valid = True
        else:
            print(f"The bounds for the move are ({len(self.board)}, {len(self.board[0])}")
        return valid

    @staticmethod
    def new_board(size: int) -> list:
        return [[None for i in range(size)] for j in range(size)]
