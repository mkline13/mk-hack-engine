from maps import TileMap
from ascii_engine import TilePlane
from time import sleep
from blessed import Terminal

term = Terminal()

def main():
    from random import choice, randint

    # CONSTANTS
    SCREEN_DIM = 60, 20
    MAP_DIM = 100, 50
    BG = '|'

    # SETUP
    display = TilePlane.new_filled(*SCREEN_DIM, BG)
    screen_buffer = TilePlane.new_filled(*MAP_DIM, fill='')
    map_buffer = TilePlane.new_filled(*MAP_DIM, fill='.')

    # Draw a bunch of blobs to the map buffer
    iterations = 500
    for i in range(iterations):
        x = randint(0, MAP_DIM[0])
        y = randint(0, MAP_DIM[1])
        map_buffer.set_tile(x, y, choice(['*', '=', '%']))

    # Initialize the player graphic
    player = TilePlane(3, 1, tiles=['{', '&', '}'])

    # Set player position
    cam_x, cam_y = 2, 2
    player_x, player_y = SCREEN_DIM[0] // 2 - 2, SCREEN_DIM[1] // 2 - 1

    # Draw the map to the screen buffer
    map_buffer.project(screen_buffer, 0, 0)
    # Draw the player to the screen buffer
    player.project(screen_buffer, -cam_x+player_x, -cam_y+player_y)
    # Transfer the screen buffer to the display
    screen_buffer.project(display, cam_x, cam_y)

    # Print the screen
    print(term.home + term.clear, end='')
    display.display()

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

            # UPDATE STUFF

            # Fill the screen
            display.fill('|')

            # Draw the map to the screen buffer
            map_buffer.project(screen_buffer, 0, 0)
            # Draw the cursor
            player.project(screen_buffer, -cam_x + player_x, -cam_y + player_y)
            # Transfer the screen buffer to the display
            screen_buffer.project(display, cam_x, cam_y)

            # Print the screen
            print(term.home + term.clear, end='')
            display.display()

    print(term.home + term.clear, end='')
    print("ALL DONE!")


if __name__ == '__main__':
    main()
