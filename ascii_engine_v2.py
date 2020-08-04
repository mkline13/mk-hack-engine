class TilePlane:
    """
    Contains a 2D array, a list of columns. Addressed like so: tp[x][y]
    """

    def __init__(self, w, h, tilelist):
        """
        Initialize the 2D array.

        :param w: width of array
        :param h: height of array
        :param tilelist: 2D list containing chars. Assumes the user will supply a list of the correct format.
        """
        self._w = w
        self._h = h
        self._tilelist = tilelist

    def project(self, destination, dest_x, dest_y):
        """
        Project the contents of the plane onto the destination plane at the specified location.

        :param destination: plane to be projected on to
        :param dest_x: x coordinate of the origin of the current plane on the destination plane
        :param dest_y: y coordinate of the origin of the current plane on the destination plane
        :return:
        """
        for x, y in TilePlane.iterate_2D(self._w, self._h):
            new_x = x + dest_x
            new_y = y + dest_y
            # clip to boundaries
            if 0 <= new_x < destination.w and 0 <= new_y < destination.h:
                destination.tilelist[new_x][new_y] = self._tilelist[x][y]

    def subplane(self, x, y, w, h):
        """
        Returns a new TilePlane object containing a snapshot of this plane at the specified coordinates.
        :param x: x coordinate of origin of new plane
        :param y: y coordinate of origin of new plane
        :param w: width of new plane
        :param h: height of new plane
        :return:
        """
        sub = TilePlane.new_filled(w, h, '')
        self.project(sub, -x, -y)
        return sub

    def get_tile(self, x, y, default=''):
        """
        Safely retrieve the value of a tile at a location.
        Returns default if the coordinates are out-of-bounds.
        :param x: x coordinate of tile to get
        :param y: y coordinate of tile to get
        :param default: value to return if coordinates are out-of-bounds
        :return:
        """
        try:
            return self._tilelist[x][y]
        except IndexError:
            return default

    def set_tile(self, x, y, val):
        """
        Safely set the value of a tile at a location.
        Fails silently if coordinate is out of bounds.
        :param x: x coordinate of tile to set
        :param y: y coordinate of tile to set
        :param val: new value for specified tile
        :return:
        """
        try:
            self._tilelist[x][y] = val
        except IndexError:
            pass

    def display(self):
        """
        Prints the contents of the tile list out onto the screen.
        :return:
        """
        for y in range(self._h):
            for x in range(self._w):
                print(self._tilelist[x][y], end='')
            print()

    def fill(self, val):
        """
        Fill this plane with chars of a specified value
        :param val: value of all chars in the plane
        :return:
        """
        for x, y in TilePlane.iterate_2D(self._w, self._h):
            self._tilelist[x][y] = val

    @property
    def tilelist(self):
        return self._tilelist

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h

    @property
    def dim(self):
        return self._w, self._h

    @staticmethod
    def tilelist_1D_to_2D(w, h, tilelist_1D=[], default=' '):
        """
        Converts a 1D list of chars into a 2D list with the specified dimensions.
        :param w: Width of new 2D list
        :param h: Height of new 2D list
        :param tilelist_1D: 1D list that will be converted
        :param default: default value for any padding tiles added to the list
        :return:
        """
        columns = []
        for x in range(w):
            col = []
            for y in range(h):
                index_1D = y * w + x
                if index_1D < len(tilelist_1D):
                    col.append(tilelist_1D[index_1D])
                else:
                    col.append(default)
            columns.append(col)
        return columns

    @staticmethod
    def tilelist_2D_to_1D(tilelist_2D):
        """
        Converts a 2D list of chars into a 1D list of chars.
        :param tilelist_2D: 2D char list
        :return:
        """
        w = len(tilelist_2D)
        h = len(tilelist_2D[0])

        tilelist_1D = ['' for _ in range(w*h)]
        for x in range(w):
            for y in range(h):
                index_1D = y * w + x
                tilelist_1D[index_1D] = tilelist_2D[x][y]
        return tilelist_1D

    @staticmethod
    def iterate_2D(w, h):
        """
        A helper method that returns a generator object for iterating through 2D arrays.
        :param w: range of x values
        :param h: range of y values
        :return:
        """
        for x in range(w):
            for y in range(h):
                yield x, y

    @staticmethod
    def new_from_1D(w, h, tilelist, default=' '):
        """
        A constructor for creating a TilePlane directly from a 1D char list.
        :param w: width of new TilePlane
        :param h: height of new TilePlane
        :param tilelist: 1D tile list
        :param default: default value for any padding tiles added to the list
        :return:
        """
        tilelist_2D = TilePlane.tilelist_1D_to_2D(w, h, tilelist, default)
        return TilePlane(w, h, tilelist_2D)

    @staticmethod
    def new_from_2D_padded(w, h, tilelist, default=' '):
        """
        A constructor for creating a TilePlane when the dimensions of the input tilelist may not be certain
        :param w: width of new TilePlane
        :param h: height of new TilePlane
        :param tilelist: A 2D list of tiles that will be padded up to the correct size
        :param default: value for padding
        :return:
        """
        tp = TilePlane.new_filled(w, h, default)
        blank_tile_list = [[default for x in range(w)] for y in range(h)]
        for x, y in TilePlane.iterate_2D(w, h):
            try:
                val = tilelist[x][y]
            except IndexError:
                val = default

            tp.set_tile(x, y, val)
        return tp

    @staticmethod
    def new_filled(w, h, fill):
        """
        A constructor for creating a TilePlane of a certain size filled with a certain value
        :param w: width of new TilePlane
        :param h: height of new TilePlane
        :param fill: char to fill TilePlane with
        :return:
        """
        return TilePlane(w, h, [[fill for y in range(h)] for x in range(w)])
