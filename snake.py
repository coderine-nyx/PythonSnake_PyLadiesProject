import random
import curses

# Comprehensive list of fruit emojis
FRUITS = ['🍎', '🍏', '🍐', '🍑', '🍒', '🍓', '🍍', '🍉', '🍇', '🍈', '🍋', '🍊', '🍅', '🍆']
SKULL = '💀'

# Fixed size of the game field
SIZE = 30

def draw_map(stdscr, coordinates, food, skulls, size, score):
    stdscr.clear()  # Clear the screen

    # Draw the border
    for x in range(size + 2):  # +2 for the top and bottom borders
        stdscr.addstr(0, x * 2, '*')
        stdscr.addstr(size + 1, x * 2, '*')

    for y in range(size + 2):  # +2 for the left and right borders
        stdscr.addstr(y, 0, '*')
        stdscr.addstr(y, (size * 2) + 2, '*')

    # Draw the game field inside the border
    for x in range(size):
        for y in range(size):
            if (x, y) == coordinates[-1]:  # Head of the snake
                stdscr.addstr(x + 1, y * 2 + 1, 'X')  # Adjusted position for border
            elif (x, y) in coordinates[:-1]:  # Body of the snake
                stdscr.addstr(x + 1, y * 2 + 1, 'O')  # Adjusted position for border
            elif (x, y) == food[1]:  # Food position
                stdscr.addstr(x + 1, y * 2 + 1, food[0])  # Fruit emoji
            elif (x, y) in skulls:  # Skull positions
                stdscr.addstr(x + 1, y * 2 + 1, SKULL)  # Skull emoji
            else:
                stdscr.addstr(x + 1, y * 2 + 1, ' ')  # Empty space

    # Display the score
    stdscr.addstr(size + 2, 0, f"Score: {score}")
    stdscr.refresh()

def movement_with_food(coordinates, direction, food, skulls, size):
    head_x, head_y = coordinates[-1]
    if direction == 'n':
        new_head = (head_x - 1, head_y)
    elif direction == 's':
        new_head = (head_x + 1, head_y)
    elif direction == 'e':
        new_head = (head_x, head_y + 1)
    elif direction == 'w':
        new_head = (head_x, head_y - 1)
    else:
        raise ValueError("Invalid direction! Use 'n', 's', 'e', or 'w'.")

    if (new_head in coordinates) or not (0 <= new_head[0] < size and 0 <= new_head[1] < size) or new_head in skulls:
        return False, food, skulls, False

    coordinates.append(new_head)
    if new_head == food[1]:
        food = place_food(coordinates, skulls, size)
        return True, food, skulls, True  # True indicates that food was eaten
    else:
        coordinates.pop(0)
        return True, food, skulls, False

def place_food(coordinates, skulls, size):
    while True:
        food_pos = (random.randint(0, size-1), random.randint(0, size-1))
        if food_pos not in coordinates and food_pos not in skulls:
            food_emoji = random.choice(FRUITS)
            return food_emoji, food_pos

def place_skulls(coordinates, size):
    skulls = set()
    while len(skulls) < 3:  # Adjust number of skulls here
        skull_pos = (random.randint(0, size-1), random.randint(0, size-1))
        if skull_pos not in coordinates:
            skulls.add(skull_pos)
    return skulls

def play_dynamic_game(stdscr):
    global SIZE

    # Initial user prompt
    stdscr.clear()
    stdscr.addstr(0, 0, "Are you ready to start the game? (y/n)")
    stdscr.refresh()
    key = stdscr.getch()
    
    if key != ord('y'):
        return  # Exit if user does not press 'y'

    # Check terminal size
    height, width = stdscr.getmaxyx()
    if SIZE > height or SIZE * 2 > width:
        stdscr.addstr(0, 0, "Terminal window too small!")
        stdscr.refresh()
        stdscr.getch()
        return

    coordinates = [(0, 0), (0, 1), (0, 2)]
    food = place_food(coordinates, set(), SIZE)
    skulls = place_skulls(coordinates, SIZE)
    direction = 'e'  # Initial direction
    score = 0        # Number of fruits eaten
    speed = 300      # Initial speed (in ms), slower start
    speed_increment = 20  # Speed increase after eating each fruit

    stdscr.nodelay(True)  # Non-blocking input
    stdscr.timeout(speed)  # Timeout for input (speed ms)

    game_over = False

    while not game_over:
        draw_map(stdscr, coordinates, food, skulls, SIZE, score)
        key = stdscr.getch()

        if key == curses.KEY_UP and direction != 's':
            direction = 'n'
        elif key == curses.KEY_DOWN and direction != 'n':
            direction = 's'
        elif key == curses.KEY_LEFT and direction != 'e':
            direction = 'w'
        elif key == curses.KEY_RIGHT and direction != 'w':
            direction = 'e'
        elif key == ord('q'):
            break
        
        try:
            success, food, skulls, ate_food = movement_with_food(coordinates, direction, food, skulls, SIZE)
            if not success:
                game_over = True
            if ate_food:
                score += 1
                speed = max(50, speed - speed_increment)  # Increase speed, not below 50 ms
                stdscr.timeout(speed)  # Update timeout for input
        except ValueError as ve:
            stdscr.addstr(SIZE + 1, 0, str(ve))
            stdscr.refresh()
            continue

    # Display "Game Over" message
    stdscr.clear()  # Clear screen to see "Game Over"
    stdscr.addstr(SIZE // 2, (SIZE * 2) // 2 - 5, "Game Over!", curses.A_BOLD)
    stdscr.addstr(SIZE // 2 + 1, (SIZE * 2) // 2 - 10, f"Final Score: {score}", curses.A_BOLD)
    stdscr.refresh()
    stdscr.nodelay(False)
    stdscr.getch()  # Wait for user input to exit

if __name__ == "__main__":
    curses.wrapper(play_dynamic_game)
