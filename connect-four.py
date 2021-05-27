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
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]
    return grid


# Prints each row in the grid's list, but in reverse row order, so the 0 row will be on the bottom
def print_grid(current_grid):
    for row in range(len(current_grid)):
        print(f"{' ' * 28} {current_grid[-(row + 1)]}")
    print("\n")


# Get the current player number
def get_player():
    return player + 1


# Prompt for player's choice
def player_prompt():
    return f"Player {get_player()}, please choose a column (1-7):"


# Ensure the selected column is a valid choice, if not reprompt until it is
def get_player_choice():
    global choice

    try:
        choice = int(input(player_prompt()))
    except ValueError:
        choice = retry()
    except KeyboardInterrupt:
        clear_screen()
        exit()

    while True:
        if 1 <= choice <= 7:
            if grid[ROWS - 1][choice - 1] == 0:
                if choice in range(1, COLUMNS + 1):
                    break
                else:
                    choice = reprompt_choice(
                        error_msg("INVALID COLUMN NUMBER"))
                    continue
            else:
                choice = reprompt_choice(
                    error_msg("NO MORE OPEN SPACES IN COLUMN", choice))
                continue
        elif choice < 1:
            choice = reprompt_choice(error_msg("COLUMN NUMBER TOO LOW"))
            continue
        else:
            choice = reprompt_choice(error_msg("COLUMN NUMBER TOO HIGH"))
            continue


# Error messages
def error_msg(msg, choice=None):
    if choice is None:
        return f"{' ' * 24} *** {msg} ***\n{player_prompt()}"
    else:
        return f"{' ' * 24} *** {msg} {choice} ***\n{player_prompt()}"


# Delete previous two lines in terminal
def delete_lines():
    sys.stdout.write('\x1b[1A')  # Move cursor up one line
    sys.stdout.write('\x1b[2K')  # Delete line
    sys.stdout.write('\x1b[1A')  # Move cursor up one line
    sys.stdout.write('\x1b[2K')  # Delete line


# Prompt for new choice
def reprompt_choice(msg):
    delete_lines()
    try:
        new_choice = int(input(msg))
        return new_choice
    except ValueError:
        new_choice = retry()
        return new_choice
    except KeyboardInterrupt:
        clear_screen()
        exit()


# Give user another chance to enter an integer, otherwise they forfeit the game
def retry():
    try:
        delete_lines()
        new_choice = int(input(error_msg("A NUMBER WAS NOT ENTERED")))
        return new_choice
    except ValueError:
        end_game()
    except KeyboardInterrupt:
        clear_screen()
        exit()


# Find the next available row for the player's chosen column
def find_open_row():
    for row in range(ROWS):
        if grid[row][choice - 1] == 0:
            return row


# Update the grid
def place_piece():
    grid[row][choice - 1] = get_player()


# Perform a series of checks to see if the current player has won
def check_win():
    global game_over

    # Check the row of the last placed piece to see if there are four in a row
    count = 0

    for column in grid[row]:
        if column != get_player():
            count = 0
        elif column == get_player():
            count += 1

        if count >= 4:
            player_wins()
            return

    # Check the column of the last placed piece to see if there are four in a row
    count = 0

    for grid_row in grid:
        if grid_row[choice - 1] != get_player():
            count = 0
        elif grid_row[choice - 1] == get_player():
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

    while current_row <= ROWS - 1 and current_column <= COLUMNS - 1:
        if grid[current_row][current_column] == get_player():
            count += 1
        else:
            count = 0

        if count >= 4:
            player_wins()
            return

        current_row += 1
        current_column += 1

    # Check to see if there are four in a row diagonally going up from right to left
    current_row = row
    current_column = choice - 1
    count = 0

    while current_row != 0 and current_column != COLUMNS - 1:
        current_row -= 1
        current_column += 1

    while current_row <= ROWS - 1 and current_column >= 0:
        if grid[current_row][current_column] == get_player():
            count += 1
        else:
            count = 0

        if count >= 4:
            player_wins()
            return

        current_row += 1
        current_column -= 1

    # Check if there are any spots left to place pieces
    count = 0

    for column in range(len(grid[ROWS - 1])):
        if grid[ROWS - 1][column] == 0:
            break
        else:
            count += 1

    if count == COLUMNS:
        print(f"{' ' * 33} IT'S A TIE!!!")
        game_over = True
        return


# Displays the winning player
def winner():
    return f"{' ' * 31} PLAYER {get_player()} WINS!!!"


# End game and display the winning player
def player_wins():
    global game_over

    game_over = True
    print(winner())


# End game if current user does not enter an integer twice in a row
def end_game():
    swap_players()
    delete_lines()
    print(f"\n{winner()}")
    exit()


# Clears the terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Refresh grid with new selection
def refresh_grid():
    clear_screen()
    print(BANNER)
    print_grid(grid)
    print(f"{' ' * 29} 1  2  3  4  5  6  7\n")


# Swap player turn
def swap_players():
    global player

    player = ((get_player()) % 2)


# Start the game
if __name__ == "__main__":
    grid = new_grid()
    refresh_grid()

    while game_over is False:
        get_player_choice()
        row = find_open_row()
        place_piece()
        refresh_grid()
        check_win()
        swap_players()
