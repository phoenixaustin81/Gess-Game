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
        if location[0] in range(2,20) and location[1] in range(2,20):
            self._board[location[0]][location[1]] = piece.get_piece_center()

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


def display_piece():
    for row in footprint.get_piece_matrix():
        print(row)


test = GessGame()
footprint = Piece([3,3], test.get_board().get_game_board())
display_piece()
test.get_board().add_piece(footprint, [13,11])
display_board()
