import os

ROWS = 6
COLUMNS = 7

# Creates a blank grid for a new game
def new_grid():
    grid = [
        [0,0,0,0,0,0,0],
        [1,0,0,0,0,0,0],
        [2,0,0,0,0,0,0],
        [3,0,0,0,0,0,0],
        [4,0,0,0,0,0,0],
        [5,0,0,0,0,0,0]
    ]
    return grid

# Prints each row in the grid's list, but in reverse row order, so the 0 row will be on the bottom
def print_grid(grid):
    for row in range(len(grid)):
        print(grid[-(row + 1)])

# Ensure the selected column is a valid choice
def is_choice_valid(choice):
    if choice in range(1, COLUMNS + 1):
        return
    else:
        choice = int(input("Please enter a valid column number (1-7):"))
        is_choice_valid(choice)

def check_win():
    pass

def refresh_grid():
    pass


# Start the game
grid = new_grid()
player_turn = 0
choice = 0
game_over = False

print_grid(grid)

while game_over == False:
    # Player 1's turn
    if player_turn == 0:
        choice = int(input("Player 1, please choose a column (1-7):"))
        is_choice_valid(choice)
    # Player 2's turn
    else:
        choice = int(input("Player 2, please choose a column (1-7):"))
        is_choice_valid(choice)
    


    # Refresh grid with new selection
    os.system('cls' if os.name == 'nt' else 'clear')
    print_grid(grid)
    # Switch player's turn
    player_turn = (player_turn + 1) % 2
