# Author: Phoenix Harris
# Date: 5.27.2020
# Description: This code is an implementation of the Gess board game - a Chess/Go variant. The GessGame, Board, and
#              Piece classes manage the state of the game together. Two players take turns making moves until one player
#              destroys the ring of the opponent or someone concedes defeat. Each player starts with one ring, but can
#              form more if desired. Valid distance and direction of a move are determined by the orientation of the
#              footprint of a piece.

class GessGame:
    """
    The GessGame class is used to make and play a game of Gess - a Chess/Go variant board game.
    The game board is stored in a Board object, and managed by the Board class.
    Game pieces are stored in Piece objects, and manipulated by the Piece, Board, and GessGame classes.
    GessGame methods for move validation and execution communicate with the Board and Piece classes.
    GessGame methods for checking the game state or resigning the game do not require communication with other classes.
    """
    def __init__(self):
        """
        Initializes the data members of a GessGame object.
        board - stored in a Board object.
        game_state - who, if anyone, won the game
        whose_turn - player whose turn it is to make a move
        up_next - player who is not currently authorized to make a move
        direction - direction of the move being made (list of two integers)
        distance - distance of the move being made
        """
        self._board = Board()
        self._game_state = "UNFINISHED"
        self._whose_turn = "B"
        self._up_next = "W"
        self._direction = None
        self._distance = None

    def get_board(self):
        """
        :return: the Board object associated with an instance of GessGame object
        """
        return self._board

    def get_game_state(self):
        """
        :return: a string indicating which player has won, or that the game is unfinished
        """
        return self._game_state

    def resign_game(self):
        """
        Allows a player to concede their demise.
        Changes the game_state attribute depending on whose turn it is,
        which is determined from the whose_turn attribute.
        """
        if self._whose_turn == "B":
            self._game_state = "WHITE_WON"
        else:
            self._game_state = "BLACK_WON"

    def make_move(self, start, end):
        """
        Makes a move if the move is legal and the game is not unfinished.

        A move is legal if the center of the piece starts and finishes on the board, the piece has no stones of the
        opponent, and the direction and distance are valid.

        Validity of direction of movement is determined by checking the orientation of the footprint of a Piece object.
        Validity of distance is determined by whether the piece has a center stone and the attempted distance.

        A move cannot break the mover's own last ring.

        :param start: the starting coordinate of the piece to be moved (list of two integers)
        :param end: the ending coordinate of the piece to be moved (list of two integers)
        :return: True if valid move-request; False if invalid move-request
        """
        # convert input game-board position - 'k18' - to a list of corresponding list indices - [3, 11]
        start = self.coordinate_conversion(start)
        end = self.coordinate_conversion(end)

        # if the game is over
        if self._game_state != "UNFINISHED":
            return False

        # if the move is not on the board
        if start[0] > 19 or start[0] < 1 or start[1] > 20 or start[1] < 1:
            return False
        if end[0] > 19 or end[0] < 1 or end[1] > 20 or end[1] < 1:
            return False

        # if the piece has stones of the opponent
        check_piece = Piece(start, self._board.get_game_board())
        if not check_piece.valid_piece(self._up_next):
            return False

        # if the direction and distance are valid, attempt the move
        if self.valid_direction(start, end) and self.valid_distance(start, end):
            return self.board_step(start, end)
        else:
            return False

    def coordinate_conversion(self, position):
        """
        Converts a game-board position to a list with corresponding indices list[x][x]
        Example: input of 'd16' returns  [5,4], which is used to access board[5][4]
        """
        return [21 - int(position[1:]), ord(position[0]) - 96]

    def valid_direction(self, start, end):
        """
        Checks whether the direction of a requested move is valid.
        This is determined by checking the orientation of the footprint of a Piece object.

        If direction is valid, the direction attribute is set accordingly.
        Example: an attempted northeastern move would set the direction attribute to [-1, 1].

        :param start: the starting coordinate of the piece to be moved (list of two integers)
        :param end: the ending coordinate of the piece to be moved (list of two integers)
        :return: True if direction of requested move is valid; False if direction of requested move is invalid
        """
        # make a piece object
        moving_piece = Piece(start, self._board.get_game_board())

        # is the piece moving southward?
        if end[0] > start[0]:

            # is the piece moving southeast?
            if end[1] > start[1]:

                # is the move truly diagonal?
                if abs(end[0] - start[0]) == abs(end[1] - start[1]):

                    # is there a stone in the SE position of the piece?
                    if moving_piece.get_piece_SE() == self._whose_turn:
                        self._direction = [1, 1]  # set the direction of the move
                        return True

            # repeat of the above for a southwest move
            elif end[1] < start[1]:
                if abs(end[0] - start[0]) == abs(end[1] - start[1]):
                    if moving_piece.get_piece_SW() == self._whose_turn:
                        self._direction = [1, -1]  # set the direction of the move
                        return True

            # must be direct south movement if reaches this line
            else:
                if moving_piece.get_piece_S() == self._whose_turn:
                    self._direction = [1, 0]  # set the direction of the move
                    return True

        # is the piece moving northward?
        elif end[0] < start[0]:

            # is the piece moving northeast?
            if end[1] > start[1]:

                # is the move truly diagonal?
                if abs(end[0] - start[0]) == abs(end[1] - start[1]):

                    # is there a stone in the NE position of the piece?
                    if moving_piece.get_piece_NE() == self._whose_turn:
                        self._direction = [-1, 1]  # set the direction of the move
                        return True

            # repeat of the above for a northwest move
            elif end[1] < start[1]:
                if abs(end[0] - start[0]) == abs(end[1] - start[1]):
                    if moving_piece.get_piece_NW() == self._whose_turn:
                        self._direction = [-1, -1]  # set the direction of the move
                        return True

            # must be direct north movement if this line is reached
            else:
                if moving_piece.get_piece_N() == self._whose_turn:
                    self._direction = [-1, 0]  # set the direction of the move
                    return True

        # direct east movement
        elif end[0] == start[0] and end[1] > start[1]:
            if moving_piece.get_piece_E() == self._whose_turn:  # stone in the east position?
                self._direction = [0, 1]  # set direction of the move
                return True

        # direct west movement
        elif end[0] == start[0] and end[1] < start[1]:
            if moving_piece.get_piece_W() == self._whose_turn:  # stone in the west position?
                self._direction = [0, -1]  # set direction of the move
                return True

        return False  # not a valid direction of movement

    def valid_distance(self, start, end):
        """
        Checks whether the distance of a requested move is valid.
        This is determined by whether the piece has a center stone and the attempted distance.
        If the piece has no center stone, only a distance of 3 is allowed.
        If the piece has a center stone, any distance is allowed.

        If distance is valid, the distance attribute is set.

        :param start: the starting coordinate of the piece to be moved (list of two integers)
        :param end: the ending coordinate of the piece to be moved (list of two integers)
        :return: True if distance of requested move is valid; False if distance of requested move is invalid
        """
        # make a piece object
        moving_piece = Piece(start, self._board.get_game_board())

        # if there is a stone in the center of the piece, any distance is valid
        if moving_piece.get_piece_center() == self._whose_turn:
            if end[0] != start[0]:
                self._distance = abs(end[0] - start[0])  # set distance based on vertical movement

            elif end[1] != start[1]:
                self._distance = abs(end[1] - start[1])  # set distance based on horizontal movement

            return True

        # if there is no stone in the center of the piece, the move-distance cannot be greater than 3
        else:
            if abs(end[0] - start[0]) > 3 or abs(end[1] - start[1] > 3):
                # the requested move-distance is greater than 3, but no stone in center of piece
                return False

            if end[0] != start[0]:
                self._distance = abs(end[0] - start[0])  # set distance based on vertical movement
            elif end[1] != start[1]:
                self._distance = abs(end[1] - start[1])  # set distance based on horizontal movement

            return True

    def board_step(self, start, end):
        """
        This method steps across the board in the direction and distance of the desired move, checking at each step
        whether the requested move is obstructed. When only one step is left, the piece is added to the board in its
        final destination, overwriting whatever is there.

        A spot is checked for obstructions by making piece object and then confirming that the piece is empty.

        If movement is obstructed, the move is not made.
        If a the player who made the move broke their own last ring, the board is returned to its previous state.

        :param start: the starting coordinate of the piece to be moved (list of two integers)
        :param end: the ending coordinate of the piece to be moved (list of two integers)
        :return: True if the move was unobstructed and executed; False if the move was obstructed and not executed
        """
        # make a copy of the piece to be moved and remove it from the board
        moving_piece = Piece(start, self._board.get_game_board())
        self._board.remove_piece(start)

        # go in the direction of the move, one step at a time, checking for obstructions at each step
        moving_coordinate = start[:]
        while self._distance > 1:
            # move the coordinate to the next check-position
            moving_coordinate[0] += self._direction[0]
            moving_coordinate[1] += self._direction[1]

            check_piece = Piece(moving_coordinate, self._board.get_game_board())
            if not check_piece.is_empty():  # if the "piece" has any stones, then the path of the move is obstructed
                self._board.add_piece(moving_piece, start)  # return the piece to its starting position
                return False

            self._distance -= 1

        if self.still_in(self._board):  # if the mover didn't break their own last ring
            self._board.add_piece(moving_piece, end)  # add the piece, overwriting the contents of the board
            self._whose_turn, self._up_next = self._up_next, self._whose_turn  # update whose turn it is
            self.still_in_double_check(self._board)  # update game_state if necessary
            return True

        else:
            # return the board to its previous state
            self._board.add_piece(moving_piece, start)

            return False

    def still_in(self, game_board):
        """
        Checks if each player is still in the game.
        This is done by making a piece object at each valid spot on the board and checking for a ring.

        Changes game_state if the player who made the move breaks the other player's last ring.

        This version of the function is called before a move is finalized (piece not yet placed in final destination).

        :param game_board: a board object
        :return: True if the player who made the move is still in, False otherwise.
        """
        def check_piece(color):
            """
            Makes a temporary piece at each valid spot on the board, checking if the piece is a ring.

            :param color: color of the player being checked
            :return: True if the player has a ring; False if the player has no ring
            """
            for row in range(3, 19):
                for column in range(3, 19):  # for every square on the board where rings are possible
                    ring_check = Piece([row, column], game_board.get_game_board())  # make a piece
                    if ring_check.is_ring(color):  # check if the piece is a ring
                        return True
            return False

        if check_piece(self._whose_turn):  # if the move didn't break the mover's own last ring
            if not check_piece(self._up_next):  # if the move broke the opponent's last ring
                # change game_state accordingly
                if self._whose_turn == "B":
                    self._game_state = "BLACK_WON"
                else:
                    self._game_state = "WHITE_WON"

            return True

        else:

            return False

    def still_in_double_check(self, game_board):
        """
        Checks if each player is still in the game.
        This is done by making a piece object at each valid spot on the board and checking for a ring.

        Changes game_state if the player who made the move breaks the other player's last ring.

        This version of the function is called after a move is finalized (piece placed in final destination).
        This is because the ring of the opponent won't be broken until the moving piece is finally set.

        :param game_board: a board object
        :return: True if the player who made the move is still in, False otherwise.
        """
        def check_piece(color):
            """
            Makes a temporary piece at each valid spot on the board, checking if the piece is a ring.

            :param color: color of the player being checked
            :return: True if the player has a ring; False if the player has no ring
            """
            for row in range(3, 19):
                for column in range(3, 19):  # for every square on the board where rings are possible
                    ring_check = Piece([row, column], game_board.get_game_board())  # make a piece
                    if ring_check.is_ring(color):  # check if the piece is a ring
                        return True
            return False

        if check_piece(self._up_next):  # if the move didn't break the mover's own last ring
            if not check_piece(self._whose_turn):  # if the move broke the opponent's last ring
                # change game_state accordingly
                if self._whose_turn == "W":
                    self._game_state = "BLACK_WON"
                else:
                    self._game_state = "WHITE_WON"

            return True

        else:

            return False


