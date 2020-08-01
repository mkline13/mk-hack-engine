from maps import GameMap
from vectors import Vector2D
import os
from blessed import Terminal

term = Terminal()

def clamp(val, min_, max_):
    return max(min(val, min_), max_)

class Display:
    pass


class SimpleDisplay(Display):
    def __init__(self):
        self.camera_pos = Vector2D(0,0)
        self.bg_buffer = []

    def generate_bg_buffer(self, gmap):
        self.bg_buffer = [row for row in gmap.tiles]

    def update(self, camera_pos):
        # update camera position
        self.camera_pos = camera_pos

        # Clear terminal
        print("\x1b[2J\x1b[H", end='')

        screen_width, screen_height = self.screen_size()
        print(screen_width, screen_height)
        screen_center = Vector2D(screen_width//2, screen_height//2)
        screen_ul = self.camera_pos - screen_center

        map_width, map_height = 4, 4

        left_clip = max(0,screen_ul.x)
        right_clip = min(screen_width, screen_ul.x+screen_width)

        left_pad = screen_ul.x * -1
        right_pad = right_clip - map_width + left_clip

        # Print bg_buffer to screen
        for line in range(screen_ul.y, screen_ul.y + screen_height):
            if line in range(map_height):
                view = self.bg_buffer[line]
                print('|' + (' ' * left_pad) + ''.join(view[left_clip:right_clip]) + (' ' * right_pad) + '|    ')
            else:
                print('|' + (' ' * screen_width) + '|')

    def screen_size(self):
        term_size = os.get_terminal_size()
        if term_size.columns == 0 or term_size.lines == 0:
            return 40, 20
        else:
            return term_size.columns, term_size.lines


class BlessedDisplay(Display):
    pass


class MapEditor:
    def __init__(self):
        # load empty game map
        self.map = GameMap()

    def load_map(self, map_data:dict) -> None:
        self.map.deserialize(map_data)



def main():
    editor = MapEditor()
    editor.load_map({'tiles': '#####..##..#####', 'w': 4, 'h': 4, 'offset': 0, 'properties': {}})
    display = SimpleDisplay()
    display.generate_bg_buffer(editor.map)

    camera = Vector2D(0,0)

    display.update(camera)

    while True:
        with term.cbreak():
            inp = term.inkey()
        if inp == 'q':
            break
        elif inp == 'u':
            display.update(camera)
        elif repr(inp) == 'KEY_LEFT':
            camera += Vector2D(-1, 0)
        elif repr(inp) == 'KEY_RIGHT':
            camera += Vector2D(1, 0)
        elif repr(inp) == 'KEY_UP':
            camera += Vector2D(0, -1)
        elif repr(inp) == 'KEY_LEFT':
            camera += Vector2D(0, 1)
        else:
            print(inp)


if __name__ == '__main__':
    main()