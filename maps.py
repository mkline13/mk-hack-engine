from vectors import Vector2D

class GameMap:
    """
    Implements a class for storing map data for games with ASCII-based graphics.

    Here is how it's used:
    >>> gmap = GameMap()
    >>> gmap.load_tiles(x=10, y=10, w=4, h=4, offset=2, tiles='abcdefgh')

    User should access the individual tiles like this:
    >>> x, y = 0, 2
    >>> tile = gmap.get_tile(x, y)

    The 'get_tile' function will return a blank string if no tile exists at the coordinates provided.
    >>> x, y = -1, -1
    >>> tile = gmap.get_tile(x,y)
    ''

    Data is stored in a nested list of rows. It can be accessed like this (but shouldn't be):
    >>> gmap.tiles[2][0]
    """
    def __init__(self):
        self.properties = {}
        self.tiles = []

    def load_tiles(self, w, h, offset, tiles) -> None:
        # create 1D array with padding for empty tiles
        l_padding = [' ' for _ in range(offset)]
        tiles_list_1d = l_padding + list(tiles)
        r_padding = [' ' for _ in range(w * h - len(tiles_list_1d))]
        tiles_list_1d.extend(r_padding)

        # reset tiles array
        self.tiles = []

        # create 2D array
        for row in range(h):
            self.tiles.append(tiles_list_1d[row * w: row * w + w])

    def dump_tiles(self):
        tiles_list_1d = []
        for row in self.tiles:
            tiles_list_1d.extend(row)

        offset = 0
        for i in tiles_list_1d:
            if i == ' ':
                offset += 1
                continue
            else:
                break

        tiles_str = ''.join(tiles_list_1d).strip(' ')
        return offset, tiles_str

    @property
    def dimensions(self):
        return Vector2D(len(self.tiles), len(self.tiles[0]))

    def get_tile(self, x: int, y: int) -> str:
        try:
            return self.tiles[y][x]
        except IndexError:
            return ""

    def serialize(self) -> dict:
        dict_rep = {}
        offset, tiles = self.dump_tiles()
        dict_rep['tiles'] = tiles
        dict_rep['w'], dict_rep['h'] = self.dimensions.x, self.dimensions.y
        dict_rep['offset'] = offset
        dict_rep['properties'] = self.properties
        return dict_rep

    def deserialize(self, dict_rep) -> None:
        self.load_tiles(dict_rep['w'], dict_rep['h'], dict_rep['offset'], dict_rep['tiles'])
        self.properties = dict_rep['properties']