class Board:
    """
    The Board class has one data member: the board of a GessGame object.
    The GessGame class uses Board class methods and data member.
    The Board class manages the state of the game board by adding and removing game Piece objects.
    The Board class needs to communicate with a the Piece class in order to add a Piece, but removing a Piece can be
    done without communication with the Piece class.
    """

    def __init__(self):
        """
        Initializes the board data member of the board class.
        The board is a list of lists.
        The top row and left column are completely inaccessible to the GessGame class, and are only there for playing
        purposes.
        """
        self._board = [[' ', 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t'],
                       [20,  '  ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                       [19,  '  ',' ','W',' ','W',' ','W','W','W','W','W','W','W','W',' ','W',' ','W',' ',' '],
                       [18,  '  ','W','W','W',' ','W',' ','W','W','W','W',' ','W',' ','W',' ','W','W','W',' '],
                       [17,  '  ',' ','W',' ','W',' ','W','W','W','W','W','W','W','W',' ','W',' ','W',' ',' '],
                       [16,  '  ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                       [15,  '  ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                       [14,  '  ',' ','W',' ',' ','W',' ',' ','W',' ',' ','W',' ',' ','W',' ',' ','W',' ',' '],
                       [13,  '  ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                       [12,  '  ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                       [11,  '  ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                       [10,  '  ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                       [9,   '   ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                       [8,   '   ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                       [7,   '   ',' ','B',' ',' ','B',' ',' ','B',' ',' ','B',' ',' ','B',' ',' ','B',' ',' '],
                       [6,   '   ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                       [5,   '   ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                       [4,   '   ',' ','B',' ','B',' ','B','B','B','B','B','B','B','B',' ','B',' ','B',' ',' '],
                       [3,   '   ','B','B','B',' ','B',' ','B','B','B','B',' ','B',' ','B',' ','B','B','B',' '],
                       [2,   '   ',' ','B',' ','B',' ','B','B','B','B','B','B','B','B',' ','B',' ','B',' ',' '],
                       [1,   '   ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']]

    def get_game_board(self):
        """
        :return: board data member (list of lists)
        """
        return self._board

    def remove_piece(self, location):
        """
        Removes a piece centered at the coordinates specified by the input parameter.
        The center and all surrounding "squares" are filled with a string of one space, which indicates no stone.
        :param location: list of two integers indicating location on the board
        """
        self._board[location[0]][location[1]] = ' '
        self._board[location[0] + 1][location[1]] = ' '
        self._board[location[0] + 1][location[1] + 1] = ' '
        self._board[location[0] + 1][location[1] - 1] = ' '
        self._board[location[0]][location[1] + 1] = ' '
        self._board[location[0] - 1][location[1]] = ' '
        self._board[location[0] - 1][location[1] + 1] = ' '
        self._board[location[0] - 1][location[1] - 1] = ' '
        self._board[location[0]][location[1] - 1] = ' '

    def add_piece(self, piece, location):
        """
        Adds the attributes of a Piece object to the board attribute of a Board object.
        The piece is only added if its center is on the board - b to s horizontally and 2 to 19 vertically.
        Piece perimeter attributes are not added if they are off the board,
        but the portion of the perimeter that is on the board is added.
        :param piece: a Piece object
        :param location: list of two integers indicating location on the board
        """
        # if the center of the piece is being added to a valid spot on the board...
        if location[0] in range(2,20) and location[1] in range(2,20):
            self._board[location[0]][location[1]] = piece.get_piece_center()

            # then add the center, plus any other part of the piece that is not off the board
            if location[0] - 1 in range(2,20) and location[1] in range(2,20):
                self._board[location[0] - 1][location[1]] = piece.get_piece_N()

            if location[0] - 1 in range(2,20) and location[1] - 1 in range(2,20):
                self._board[location[0] - 1][location[1] - 1] = piece.get_piece_NW()

            if location[0] - 1 in range(2,20) and location[1] + 1 in range(2,20):
                self._board[location[0] - 1][location[1] + 1] = piece.get_piece_NE()

            if location[0] + 1 in range(2,20) and location[1] in range(2,20):
                self._board[location[0] + 1][location[1]] = piece.get_piece_S()

            if location[0] + 1 in range(2,20) and location[1] - 1 in range(2,20):
                self._board[location[0] + 1][location[1] - 1] = piece.get_piece_SW()

            if location[0] + 1 in range(2,20) and location[1] + 1 in range(2,20):
                self._board[location[0] + 1][location[1] + 1] = piece.get_piece_SE()

            if location[0] in range(2,20) and location[1] + 1 in range(2,20):
                self._board[location[0]][location[1] + 1] = piece.get_piece_E()

            if location[0] in range(2,20) and location[1] - 1 in range(2,20):
                self._board[location[0]][location[1] - 1] = piece.get_piece_W()


class Piece:
    """
    The Piece class has data members for keeping track of where stones are in a GessGame board-piece.
    Piece class methods look at Piece attributes to return relevant information such as if the Piece is a ring or empty.
    Communication with the Board class is required to make a Piece object;
    a Piece object is a copy of a section of board from a Board object.
    """
    def __init__(self, location, board):
        """
        Fills the Piece with stones or spaces depending on the orientation
        of the input Board object and location on the board.
        :param location: list of two integers indicating location on the board
        :param board: a Board object
        """
        self._center = board[location[0]][location[1]]
        self._N = board[location[0] - 1][location[1]]
        self._NW = board[location[0] - 1][location[1] - 1]
        self._NE = board[location[0] - 1][location[1] + 1]
        self._S = board[location[0] + 1][location[1]]
        self._SW = board[location[0] + 1][location[1] - 1]
        self._SE = board[location[0] + 1][location[1] + 1]
        self._W = board[location[0]][location[1] - 1]
        self._E = board[location[0]][location[1] + 1]

        self._piece_matrix = [[self._NW, self._N, self._NE],
                              [self._W, self._center, self._E],
                              [self._SW, self._S, self._SE]]

    def perimeter(self):
        """
        The perimeter method is used by the is_ring method to check if a piece is a ring.
        :return: a list with all attributes of the Piece except the center attribute
        """
        return [self._N, self._NW, self._NE, self._S, self._SW, self._SE, self._W, self._E]

    def is_ring(self, color):
        """
        Checks whether a piece is a ring.
        A ring is a piece with a perimeter of all the same stone, but no center stone.
        :param color: color of the stones of the piece that might be a ring
        :return: True if piece is a ring; False if piece is not a ring
        """
        if self._center == " ":  # can only be a ring if center has no stone
            perimeter_count = 0
            for stone in self.perimeter():
                if stone == color:
                    perimeter_count += 1
            if perimeter_count == 8:  # if every stone in the perimeter is the specified color
                return True
        else:
            return False

    def valid_piece(self, up_next):
        """
        Confirms that a piece does not have stones of the other player.
        :param up_next: color of the player who is not currently authorized to make a move
        :return: True if piece has no stones of the opponent; False otherwise
        """
        if self._center == up_next:
            return False
        if up_next in self.perimeter():
            return False

        return True

    def is_empty(self):
        """
        :return: True if a piece has no stones; False if a piece has a stone
        """
        for row in self._piece_matrix:
            for space in row:
                if space != ' ':  # no stone in the space
                    return False

        return True

    def get_piece_center(self):
        """
        :return: center attribute of the piece
        """
        return self._center

    def get_piece_N(self):
        """
        :return: north attribute of the piece
        """
        return self._N

    def get_piece_NW(self):
        """
        :return: northwest attribute of the piece
        """
        return self._NW

    def get_piece_NE(self):
        """
        :return: northeast attribute of the piece
        """
        return self._NE

    def get_piece_S(self):
        """
        :return: south attribute of the piece
        """
        return self._S

    def get_piece_SW(self):
        """
        :return: southwest attribute of the piece
        """
        return self._SW

    def get_piece_SE(self):
        """
        :return: southeast attribute of the piece
        """
        return self._SE

    def get_piece_W(self):
        """
        :return: west attribute of the piece
        """
        return self._W

    def get_piece_E(self):
        """
        :return: east attribute of the piece
        """
        return self._E
