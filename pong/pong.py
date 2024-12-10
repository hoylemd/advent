from batgrl.app import App
from batgrl.colors import MAGENTA
from batgrl.gadgets.pane import Pane

FIELD_HEIGHT = 25
FIELD_WIDTH = 100


class Pong(App):
    async def on_start(self):
        game_field = Pane(size=(FIELD_HEIGHT, FIELD_WIDTH), bg_color=MAGENTA)
        self.add_gadget(game_field)
        pass

if __name__ == "__main__":
    Pong().run()
