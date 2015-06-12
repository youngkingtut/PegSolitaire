from gameconfig import GameConfig


class Puzzle(object):
    EMPTY = 0
    OCCUPIED = 1

    def __init__(self, pieces=set()):
        self.positions = {}
        self.pieces = pieces
        self.init_blank_puzzle()
        self.create_puzzle()

    def init_blank_puzzle(self):
        max_grid_radius = int(GameConfig.GAME_GRID_SIZE)
        for r in range(max_grid_radius + 1):
            for x in range(-r, r + 1):
                for y in range(-r, r + 1):
                    if (x ** 2 + y ** 2) ** 0.5 < 13 ** 0.5:
                        self.positions[(x, y)] = Puzzle.EMPTY

    def create_puzzle(self):
        if not self.pieces:
            for position in self.positions:
                self.add_piece(position)
            self.remove_piece((0, 0))

        else:
            for piece in self.pieces:
                self.positions[piece] = Puzzle.OCCUPIED

    def add_piece(self, position):
        self.positions[position] = Puzzle.OCCUPIED
        self.pieces.add(position)

    def remove_piece(self, position):
        self.positions[position] = Puzzle.EMPTY
        self.pieces.remove(position)

    def valid_moves(self, piece):
        assert self.positions.get(piece, None) == Puzzle.OCCUPIED
        x, y = piece
        valid_moves = []
        if self.positions.get((x + 1, y), None) == Puzzle.OCCUPIED:
            if self.positions.get((x + 2, y), None) == Puzzle.EMPTY:
                valid_moves.append((x + 2, y))
        if self.positions.get((x - 1, y), None) == Puzzle.OCCUPIED:
            if self.positions.get((x - 2, y), None) == Puzzle.EMPTY:
                valid_moves.append((x - 2, y))
        if self.positions.get((x, y + 1), None) == Puzzle.OCCUPIED:
            if self.positions.get((x, y + 2), None) == Puzzle.EMPTY:
                valid_moves.append((x, y + 2))
        if self.positions.get((x, y - 1), None) == Puzzle.OCCUPIED:
            if self.positions.get((x, y - 2), None) == Puzzle.EMPTY:
                valid_moves.append((x, y - 2))

        return valid_moves

    def move_piece(self, piece, new_position):
        self.remove_piece(piece)
        self.add_piece(new_position)

        def get_middle_coord(a, b):
            return a + (b - a) / 2

        self.remove_piece(tuple(map(get_middle_coord, piece, new_position)))

    def clear_puzzle(self):
        for piece in self.pieces:
            self.remove_piece(piece)
