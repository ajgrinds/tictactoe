from colors import light_colors, dark_colors


class BaseState:
    def __init__(self, colors: dict):
        self.colors = colors

    def dark_mode(self, state: bool):
        if state:
            self.colors = dark_colors
        else:
            self.colors = light_colors

    def cleanup(self):
        pass
