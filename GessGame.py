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
        if start[0] > 19 or start [0] < 1 or start[1] > 20 or start[1] < 1:
            return False
        if end[0] > 19 or end[0] < 1 or end[1] > 20 or end[1] < 1:
            return False

        # if the piece has stones of the opponent
        check_piece = Piece(start, self._board.get_game_board())
        if not check_piece.valid_piece(self._up_next):
            return False

        return self.valid_direction(start, end)

        return True

    def coordinate_conversion(self, position):
        """
        Converts a game-board position to a list with corresponding indices list[x][x]
        Example: 'd16' to  [5,4], which is list[5][4]
        """
        return [21 - int(position[1:]), ord(position[0]) - 96]

    def valid_direction(self, start, end):
        piece_start = Piece(start, self._board.get_game_board())
        piece_end = Piece(end, self._board.get_game_board())

        # is the piece moving southward?
        if end[0] > start[0]:

            # is the piece moving southeast?
            if end[1] > start[1]:

                # is the move truly diagonal?
                if abs(end[0] - start[0]) == abs(end[1] - start[1]):

                    # is there a stone in the SE position of the piece?
                    if piece_start.get_piece_SE() == self._whose_turn:
                        self._direction = [1, 1]  # set the direction of the move
                        return True

            # repeat of the above for a southwest move
            elif end[1] < start[1]:
                if abs(end[0] - start[0]) == abs(end[1] - start[1]):
                    if piece_start.get_piece_SW() == self._whose_turn:
                        self._direction = [1, -1]  # set the direction of the move
                        return True

            # must be direct south movement
            else:
                if piece_start.get_piece_S() == self._whose_turn:
                    self._direction = [1, 0]  # set the direction of the move
                    return True

        # is the piece moving northward?
        elif end[0] < start[0]:

            # is the piece moving northeast?
            if end[1] > start[1]:

                # is the move truly diagonal?
                if abs(end[0] - start[0]) == abs(end[1] - start[1]):

                    # is there a stone in the NE position of the piece?
                    if piece_start.get_piece_NE() == self._whose_turn:
                        self._direction = [-1, 1]  # set the direction of the move
                        return True

            # repeat of the above for a northwest move
            elif end[1] < start[1]:
                if abs(end[0] - start[0]) == abs(end[1] - start[1]):
                    if piece_start.get_piece_NW() == self._whose_turn:
                        self._direction = [-1, -1]  # set the direction of the move
                        return True

            # must be direct north movement
            else:
                if piece_start.get_piece_N() == self._whose_turn:
                    self._direction = [-1, 0]  # set the direction of the move
                    return True

        # direct east move?
        elif end[0] == start[0] and end[1] > start[1]:
            if piece_start.get_piece_E() == self._whose_turn:  # stone in the east position?
                self._direction = [0, 1]  # set direction of the move
                return True

        # direct west move?
        elif end[0] == start[0] and end[1] < start[1]:
            if piece_start.get_piece_W() == self._whose_turn:  # stone in the west position?
                self._direction = [0, -1]  # set direction of the move
                return True

        return False  # not a valid direction of movement

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
footprint = Piece([3,3], test.get_board().get_game_board())
test.get_board().add_piece(footprint, [13,11])
display_board()


print(test.make_move('b6', 'd8'))