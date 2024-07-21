import random
import curses

# Umfassende Liste der Frucht-Emojis
FRUITS = ['🍎', '🍏', '🍐', '🍑', '🍒', '🍓', '🥭', '🍍', '🍉', '🍇', '🍈', '🍋', '🍊', '🍅', '🍆']

def draw_map(stdscr, coordinates, food, size, score):
    stdscr.clear()  # Bildschirm löschen
    for x in range(size):
        for y in range(size):
            if (x, y) in coordinates:
                stdscr.addstr(x, y * 2, 'X')
            elif (x, y) == food[1]:
                stdscr.addstr(x, y * 2, food[0])  # Emoji der Frucht anzeigen
            else:
                stdscr.addstr(x, y * 2, '.')
    
    # Anzeige der Anzahl der gegessenen Äpfel
    stdscr.addstr(size, 0, f"Score: {score}")
    stdscr.refresh()

def movement_with_food(coordinates, direction, food, size):
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

    if (new_head in coordinates) or not (0 <= new_head[0] < size and 0 <= new_head[1] < size):
        return False, food, False

    coordinates.append(new_head)
    if new_head == food[1]:
        food = place_food(coordinates, size)
        return True, food, True  # True indicates that food was eaten
    else:
        coordinates.pop(0)
        return True, food, False

def place_food(coordinates, size):
    while True:
        food_pos = (random.randint(0, size-1), random.randint(0, size-1))
        if food_pos not in coordinates:
            food_emoji = random.choice(FRUITS)
            return food_emoji, food_pos

def play_dynamic_game(stdscr):
    global size
    # Überprüfen der Terminalgröße
    height, width = stdscr.getmaxyx()
    if size > height or size * 2 > width:
        stdscr.addstr(0, 0, "Terminal window too small!")
        stdscr.refresh()
        stdscr.getch()
        return

    coordinates = [(0, 0), (0, 1), (0, 2)]
    food = place_food(coordinates, size)
    direction = 'e'  # Anfangsrichtung
    score = 0        # Anzahl der gegessenen Äpfel
    speed = 300      # Anfangsgeschwindigkeit (in ms), langsamer Start
    speed_increment = 20  # Erhöhung der Geschwindigkeit nach jedem gegessenen Apfel

    stdscr.nodelay(True)  # Eingaben nicht blockieren
    stdscr.timeout(speed)  # Timeout für Eingabe (speed ms)

    game_over = False

    while not game_over:
        draw_map(stdscr, coordinates, food, size, score)
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
            success, food, ate_food = movement_with_food(coordinates, direction, food, size)
            if not success:
                game_over = True
            if ate_food:
                score += 1
                speed = max(50, speed - speed_increment)  # Geschwindigkeit erhöhen, nicht unter 50 ms
                stdscr.timeout(speed)  # Aktualisieren des Timeouts für die Eingabe
        except ValueError as ve:
            stdscr.addstr(size + 1, 0, str(ve))
            stdscr.refresh()
            continue

    # Anzeigen der Game Over-Nachricht
    stdscr.clear()  # Bildschirm löschen, um das "Game Over"-Label zu sehen
    stdscr.addstr(size // 2, (size * 2) // 2 - 5, "Game Over!", curses.A_BOLD)
    stdscr.addstr(size // 2 + 1, (size * 2) // 2 - 10, f"Final Score: {score}", curses.A_BOLD)
    stdscr.refresh()
    stdscr.nodelay(False)
    stdscr.getch()  # Warten auf Benutzereingabe, um das Programm zu beenden

if __name__ == "__main__":
    size = int(input("Enter the size of the map (greater than 4): "))
    curses.wrapper(play_dynamic_game)
