from maps import GameMap
from time import sleep
from blessed import Terminal

term = Terminal()


def clamp(val, min_, max_):
    return max(min(val, min_), max_)


def safe_get(iterable, index, default=None):
    if 0 <= index < len(iterable):
        return iterable[index]
    else:
        return default


def vec_add(l, r):
    return tuple(l[i] + r[i] for i in range(len(l)))


def vec_sub(l, r):
    return tuple(l[i] - r[i] for i in range(len(l)))


def vec_floor(l, r):
    return tuple(l[i] // r[i] for i in range(len(l)))


class Display:
    pass


class SimpleDisplay(Display):
    def __init__(self):
        self.screen_buffer = []
        self.camera_pos = (0, 0) # camera position is the center of the screen
        self.screen_size = (78, 20)

    def camera_move(self, pos):
        self.camera_pos = pos

    def camera_center(self, pos):
        self.camera_pos = vec_sub(pos, vec_floor(self.screen_size, (2,2)))

    def generate_bg_buffer(self, gmap):
        self.screen_buffer = [row for row in gmap.tiles]

    def flip(self):
        # clear screen
        print(term.home, term.clear, end='')

        # render bg_buffer to screen
        # get screen dimensions and camera offset
        sw, sh = self.screen_size
        offset_x, offset_y = self.camera_pos

        # render
        print('|' + ('-' * sw) + '|')
        for row in range(sh):
            # get the row
            r = safe_get(self.screen_buffer, row + offset_y)
            if r is not None:
                # render the row if it exists
                rendered_row = []
                print('|', end='')
                for col in range(sw):
                    print(safe_get(r, col+offset_x, ' '), sep='', end='')
                print('|')
            else:
                # otherwise render a blank row
                print('|' + (' ' * sw) + '|')
        print('|' + ('-' * sw) + '|')


class BlessedDisplay(Display):
    pass


class MapEditor:
    def __init__(self):
        # load empty game map
        self.map = GameMap()

    def load_map(self, map_data: dict) -> None:
        self.map.deserialize(map_data)


def main():
    editor = MapEditor()
    editor.load_map({'tiles': '#####..##..#####', 'w': 4, 'h': 4, 'offset': 0, 'properties': {}})

    display = SimpleDisplay()
    display.generate_bg_buffer(editor.map)

    cursor_loc = (10,10)

    display.camera_center(cursor_loc)
    display.flip()

    while True:
        # NEXT TASK: take keyboard input to move around screen
        with term.cbreak(), term.hidden_cursor():
            inp = term.inkey()

            if inp == 'q':
                break
            elif repr(inp) == 'KEY_LEFT':
                cursor_loc = vec_add(cursor_loc, (-1,0))
            elif repr(inp) == 'KEY_RIGHT':
                cursor_loc = vec_add(cursor_loc, (1, 0))
            elif repr(inp) == 'KEY_UP':
                cursor_loc = vec_add(cursor_loc, (0, -1))
            elif repr(inp) == 'KEY_DOWN':
                cursor_loc = vec_add(cursor_loc, (0, 1))

            # THEN: show cursor at center point
            display.camera_center(cursor_loc)
            display.flip()

    print(term.home, term.clear, end='')
    print("ALL DONE!")


if __name__ == '__main__':
    main()
