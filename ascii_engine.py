def multi_range(x, y):
    for i in range(y):
        for j in range(x):
            yield j, i

class TileBuffer:
    def __init__(self, w, h, tiles=[]):
        self._w = w
        self._h = h

        self._tiles = tiles[:w*h]

    @property
    def tiles(self):
        return self._tiles

    @property
    def tiles_2d(self):
        result = []
        for row in range(self.height):
            result.append(self._tiles[row * self.width : row * self.width + self.width])
        return result

    @property
    def width(self):
        return self._w

    @property
    def height(self):
        return self._h

    def get_tile(self, x, y):
        try:
            return self._tiles[(y * self.width) + (x % self.width)]
        except IndexError:
            return None

    def draw(self, tile_buffer, x, y):
        for index, tile in enumerate(self._tiles):
            new_x = index % self._w + x
            new_y = index // self._h + y
            # check to see if drawing inside the buffer to prevent IndexError / weird wrapping
            if 0 <= new_x < tile_buffer.width and 0 <= new_y < tile_buffer.height:
                # write to screen if the tile is not blank
                if tile != '':
                    new_index = new_y * tile_buffer.width + new_x
                    tile_buffer.tiles[new_index] = tile

    def draw_test(self, tile_buffer, x, y):
        for index, tile in enumerate(self._tiles):
            new_x = index % self._w + x
            new_y = index // self._h + y
            # check to see if drawing inside the buffer to prevent IndexError / weird wrapping
            if 0 <= new_x < tile_buffer.width and 0 <= new_y < tile_buffer.height:
                # write to screen if the tile is not blank
                if tile != '':
                    new_index = new_y * tile_buffer.width + new_x
                    tile_buffer.tiles[new_index] = '{:<3}'.format(str(new_index))



class Display(TileBuffer):
    def __init__(self, w, h, bg=' '):
        self._w = w
        self._h = h

        self._tiles = [bg for _ in range(w * h)]

    def flip(self):
        for row in self.tiles_2d:
            print(*row, sep='')



def test_TileBuffer(w=4, h=3, tiles=[0,1,2,3,4,5,6,7,8,9,10,11]):
    tb = TileBuffer(w, h, tiles)
    print(tb.tiles)
    print(tb.tiles_2d)

    for x, y in multi_range(tb.width, tb.height):
        print(tb.get_tile(x, y))


def test_TileBuffer_draw(tb1=TileBuffer(15, 8, tiles=['-' for _ in range(120)]), tb2=TileBuffer(2, 2, tiles=['#', '#', '', '#',])):
    print(*tb1.tiles_2d, sep='\n')
    print()
    print(*tb2.tiles_2d, sep='\n')
    print()
    x, y = 1, 3
    print(f"DRAWING AT ({x}, {y})")
    tb2.draw(tb1, x, y)
    x, y = 6, 5
    print(f"DRAWING AT ({x}, {y})")
    tb2.draw(tb1, x, y)
    for r in tb1.tiles_2d:
        print(*r, sep='')


def test_Display():
    from blessed import Terminal
    term = Terminal()
    print(term.home + term.clear, end='')

    bg = '#'
    W, H = 25, 12
    DIM = 30
    display = Display(W, H, bg=bg)
    map_buffer = TileBuffer(DIM, DIM, tiles=['.' for _ in range(DIM*DIM)])

    obj1 = TileBuffer(2, 2, tiles = [term.white_on_black(t) if t != '' else '' for t in ['#', '#', '', '#',]])
    obj2 = TileBuffer(3, 4, tiles = [1,2,3,4,5,6,7,8,9,0,1,2])
    player = TileBuffer(1, 1, tiles = [term.yellow_on_black('@')])

    obj1.draw(map_buffer, 1, 1)
    obj1.draw(map_buffer, 10, 10)
    obj1.draw(map_buffer, 20, 5)
    obj2.draw(map_buffer, 4, 4)
    player.draw(map_buffer, 5, 5)

    map_buffer.draw(display, -12, 1)
    display.flip()
    print()



def main():
    # CONSTANTS
    SCREEN_SIZE = (78, 20)

    # SETUP
    display = Display(*SCREEN_SIZE)
    print(SCREEN_SIZE)

    # MAIN LOOP


if __name__ == '__main__':
    # test_TileBuffer()
    # test_TileBuffer_draw()
     test_Display()
    # main()