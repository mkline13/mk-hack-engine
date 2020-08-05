from maps import TileMap
from ascii_engine import TilePlane
from time import sleep
from blessed import Terminal

term = Terminal()

class Cursor:
    def __init__(self, x, y, cam_offset_x, cam_offset_y):
        self.x = x
        self.y = y
        self._cam_offset_x = cam_offset_x
        self._cam_offset_y = cam_offset_y

    def draw(self, tile_plane):
        char = tile_plane.get_tile(self.x, self.y, default=' ')
        tile_plane.set_tile(self.x, self.y, term.black_on_blue(char))

    def get_camera_pos(self):
        return -self.x + self._cam_offset_x, -self.y + self._cam_offset_y

class Text:
    def __init__(self, text, visible=False):
        self.text = text
        self.visible = visible

    def draw(self, tile_plane, x, y):
        if self.visible:
            current_x = x
            current_y = y
            for char in self.text:
                if char != '\n':
                    tile_plane.set_tile(current_x, current_y, char)
                    current_x += 1
                else:
                    current_x = x
                    current_y += 1

    def style(self, style_func):
        new_string = []
        for char in self.text:
            new_string.append(style_func(char))
        self.text = ''.join(new_string)


def main():
    # CONSTANTS
    SCREEN_DIM = 60, 20
    HALF_SCREEN_DIM = SCREEN_DIM[0] // 2, SCREEN_DIM[1] // 2
    MAP_DIM = 100, 50
    BG = '|'

    # SETUP
    VALID_CHARS = r'abcdefghijklmnopqrstuvwxyz1234567890-[]\;:/?<>,.~!@#$%^&*()_={}|` '
    previous_char = ' '

    display = TilePlane.new_filled(*SCREEN_DIM, BG)
    screen_buffer = TilePlane.new_filled(*MAP_DIM, fill='')
    map_buffer = TilePlane.new_filled(*MAP_DIM, fill=' ')
    text_display = Text("Hello World!", visible=True)

    cursor = Cursor(25, 5, *HALF_SCREEN_DIM)

    # Draw the map to the screen buffer
    map_buffer.project(screen_buffer, 0, 0)
    # Draw the cursor onto the screen buffer
    cursor.draw(screen_buffer)
    # Transfer the screen buffer to the display
    screen_buffer.project(display, *cursor.get_camera_pos())

    # Display text
    text_display.text = f" POS: ({cursor.x}, {cursor.y}) \n CHAR: {map_buffer.get_tile(cursor.x, cursor.y)} "
    text_display.draw(display, 3, 1)

    # Print the screen
    print(term.home + term.clear, end='')
    display.display()

    while True:
        # NEXT TASK: take keyboard input to move around screen
        with term.cbreak(), term.hidden_cursor():
            inp = term.inkey()

            if inp == 'q':
                break
            elif inp in VALID_CHARS:
                map_buffer.set_tile(cursor.x, cursor.y, inp[0])
                previous_char = inp[0]
            elif inp == '\t':
                map_buffer.set_tile(cursor.x, cursor.y, previous_char)
            elif repr(inp) == 'KEY_LEFT':
                cursor.x -= 1
            elif repr(inp) == 'KEY_RIGHT':
                cursor.x += 1
            elif repr(inp) == 'KEY_UP':
                cursor.y -= 1
            elif repr(inp) == 'KEY_DOWN':
                cursor.y += 1

            # UPDATE STUFF

            # Fill the screen
            display.fill(BG)

            # Draw the map to the screen buffer
            map_buffer.project(screen_buffer, 0, 0)
            # Draw the cursor onto the screen buffer
            cursor.draw(screen_buffer)
            # Transfer the screen buffer to the display
            screen_buffer.project(display, *cursor.get_camera_pos())

            # Update text display
            text_display.text = f" POS: ({cursor.x}, {cursor.y}) \n CHAR: {map_buffer.get_tile(cursor.x, cursor.y)} "
            text_display.draw(display, 3, 1)

            # Print the screen
            print(term.home + term.clear, end='')
            display.display()

    print(term.home + term.clear, end='')
    print("ALL DONE!")


if __name__ == '__main__':
    main()
