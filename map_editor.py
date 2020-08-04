from maps import TileMap
from ascii_engine import TileBuffer, Display
from time import sleep
from blessed import Terminal

term = Terminal()


class MapEditor:
    def __init__(self, map_):
        # load empty game map
        self.map = map_

    def load_map(self, map_data: dict) -> None:
        self.map.deserialize(map_data)


def main():
    from random import choice, randint

    # gmap = TileMap()
    # editor = MapEditor(gmap)
    # editor.load_map({'tiles': '#####..##..#####', 'w': 4, 'h': 4, 'offset': 0})

    # CONSTANTS
    SCREEN_DIM = 60, 20
    MAP_DIM = 100, 50
    BG = '|'

    # SETUP
    display = Display(*SCREEN_DIM, bg=BG)
    screen_buffer = TileBuffer(*MAP_DIM, default='.')
    map_buffer = TileBuffer(*MAP_DIM, default='.')

    display.clear()

    # Draw a bunch of blobs to the map buffer
    tw, th = 5, 5
    iterations = 100
    stamp = TileBuffer(tw, th, tiles=[choice(['#', '@', '']) for _ in range(tw * th)])
    for i in range(iterations):
        stamp.draw(map_buffer, randint(-1, MAP_DIM[0]), randint(-1, MAP_DIM[1]))

    # Initialize the player graphic
    player = TileBuffer(3, 1, tiles=['{', '&', '}'])

    # Set player position
    cam_x, cam_y = 2, 2
    player_x, player_y = SCREEN_DIM[0] // 2, SCREEN_DIM[1] // 2

    # Draw the map to the screen buffer
    map_buffer.draw(screen_buffer, 0, 0)

    # Draw the player to the screen buffer
    player.draw(screen_buffer, -cam_x+player_x, -cam_y+player_y)

    # Transfer the screen buffer to the display
    screen_buffer.draw(display, cam_x, cam_y)

    # Print the screen
    display.flip()


    while True:
        # NEXT TASK: take keyboard input to move around screen
        with term.cbreak(), term.hidden_cursor():
            inp = term.inkey()

            if inp == 'q':
                break
            elif repr(inp) == 'KEY_LEFT':
                cam_x += 1
            elif repr(inp) == 'KEY_RIGHT':
                cam_x -= 1
            elif repr(inp) == 'KEY_UP':
                cam_y += 1
            elif repr(inp) == 'KEY_DOWN':
                cam_y -= 1

            # Clear the screen + fill the display buffer with something
            display.clear()
            display.fill(BG)

            # Draw the map buffer to the screen buffer
            map_buffer.draw(screen_buffer, 0, 0)

            # Draw the player to the screen buffer
            player.draw(screen_buffer, -cam_x+player_x, -cam_y+player_y)

            # Draw the screen buffer to the display
            screen_buffer.draw(display, cam_x, cam_y)

            # Print the screen
            display.flip()

    display.clear()
    print("ALL DONE!")


if __name__ == '__main__':
    main()
