import random
import threading
import time
import keyboard

# Funktion zur Kartenerstellung
def draw_map(coordinates, food, size=10):
    grid = [['.' for _ in range(size)] for _ in range(size)]
    for x, y in coordinates:
        grid[x][y] = 'X'
    fx, fy = food
    grid[fx][fy] = '🍎'  # Apfel-Emoji
    for row in grid:
        print(' '.join(row))
    print()

# Bewegungsfunktion mit Prüfungen
def movement_with_food(coordinates, direction, food, size=10):
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
        print("Invalid move! Game Over!")
        return False, food
    
    coordinates.append(new_head)
    if new_head == food:
        food = place_food(coordinates, size)
    else:
        coordinates.pop(0)
    return True, food

# Funktion zur Platzierung des Futters
def place_food(coordinates, size=10):
    while True:
        food = (random.randint(0, size-1), random.randint(0, size-1))
        if food not in coordinates:
            return food

# Funktion zur Steuerung der Richtung
def change_direction(event):
    global direction
    if event.name in ['up', 'down', 'left', 'right']:
        direction = {'up': 'n', 'down': 's', 'left': 'w', 'right': 'e'}[event.name]

# Hauptfunktion für das Spiel mit kontinuierlicher Bewegung
def play_dynamic_game():
    global direction
    size = int(input("Enter the size of the map (greater than 4): "))
    coordinates = [(0, 0), (0, 1), (0, 2)]
    food = place_food(coordinates, size)
    direction = 'e'  # Anfangsrichtung

    # Starte einen Thread, um Tastenereignisse zu überwachen
    keyboard.on_press(change_direction)
    
    while True:
        draw_map(coordinates, food, size)
        try:
            success, food = movement_with_food(coordinates, direction, food, size)
            if not success:
                break
        except ValueError as ve:
            print(ve)
            print("Please enter a valid direction.")
            continue
        time.sleep(0.5)  # Wartezeit zwischen den Bewegungen

play_dynamic_game()
