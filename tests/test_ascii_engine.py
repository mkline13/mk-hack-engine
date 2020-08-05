from ascii_engine import TilePlane

def test_TilePlane_conversions():
    print("TESTING conversions")
    W = 4
    H = 5
    tiles_1D = [str(i) for i in range(W*H)]
    print("ORIGINAL:\n", tiles_1D, end='\n\n')
    tiles_2D = TilePlane.tilelist_1D_to_2D(W, H, tiles_1D, default='.')
    print("2D VERSION:\n", *tiles_2D, sep='\n', end='\n\n')
    converted_back_to_1D = TilePlane.tilelist_2D_to_1D(tiles_2D)
    print("2D TO 1D:\n", tiles_1D, end='\n\n')


def test_TilePlane_display():
    print("TESTING tp.display()")
    W = 4
    H = 5
    tp = TilePlane.new_from_1D(W, H, [str(i%W) for i in range(W*H)], default='.')
    tp.display()
    print()


def test_TilePlane_get_set_tile():
    print("TESTING tp.get_tile() and tp.set_tile()")
    W = 10
    H = 6
    tp = TilePlane.new_filled(W, H, '0')
    print(*tp.tilelist, sep='\n')
    print("ORIGINAL:")
    tp.display()
    x, y = 2, 4
    val = '#'
    tp.set_tile(x, y, val)
    print(f"AFTER SETTING TILE {x},{y} to {val}:")
    tp.display()
    print(f"GET TILE {x},{y}:", tp.get_tile(x, y))
    print()

def test_TilePlane_project():
    print("TESTING tp.project()")
    print("BACKGROUND:")
    bg_tp = TilePlane.new_filled(20, 20, '.')
    bg_tp.display()
    print("FOREGROUND:")
    fg_tp = TilePlane.new_filled(2, 2, '@')
    fg_tp.display()
    print("PROJECTED:")
    fg_tp.project(bg_tp, 1, 1)
    fg_tp.project(bg_tp, -1, 4)
    fg_tp.project(bg_tp, 19, 8)
    fg_tp.project(bg_tp, 22, 11)
    fg_tp.project(bg_tp, 5, -1)
    fg_tp.project(bg_tp, 12, 19)
    fg_tp.project(bg_tp, 25, 25)
    bg_tp.display()
    print()

def test_TilePlane_subplane():
    print("TESTING tp.subplane()")
    print("MAIN:")
    w, h = 20, 10
    main_plane = TilePlane.new_from_1D(w, h, ["abcdefghijklmnopqrstuvwxyz"[i%26] for i in range(w*h)])
    main_plane.display()
    print()
    print("SUB:")
    sub = main_plane.subplane(2,2,4,4)
    sub.display()
    print()

def test_TilePlane_fill():
    print("TESTING tp.fill()")
    print("BEFORE:")
    w, h = 6, 6
    main_plane = TilePlane.new_from_1D(w, h, ["abcdefghijklmnopqrstuvwxyz"[i % 26] for i in range(w * h)])
    main_plane.display()
    print()
    print("AFTER:")
    main_plane.fill('&')
    main_plane.display()
    print()

def test_TilePlane_new_from_2D_padded():
    print("TESTING TilePlane.new_from_2D_padded()")
    W, H = 5, 4
    tile_list = [[1,2,3],[4,5],[7,8,9,0],[1,2,3,4,5,6]]
    tp = TilePlane.new_from_2D_padded(W, H, tile_list, '#')
    tp.display()
    print()


def test_TilePlane_new_filled():
    print("TESTING TilePlane.new_filled()")
    W = 10
    H = 6
    tp = TilePlane.new_filled(W, H, '0')
    tp.display()


if __name__ == '__main__':
    test_TilePlane_new_filled()
    test_TilePlane_conversions()
    test_TilePlane_display()
    test_TilePlane_get_set_tile()
    test_TilePlane_project()
    test_TilePlane_subplane()
    test_TilePlane_fill()
    test_TilePlane_new_from_2D_padded()
