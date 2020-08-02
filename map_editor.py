from maps import GameMap
import os
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
        self.bg_buffer = []
        self.camera_pos = (0, 0) # camera position is the center of the screen

    def camera_move(self, pos):
        self.camera_pos = pos

    def camera_center(self, pos):
        self.camera_pos = vec_sub(pos, vec_floor(self.get_screen_size(), (2,2)))

    def generate_bg_buffer(self, gmap):
        self.bg_buffer = [row for row in gmap.tiles]

    def update(self):
        # render bg_buffer to screen
        sw, sh = screen_dim = self.get_screen_size()
        offset_x, offset_y = self.camera_pos

        for row in range(sh):
            r = safe_get(self.bg_buffer, row+offset_y)
            if r is not None:
                rendered_row = []
                for col in range(sw):
                    tile = safe_get(r, col+offset_x, ' ')

                    rendered_row.append(tile)
                self.print_ln(''.join(rendered_row))
            else:
                self.print_ln(' ' * sw)


    def print_ln(self, line):
        print('|' + line + '|')

    def get_screen_size(self):
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
    display.camera_center((1,1))
    display.update()


if __name__ == '__main__':
    main()