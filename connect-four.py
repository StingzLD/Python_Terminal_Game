import os
import sys

BANNER = '''
_________                                     __    ___________                 
\_   ___ \  ____   ____   ____   ____   _____/  |_  \_   _____/___  __ _________ 
/    \  \/ /  _ \ /    \ /    \_/ __ \_/ ___\   __\  |    __)/  _ \|  |  \_  __ \ 
\     \___(  <_> )   |  \   |  \  ___/\  \___|  |    |   |  (  <_> )  |  /|  | \/
 \________/\____/|___|__/___|__/\_____>\_____>__|    \___|   \____/|____/ |__|


'''
ROWS = 6
COLUMNS = 7
player = 0
choice = 0
row = 0
game_over = False

# Creates a blank grid for a new game
def new_grid() -> list:
    grid = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ]
    return grid

# Prints each row in the grid's list, but in reverse row order, so the 0 row will be on the bottom
def print_grid(grid):
    for row in range(len(grid)):
        print((" " * 28) + str(grid[-(row + 1)]))
    print("\n")

# Ensure the selected column is a valid choice, if not reprompt until it is
def get_player_choice():
    global choice

    try:
        choice = int(input("Player " + str(player + 1) + ", please choose a column (1-7):"))
    except:
        choice = retry()

    while True:
        if choice >= 1 and choice <= 7:
            if grid[ROWS - 1][choice - 1] == 0:
                if choice in range(1, COLUMNS + 1):
                    break
                else:
                    choice = reprompt_choice((" " * 24) + "*** INVALID COLUMN NUMBER ***\nPlayer " + str(player + 1) + ", please enter a valid column number (1-7):")
                    continue
            else:
                choice = reprompt_choice((" " * 24) + f"*** NO MORE OPEN SPACES IN COLUMN {choice} ***\nPlayer " + str(player + 1) + ", please enter a valid column number (1-7):")
                continue
        elif choice < 1:
            choice = reprompt_choice((" " * 24) + "*** COLUMN NUMBER TOO LOW ***\nPlayer " + str(player + 1) + ", please enter a valid column number (1-7):")
            continue
        else:
            choice = reprompt_choice((" " * 24) + "*** COLUMN NUMBER TOO HIGH ***\nPlayer " + str(player + 1) + ", please enter a valid column number (1-7):")
            continue

# Delete previous two lines in terminal
def delete_lines():
    sys.stdout.write('\x1b[1A') # Move cursor up one line
    sys.stdout.write('\x1b[2K') # Delete line
    sys.stdout.write('\x1b[1A') # Move cursor up one line
    sys.stdout.write('\x1b[2K') # Delete line

# Prompt for new choice
def reprompt_choice(msg):
    delete_lines()
    try:
        new_choice = int(input(msg))
    except:
        new_choice = retry()  
    return new_choice

# Give user another chance to enter an integer, otherwise they forfeit the game
def retry():
    try:
        delete_lines()
        new_choice = int(input((" " * 24) + "*** A NUMBER WAS NOT ENTERED ***\nPlayer " + str(player + 1) + ", please enter a valid column number (1-7):"))
        return new_choice
    except:
        end_game()

# Find the next available row for the player's chosen column
def find_open_row():
    for row in range(ROWS):
        if grid[row][choice -1] == 0:
            return row

# Update the grid
def place_piece():
    grid[row][choice - 1] = player + 1

# Perform a series of checks to see if the current player has won
def check_win():
    # Check the row of the last placed piece to see if there are four in a row
    count = 0
    for column in grid[row]:
        if column != player + 1:
            count = 0
        elif column == player + 1:
            count += 1
        if count >= 4:
            player_wins()
            return

    # Check the column of the last placed piece to see if there are four in a row
    count = 0
    for grid_row in grid:
        if grid_row[choice - 1] != player + 1:
            count = 0
        elif grid_row[choice - 1] == player + 1:
            count += 1
        if count >= 4:
            player_wins()
            return
    
    # Check to see if there are four in a row diagonally going up from left to right
    current_row = row
    current_column = choice - 1
    count = 0
    while current_row != 0 and current_column != 0:
        current_row -= 1
        current_column -= 1
    try:
        while current_row <= ROWS - 1 and current_column <= COLUMNS - 1:
            if grid[current_row][current_column] == player + 1:
                count += 1
            else:
                count = 0
            if count >= 4:
                player_wins()
                return
            current_row += 1
            current_column += 1
    except:
        pass

    # Check to see if there are four in a row diagonally going up from right to left
    current_row = row
    current_column = choice - 1
    count = 0
    while current_row != 0 and current_column != COLUMNS - 1:
        current_row -= 1
        current_column += 1
    try:
        while current_row <= ROWS - 1 and current_column >= 0:
            if grid[current_row][current_column] == player + 1:
                count += 1
            else:
                count = 0
            if count >= 4:
                player_wins()
                return
            current_row += 1
            current_column -= 1
    except:
        pass

    # Check if there are any spots left to place pieces
    count = 0
    for column in range(len(grid[ROWS - 1])):
        if grid[ROWS-1][column] == 0:
            break
        else:
            count += 1
    if count == COLUMNS:
        print((" " * 33) + "IT'S A TIE!!!")
        return

# End game and display the winning player
def player_wins():
    global game_over
    
    game_over = True
    print((" " * 31) + "PLAYER " + str(player + 1) + " WINS!!!")

# End game if current user does not enter an integer twice in a row
def end_game():
    swap_players()
    delete_lines()
    print("\n" + (" " * 31) + "PLAYER " + str(player + 1) + " WINS!!!")
    exit()

# Refresh grid with new selection
def refresh_grid():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)
    print_grid(grid)
    print((" " * 29) + "1  2  3  4  5  6  7\n")

# Swap player turn
def swap_players():
    global player

    player = ((player + 1) % 2)

# Start the game    
if __name__ == "__main__":
   grid = new_grid()
   refresh_grid()

   while game_over == False:
        get_player_choice()
        row = find_open_row()
        place_piece()
        refresh_grid()
        check_win()
        swap_players()
