class GessGame:

    def __init__(self):
        self._board = Board()
        self._game_state = "UNFINISHED"
        self._whose_turn = "B"
        self._up_next = "W"
        self._direction = None
        self._distance = None

    def get_board(self):
        return self._board

    def make_move(self, start, end):

        # convert game-board positions to list indices
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
        Example: 'd16' to  [5,4], which is list[5][4]
        """
        return [21 - int(position[1:]), ord(position[0]) - 96]

    def valid_direction(self, start, end):
        """
        Checks whether the direction of a requested move is valid
        If direction is valid, the direction attribute is set, and True is returned
        If the direction is not valid, False is returned
        """
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

            # must be direct south movement
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

            # must be direct north movement
            else:
                if moving_piece.get_piece_N() == self._whose_turn:
                    self._direction = [-1, 0]  # set the direction of the move
                    return True

        # direct east move?
        elif end[0] == start[0] and end[1] > start[1]:
            if moving_piece.get_piece_E() == self._whose_turn:  # stone in the east position?
                self._direction = [0, 1]  # set direction of the move
                return True

        # direct west move?
        elif end[0] == start[0] and end[1] < start[1]:
            if moving_piece.get_piece_W() == self._whose_turn:  # stone in the west position?
                self._direction = [0, -1]  # set direction of the move
                return True

        return False  # not a valid direction of movement

    def valid_distance(self, start, end):
        """
        Checks whether the distance of a requested move is valid
        If distance is valid, the distance attribute is set, and True is returned
        If the distance is not valid, False is returned
        """
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
            if abs(end[0] - start[0]) > 3 or abs(end[1] - start[1] >3):
                return False  # the move-distance is greater than 3, but no stone in center of piece

            if end[0] != start[0]:
                self._distance = abs(end[0] - start[0])  # set distance based on vertical movement
            elif end[1] != start[1]:
                self._distance = abs(end[1] - start[1])  # set distance based on horizontal movement

            return True

    def board_step(self, start, end):
        moving_piece = Piece(start, self._board.get_game_board())
        moving_coordinate = start[:]
        self._board.remove_piece(start)
        while self._distance > 1:
            # add a line for if piece is still on board?.. I think I already have this covered!

            # move the coordinate to the next check position
            moving_coordinate[0] += self._direction[0]
            moving_coordinate[1] += self._direction[1]
            check_piece = Piece(moving_coordinate, self._board.get_game_board())
            if not check_piece.is_empty():  # if the "piece" has any stones, then the path of the move is obstructed
                self._board.add_piece(moving_piece, start)  # return the piece to its starting position
                return False

            self._distance -= 1

        # add the piece back to the board in its final destination, overwriting anything that's already there
        self._board.add_piece(moving_piece, end)

        if self.still_in(self._board):  # if the mover didn't break their own last ring
            self._whose_turn, self._up_next = self._up_next, self._whose_turn  # update whose turn it is
            return True

        else:
            return False

    def still_in(self, game_board):
        """
        Checks if each player is still in the game
        Returns False if the player who made the move broke their own last ring; returns True otherwise
        Changes game_state if the player who made the move breaks the other player's last ring
        """
        for row in range(3, 18):
            for column in range(3, 18):
                ring_check = Piece([row, column], game_board.get_game_board())
                if ring_check.is_ring():
                    return True
                else:
                    return False

        if check_piece(self._whose_turn):  # if the move didn't break the mover's own last ring
            print('here')
            if not check_piece(self._up_next):  # if the move broke the opponent's last ring

                # change game_state accordingly
                if self._whose_turn == "B":
                    self._game_state = "BLACK_WON"
                else:
                    self._game_state = "WHITE_WON"

            return True

        else:
            return False

'''
    def still_in(self, game_board):
        """
        Checks if each player is still in the game
        Returns False if the player who made the move broke their own last ring; returns True otherwise
        Changes game_state if the player who made the move breaks the other player's last ring
        """
        def check_piece(color):
            """
            Makes a temporary piece at each valid spot on the board
            Returns True if the perimeter of the piece is filled with the color of the piece
            Returns False if no piece has a full perimeter of the specified color
            """
            for row in range(3, 18):
                for column in range(3, 18):
                    ring_check = Piece([row, column], game_board.get_game_board())
                    if ring_check.is_ring():
                        return True
#                    perimeter_count = 0
 #                   for stone in ring_check.perimeter():
  #                      if stone == color:
   #                         perimeter_count += 1
    #                if perimeter_count == 8 and ring_check.get_piece_center() == ' ':
     #                   print(row, column)
      #                  print(ring_check.get_piece_center())
       #                 return True
                    else:
                        return False

        if check_piece(self._whose_turn):  # if the move didn't break the mover's own last ring
            print('here')
            if not check_piece(self._up_next):  # if the move broke the opponent's last ring

                # change game_state accordingly
                if self._whose_turn == "B":
                    self._game_state = "BLACK_WON"
                else:
                    self._game_state = "WHITE_WON"

            return True

        else:
            return False
'''

class Board:

    def __init__(self):
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
        return self._board

    def remove_piece(self, center_coordinates):

        # refactor center_coordinates to piece.getN

        self._board[center_coordinates[0]][center_coordinates[1]] = ' '
        self._board[center_coordinates[0]+1][center_coordinates[1]] = ' '
        self._board[center_coordinates[0]+1][center_coordinates[1]+1] = ' '
        self._board[center_coordinates[0]+1][center_coordinates[1]-1] = ' '
        self._board[center_coordinates[0]][center_coordinates[1]+1] = ' '
        self._board[center_coordinates[0]-1][center_coordinates[1]] = ' '
        self._board[center_coordinates[0]-1][center_coordinates[1]+1] = ' '
        self._board[center_coordinates[0]-1][center_coordinates[1]-1] = ' '
        self._board[center_coordinates[0]][center_coordinates[1]-1] = ' '

    def add_piece(self, piece, location):
        # if the center of the piece is being added to a valid spot on the board...
        if location[0] in range(2,20) and location[1] in range(2,20):
            self._board[location[0]][location[1]] = piece.get_piece_center()

            # then add the center, plus any part of the piece that is not off the board
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

    def __init__(self, middle, board):
        self._center = board[middle[0]][middle[1]]
        self._N = board[middle[0] - 1][middle[1]]
        self._NW = board[middle[0] - 1][middle[1] - 1]
        self._NE = board[middle[0] - 1][middle[1] + 1]
        self._S = board[middle[0] + 1][middle[1]]
        self._SW = board[middle[0] + 1][middle[1] - 1]
        self._SE = board[middle[0] + 1][middle[1] + 1]
        self._W = board[middle[0]][middle[1] - 1]
        self._E = board[middle[0]][middle[1] + 1]

        self._piece_matrix = [[self._NW, self._N, self._NE],
                              [self._W, self._center, self._E],
                              [self._SW, self._S, self._SE]]

    def perimeter(self):
        return [self._N, self._NW, self._NE, self._S, self._SW, self._SE, self._W, self._E]

    def get_piece_matrix(self):
        return self._piece_matrix

    def valid_piece(self, up_next):
        """
        Confirms that a piece does not have stones of the other player
        """
        if self._center == up_next:
            return False
        if up_next in self.perimeter():
            return False

        return True

    def is_empty(self):
        """
        Returns True if a piece has no stones
        Returns False if a piece has a stone
        """
        for row in self._piece_matrix:
            for space in row:
                if space != ' ':
                    return False

        return True

    def is_ring(self):
        if " " not in self.perimeter() and self._center == " ":
            return True
        else:
            return False

    def get_piece_center(self):
        return self._center

    def get_piece_N(self):
        return self._N

    def get_piece_NW(self):
        return self._NW

    def get_piece_NE(self):
        return self._NE

    def get_piece_S(self):
        return self._S

    def get_piece_SW(self):
        return self._SW

    def get_piece_SE(self):
        return self._SE

    def get_piece_W(self):
        return self._W

    def get_piece_E(self):
        return self._E


def display_board():
    for row in test.get_board().get_game_board():
        print(row)
    print()


test = GessGame()
print(test.make_move('i3', 'i6'))
display_board()
print(test._game_state)

thing = Piece([3,12], test.get_board().get_game_board())
print(thing.is_ring())
