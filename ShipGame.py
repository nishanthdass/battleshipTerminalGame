# Author: Nishanth Dass
# Date: 3/10/2022
# GitHub username: nishanthdass
# Description:  The below program is a python console version of a game of Battleship. The program uses three classes
#               that work together to allow the two users to place their ships on a board(represented by a simple grid
#               gui). After ships are placed the users will take turns and attempt to sink the opposite players ships.

class ShipGame:
    """Represents a game of Battleship with 2 game boards for either player, a database of created ships and a system of
     player turn tracking once the first torpedo is fired. This class will also allow for the placement horizontal &
     vertical ships on either board """

    def __init__(self):
        """ init method that has no parameters and sets all data members to their initial values"""
        self._player_boards = {'first': Board(), 'second': Board()}
        #   dictionary with ‘first’ and ‘second’ as keys & Board GUI objects as values
        self._ship_bank = {'first': [], 'second': []}
        #   dictionary with ‘first’ and ‘second’ as keys and list of placed ships as values
        self._dict_inx = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}
        #   used as way to index board positions
        self._game_init = ShotsFired()
        #   initialized to a class that will be called after first torpedo is fired

    def get_ship_bank(self):
        """Getter method that returns the dictionary of all ships placed on either board"""
        return self._ship_bank

    def place_ship(self, player_in, len_in, coordinate_in, orientation_in):
        """Method takes the player name as string, length of ship as integer, ship position and orientation as
        argument. It provides a system of validation for ships placement on the board."""
        game_instance = self._game_init
        cord_let = coordinate_in[0]
        cord_num = int(coordinate_in[1:])
        if player_in == 'first' or player_in == 'second':
            if orientation_in == "C" and 2 <= len_in <= 10 and game_instance.valid_shots(coordinate_in) is True:
                return self.val_vertical(player_in, cord_let, cord_num, len_in)
            elif orientation_in == "R" and 2 <= len_in <= 10 and game_instance.valid_shots(coordinate_in) is True:
                return self.val_horizontal(player_in, cord_let, cord_num, len_in)
            else:
                return False

    def val_vertical(self, player_in, cord_let, cord_num, len_in):
        """Helper function for place_ship method. Intended to validate vertical ship placement.  Also makes calls to the
        Board class so that vertical ships can be visualized and appends validated inputs to a ship_bank dictionary"""
        ship_part = []
        for keys in self._dict_inx:
            if self._dict_inx[keys] == cord_let:
                overflow = 10 - keys
                if len_in <= overflow:
                    ship_part = ["".join(self._dict_inx[keys + ship_len]+str(cord_num))for ship_len in range(len_in)]
                else:
                    return False
        if self.val_overlap(player_in, ship_part) is False:
            return False
        else:
            self._ship_bank[player_in] += [ship_part]
            self._player_boards[player_in].draw_verticle(player_in, cord_let, cord_num, len_in, self._dict_inx)
            return True

    def val_overlap(self, player, ship_part):
        """Helper function for place_ship method. Intended to prevent ships from overlapping each other.
        Takes the player’s name as an argument and looks to see if that player is attempting to input coordinates in
        a position that has already been added to the placed ships dictionary."""
        for used_parts in self._ship_bank[player]:
            for ind_parts in used_parts:
                for parts in ship_part:
                    if parts == ind_parts:
                        return False

    def val_horizontal(self, player_in, cord_let, cord_num, len_in):
        """Helper function for place_ship method. Intended to validate horizontal ship placement.  Also makes calls to
        the Board class so that horizontal ships can be visualized and appends validated inputs to a ship_bank
        dictionary."""
        ship_part = []
        for keys in self._dict_inx:
            if self._dict_inx[keys] == cord_let:
                size = len_in + cord_num
                if size <= 11:
                    ship_part = ["".join(cord_let + str(cord_num + ship_len))for ship_len in range(len_in)]
                else:
                    return False
        if self.val_overlap(player_in, ship_part) is False:
            return False
        else:
            self._ship_bank[player_in] += [ship_part]
            self._player_boards[player_in].draw_horizontal(player_in, cord_let, cord_num, len_in)
            return True

    def get_current_state(self):
        """returns the current state of the game: either 'FIRST_WON', 'SECOND_WON', or 'UNFINISHED'."""
        return self._game_init.get_current_state()

    def fire_torpedo(self, player_in, coordinate):
        """This method validates the turn tracking for each player, observes the game state to find a winner and record
        destroyed ships by reducing ship_bank. It does this by making calls to the ShotsFired class which will
        hold the current state, initializes & holds the player turn, record a bank of ship coordinates that were hit and
        a bank of all shots fired."""
        game_instance = self._game_init

        while game_instance.get_current_state() == 'UNFINISHED':
            if game_instance.valid_shots(coordinate) is True:
                if game_instance.switch_player(player_in) is True:
                    game_instance.target_find(player_in, coordinate, self._ship_bank)
                    game_instance.search_del(self._ship_bank)
                    game_instance.who_won(self._ship_bank)
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def get_num_ships_remaining(self, player_in):
        """Getter method takes the below player name(string) as an argument, it returns the length of the database that
        holds the ships which would be the number of ships left for either player"""
        return len(self._ship_bank[player_in])


