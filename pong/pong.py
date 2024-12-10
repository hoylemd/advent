from batgrl.app import App
from batgrl.colors import MAGENTA, GREEN
from batgrl.gadgets.pane import Pane
from batgrl.gadgets.text import Text
from batgrl.geometry.basic import Size, Point

FIELD_DIMS = Size(25, 100)
PADDLE_DIMS = Size(5, 1)


class Paddle(Pane):
    def __init__(self, up, down, **kwargs):
        self.up = up
        self.down = down
        super().__init__(**kwargs)

    def on_key(self, key_event):
        if key_event.key == self.up:
            self.y -= 1
        elif key_event.key == self.down:
            self.y += 1

        if self.y < 0:
            self.y = 0
        elif self.y > (max_y := FIELD_DIMS.height - PADDLE_DIMS.height):
            self.y = max_y


class Pong(App):
    async def on_start(self):
        game_field = Pane(size=FIELD_DIMS, bg_color=MAGENTA)

        center = FIELD_DIMS.height // 2 - PADDLE_DIMS.height // 2

        left_paddle = Paddle(
            up="w",
            down="s",
            size=PADDLE_DIMS,
            pos=Point(center, 1),
            bg_color=GREEN
        )

        right_paddle = Paddle(
            up="up",
            down="down",
            size=PADDLE_DIMS,
            pos=Point(center, FIELD_DIMS.width - 2),
            bg_color=GREEN
        )

        divider = Pane(
            size=Size(1, 1),
            size_hint={"height_hint": 1.0},
            pos_hint={"x_hint": 0.5},
            bg_color=GREEN
        )

        left_score_label = Text(
            size=Size(1, 5),
            pos=Point(1, 1),
            pos_hint={"x_hint": 0.25}
        )

        right_score_label = Text(
            size=Size(1, 5),
            pos=Point(1, 1),
            pos_hint={"x_hint": 0.75}
        )

        game_field.add_gadgets(left_paddle, right_paddle, divider, left_score_label, right_score_label)
        self.add_gadget(game_field)


if __name__ == "__main__":
    Pong().run()
