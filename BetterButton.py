import arcade


class BetterButton(arcade.TextButton):
    """
    A better button class
    """

    def __init__(self, x, y, width, height, text, function):
        super().__init__(x, y, width, height,
                        font_face='fonts/Ubuntu/Ubuntu-Regular', text=text,
                        font_color=arcade.color.BLACK, face_color=(0, 0, 0, 0),
                        highlight_color=(0, 0, 0, 0), shadow_color=(0, 0, 0, 0))

        self.mouse_pressed = False

        self.function = function

    def check_mouse_hover(self, x, y):
        if x > self.center_x + self.width / 2:
            self.face_color = (0, 0, 0, 0)
            return
        if x < self.center_x - self.width / 2:
            self.face_color = (0, 0, 0, 0)
            return
        if y > self.center_y + self.height / 2:
            self.face_color = (0, 0, 0, 0)
            return
        if y < self.center_y - self.height / 2:
            self.face_color = (0, 0, 0, 0)
            return
        if not self.mouse_pressed:
            self.on_hover()

    def on_hover(self):
        self.face_color = (0, 0, 0, 50)

    def on_press(self):
        self.mouse_pressed = True
        self.face_color = (0, 0, 0, 100)

    def check_mouse_release(self, x, y):
        if x > self.center_x + self.width / 2:
            self.face_color = (0, 0, 0, 0)
            return
        if x < self.center_x - self.width / 2:
            self.face_color = (0, 0, 0, 0)
            return
        if y > self.center_y + self.height / 2:
            self.face_color = (0, 0, 0, 0)
            return
        if y < self.center_y - self.height / 2:
            self.face_color = (0, 0, 0, 0)
            return
        self.mouse_pressed = False
        self.face_color = (0, 0, 0, 0)
        self.on_release()

    def on_release(self):
        self.function()
