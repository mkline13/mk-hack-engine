class TileBuffer:
    """
    Stores an array of strings to be used for drawing ascii graphics like Rogue or NetHack.

    Provides methods for viewing this array, manipulating it, and drawing it onto other TileBuffers.
    """
    def __init__(self, w, h, tiles=[]):
        """
        :param w: the width of the buffer
        :param h: the height of the buffer
        :param tiles: a 1D array containing a list of tiles to be drawn in the specified dimensions.
        """
        self._w = w
        self._h = h

        self._tiles = tiles[:w*h]

    @property
    def tiles(self):
        """
        :returns: 1D list of tiles: tiles[index]
        """
        return self._tiles

    @property
    def tiles_2d(self):
        """
        :returns: 2D list of tiles in this format: tiles[row][col]
        """
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

    def get_tile(self, x, y, default=''):
        """
        :param x: x position to get
        :param y: y position to get
        :param default: default value to return if nothing is found
        :returns: the value of a single tile at the specified coordinates. If out of range, returns default
        """
        try:
            return self._tiles[(y * self.width) + (x % self.width)]
        except IndexError:
            return default

    def draw(self, tile_buffer, x, y):
        """
        Draws the contents of the tile buffer into another tile buffer at the specified location.
        Designed to be similar to the surface.blit() function in Pygame.
        :param tile_buffer: another tile buffer object to be drawn into.
        :param x: x position for drawing
        :param y: y position for drawing
        """
        for index, tile in enumerate(self._tiles):
            new_x = index % self._w + x
            new_y = index // self._h + y
            # check to see if drawing inside the buffer to prevent IndexError / weird wrapping
            if 0 <= new_x < tile_buffer.width and 0 <= new_y < tile_buffer.height:
                # write to screen if the tile is not blank
                if tile != '':
                    new_index = new_y * tile_buffer.width + new_x
                    tile_buffer.tiles[new_index] = tile


class Display(TileBuffer):
    """
    A specialized TileBuffer with methods for drawing to the screen.
    """
    def __init__(self, w, h, bg=' '):
        self._w = w
        self._h = h

        self._tiles = [bg for _ in range(w * h)]

    def flip(self):
        for row in self.tiles_2d:
            print(*row, sep='')