class ShotsFired:
    """Represents a turn tracking system for the game which holds the current state, initializes & holds the player
    turn, a bank of ship coordinates that were hit and a bank of all shots fired. This class will assist in determining
    if a shot was valid and if a shot was successfully able to hit the opposite player’s ship."""
    def __init__(self):
        """init method that has no parameters and sets all data members to their initial values"""

        self._current_state = 'UNFINISHED'
        self._hold_turn = 'first'
        self._hit_ship = {'first': [], 'second': []}
        self._all_shots = {'first': [], 'second': []}

    def switch_player(self, player_in):
        """This method ensures that the correct player is taking their turn. It will work by changing
        the hold_turn data member to the next intended player after each turn is validated."""

        if player_in != self._hold_turn:
            return False
        else:
            if self._hold_turn == 'first':
                self._hold_turn = 'second'
            else:
                self._hold_turn = 'first'
            return True

    def valid_shots(self, coordinate):
        """function used to validate if the coordinates letter and number are in the correct range"""
        cord_let = coordinate[0]
        cord_num = int(coordinate[1:])
        if 1 <= cord_num <= 10 and "A" <= cord_let <= "J":
            return True
        else:
            return False

    def get_current_state(self):
        """returns the current state of the game: either 'FIRST_WON', 'SECOND_WON', or 'UNFINISHED'."""
        return self._current_state

    def target_find(self, player_in, coordinate, ship_bank):
        """Iterates through the database of placed ships and checks if the coordinate is present in the opposite
        players database of ship coordinates. It will add hit ship coordinates to hit_ship and remove that coordinate
        from the opposite ships database of placed ships."""

        all_shots = self._all_shots[player_in]
        all_shots += coordinate,

        self.string_sort(all_shots)
        for keys in ship_bank:
            if keys != player_in:
                self._hit_ship[player_in] += [ships for sublist in ship_bank[keys] for ships in sublist if ships == coordinate]
                for ships in ship_bank[keys]:
                    for parts in range(ships.count(coordinate)):
                        ships.remove(coordinate)

    def search_del(self, ship_bank):
        """function iterates through the list of placed ships, if the length of the ship is 0 because all coordinates
        have been hit, then it removes the empty list from that particular players ship bank"""
        for keys in ship_bank:
            for ships in ship_bank[keys]:
                if len(ships) == 0:
                    ship_bank[keys].remove(ships)

    def get_hit_ships(self):
        """returns dictionary of hit ship coordinates"""
        return self._hit_ship

    def who_won(self, ship_bank):
        """function checks if either player has 0 ships left, if so then the opposite player is designated the winner"""
        if len(ship_bank['first']) == 0:
            self._current_state = 'SECOND_WON'
        elif len(ship_bank['second']) == 0:
            self._current_state = 'FIRST_WON'

    def get_hold_turn(self):
        """getter method to return whose turn it currently is"""
        return self._hold_turn

    def string_sort(self, my_list):
        """string sorting function"""
        for index in range(1, len(my_list)):
            values = my_list[index]
            position = index - 1
            while position >= 0 and my_list[position].lower() > values.lower():
                my_list[position + 1] = my_list[position]
                position -= 1
            my_list[position + 1] = values


class Board:
    """Represents the game board object. This will act as the GUI for each player’s game board. The class allows for
    vertical and horizontal markings (representing ships) to be inserted into the game board."""
    def __init__(self):
        self._horiz_label = [" ", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self._board = {'A': ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                       'B': ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                       'C': ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                       'D': ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                       'E': ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                       'F': ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                       'G': ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                       'H': ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                       'I': ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                       'J': ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]}

    def board_design(self, player_in):
        """Takes a player name from the ShipGame parent class as an argument. Draws a very simple xy grid that will
        represent a separate game board for either player"""
        print()
        print("".join("     " + player_in + " player"))
        for x in self._horiz_label:
            print(x, end=' ')
        print("")
        for y in self._board:
            print(y, "".join(self._board[y]))

    def draw_verticle(self, player_in, cord_let, cord_num, len_in, dict_ind):
        """Responsible for drawing vertical markers on the Board object."""
        for index, keys in enumerate(self._board):
            if cord_let == keys:
                self._board[cord_let][cord_num - 1] = "X "
                for count in range(1, len_in):
                    self._board[dict_ind[index + count]][cord_num - 1] = "X "
        self.board_design(player_in)

    def draw_horizontal(self, player_in, cord_let, cord_num, len_in):
        """Responsible for drawing horizontal markers on the Board object."""
        for index, keys in enumerate(self._board):
            if cord_let == keys:
                self._board[cord_let][cord_num - 1] = "x "
                for count in range(1, len_in):
                    self._board[cord_let][(cord_num - 1) + count] = "x "
        self.board_design(player_in)

game = ShipGame()
