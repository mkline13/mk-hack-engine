from maps import GameMap

class TestGameMap:
    def test_load_tiles(self, w=3, h=4, offset=2, tiles='x#x###x##'):
        gmap = GameMap()
        print(f"TESTING 'load_tiles(w,h,offset,tiles)' WITH THESE VALUES: w={w} h={h} offset={offset} tiles={tiles}")
        gmap.load_tiles(w, h, offset, tiles)
        print("    SUCCESS! Loaded map:")
        self.print_map(gmap, indent='        ')

    def test_dump_tiles(self, w=4, h=4, offset=4, tiles='#####@@# ##'):
        print(f"TESTING 'dump_tiles()' WITH THESE VALUES: w={w} h={h} offset={offset} tiles={tiles}")
        gmap = GameMap()
        gmap.load_tiles(w, h, offset, tiles)

        print("    LOADED MAP:")
        self.print_map(gmap, indent='         ')
        offset, result = gmap.dump_tiles()

        print(f"    DUMPED MAP: '{result}' offset='{offset}")
        if result == tiles:
            print(f"    SUCCESS!\n    ORIGINAL:   '{tiles}'")
        else:
            print(f"    FAILURE...\n    ORIGINAL: '{tiles}'")
        print()

    def test_dimensions(self, w=4, h=4, offset=4, tiles='#####@@# ##'):
        print(f"TESTING 'dimensions' property WITH THESE VALUES: w={w} h={h} offset={offset} tiles={tiles}")
        gmap = GameMap()
        gmap.load_tiles(w, h, offset, tiles)
        dim = gmap.dimensions
        print(f"    ORIGINAL: w={w} h={h}")
        print(f"    LOADED:   w={dim.x} h={dim.y}")
        if w == dim.x and h == dim.y:
            print("    SUCCESS!")
        else:
            print("    FAILURE...")
        print()

    def test_get_tile(self, x=4, y=0, w=4, h=4, offset=2, tiles='abcdefgh'):
        print(f"TESTING 'get_tile(x,y)' WITH THESE VALUES: w={w} h={h} offset={offset} tiles={tiles}")
        gmap = GameMap()
        gmap.load_tiles(w, h, offset, tiles)
        print(f"    GETTING TILE @: ({x},{y})")
        self.print_map(gmap, indent='        ')
        tile = gmap.get_tile(x, y)
        if tile == '':
            print(f"    coordinates out of range: ({x},{y})")
            print("    SUCCESS!")
        else:
            print(f"    TILE: '{tile}'")
            print("    SUCCESS!")
        print()

    def test_serialize(self, w=4, h=4, offset=2, tiles='   abcdefgh'):
        print(f"TESTING 'serialize()'")
        gmap = GameMap()
        gmap.load_tiles(w, h, offset, tiles)
        print('   ', gmap.serialize())
        print()

    def test_deserialize(self, w=4, h=4, offset=2, tiles='   abcdefgh'):
        print(f"TESTING 'deserialize()'")
        gmap = GameMap()
        gmap.load_tiles(w, h, offset, tiles)
        print("    ORIGINAL:")
        self.print_map(gmap, indent='        ')
        serial = gmap.serialize()
        print(f"    SERIAL VERSION: {str(serial)}")
        new_gmap = GameMap()
        new_gmap.deserialize(serial)
        self.print_map(new_gmap, indent='        ')

        if gmap.tiles == new_gmap.tiles:
            print("    SUCCESS! Maps match.")
        else:
            print("    FAILURE... Maps do not match.")

    def print_map(self, gmap, indent='    '):
        for row in gmap.tiles:
            print(indent, row, sep='')
        print()


if __name__ == '__main__':
    tester = TestGameMap()
    tester.test_load_tiles()
    tester.test_dump_tiles()
    tester.test_dimensions()
    tester.test_get_tile()
    tester.test_deserialize()