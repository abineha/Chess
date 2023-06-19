import matplotlib.pyplot as plt

class KnightTour:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = [[-1 for _ in range(board_size)] for _ in range(board_size)]
        self.moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]

    def is_valid_move(self, x, y):
        if 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[x][y] == -1:
            return True
        return False

    def solve(self):
        self.board[0][0] = 0
        if self.solve_util(0, 0, 1):
            self.plot_solution()
        else:
            print("No solution found.")

    def solve_util(self, x, y, move_number):
        if move_number == self.board_size ** 2:
            return True

        for move in self.moves:
            next_x = x + move[0]
            next_y = y + move[1]

            if self.is_valid_move(next_x, next_y):
                self.board[next_x][next_y] = move_number
                if self.solve_util(next_x, next_y, move_number + 1):
                    return True
                self.board[next_x][next_y] = -1  # Backtracking

        return False

    def plot_solution(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.axis('off')

        for row in range(self.board_size):
            for col in range(self.board_size):
                ax.text(col, row, str(self.board[row][col]), va='center', ha='center', fontsize=10, fontweight='bold')
                ax.plot(col + 0.5, row + 0.5, 'ko', markersize=10)

        for row in range(self.board_size):
            for col in range(self.board_size):
                for move in self.moves:
                    next_x = row + move[0]
                    next_y = col + move[1]
                    if self.is_valid_move(next_x, next_y):
                        ax.plot([col + 0.5, next_y + 0.5], [row + 0.5, next_x + 0.5], 'b-')

        plt.show()



class QueenMovesGraph:
    def __init__(self, board_size):
        self.board_size = board_size

    def generate_moves(self):
        moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                for i in range(self.board_size):
                    if i != col:
                        moves.append(((row, col), (row, i)))  # Horizontal moves
                        moves.append(((col, row), (i, row)))  # Vertical moves
                        diag_row = row + (i - col)
                        if 0 <= diag_row < self.board_size:
                            moves.append(((row, col), (diag_row, i)))  # Diagonal moves
                        diag_row = row - (i - col)
                        if 0 <= diag_row < self.board_size:
                            moves.append(((row, col), (diag_row, i)))  # Diagonal moves
        return moves

    def plot_moves(self):
        moves = self.generate_moves()

        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.axis('off')

        for move in moves:
            start, end = move
            ax.plot([start[1] + 0.5, end[1] + 0.5], [start[0] + 0.5, end[0] + 0.5], 'b-')

        plt.xlim([-0.5, self.board_size - 0.5])
        plt.ylim([-0.5, self.board_size - 0.5])
        plt.show()


class KingMovesGraph:
    def __init__(self, board_size):
        self.board_size = board_size

    def generate_moves(self):
        moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        next_row = row + i
                        next_col = col + j
                        if 0 <= next_row < self.board_size and 0 <= next_col < self.board_size:
                            moves.append(((row, col), (next_row, next_col)))
        return moves

    def plot_moves(self):
        moves = self.generate_moves()

        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.axis('off')

        for move in moves:
            start, end = move
            ax.plot([start[1] + 0.5, end[1] + 0.5], [start[0] + 0.5, end[0] + 0.5], 'b-')

        plt.xlim([-0.5, self.board_size - 0.5])
        plt.ylim([-0.5, self.board_size - 0.5])
        plt.show()



class PawnMovesGraph:
    def __init__(self, board_size):
        self.board_size = board_size

    def generate_moves(self):
        moves = []
        for col in range(self.board_size):
            moves.append(((1, col), (2, col)))  # Initial double move
            moves.append(((self.board_size - 2, col), (self.board_size - 3, col)))  # Initial double move for black pawns

            moves.append(((1, col), (1, col + 1)))  # Capture move to the right
            moves.append(((1, col), (1, col - 1)))  # Capture move to the left
            moves.append(((self.board_size - 2, col), (self.board_size - 2, col + 1)))  # Capture move to the right for black pawns
            moves.append(((self.board_size - 2, col), (self.board_size - 2, col - 1)))  # Capture move to the left for black pawns
        return moves

    def plot_moves(self):
        moves = self.generate_moves()

        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.axis('off')

        for move in moves:
            start, end = move
            ax.plot([start[1] + 0.5, end[1] + 0.5], [start[0] + 0.5, end[0] + 0.5], 'b-')

        plt.xlim([-0.5, self.board_size - 0.5])
        plt.ylim([-0.5, self.board_size - 0.5])
        plt.show()



class RookMovesGraph:
    def __init__(self, board_size):
        self.board_size = board_size

    def generate_moves(self):
        moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                for i in range(self.board_size):
                    if i != row:
                        moves.append(((row, col), (i, col)))  # Vertical moves
                        moves.append(((col, row), (col, i)))  # Horizontal moves
        return moves

    def plot_moves(self):
        moves = self.generate_moves()

        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.axis('off')

        for move in moves:
            start, end = move
            ax.plot([start[1] + 0.5, end[1] + 0.5], [start[0] + 0.5, end[0] + 0.5], 'b-')

        plt.xlim([-0.5, self.board_size - 0.5])
        plt.ylim([-0.5, self.board_size - 0.5])
        plt.show()




class BishopMovesGraph:
    def __init__(self, board_size):
        self.board_size = board_size

    def generate_moves(self):
        moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                for i in range(self.board_size):
                    if i != row:
                        diag_row = i
                        diag_col = col + (i - row)
                        if 0 <= diag_row < self.board_size and 0 <= diag_col < self.board_size:
                            moves.append(((row, col), (diag_row, diag_col)))  # Diagonal moves

                        diag_row = i
                        diag_col = col - (i - row)
                        if 0 <= diag_row < self.board_size and 0 <= diag_col < self.board_size:
                            moves.append(((row, col), (diag_row, diag_col)))  # Diagonal moves
        return moves

    def plot_moves(self):
        moves = self.generate_moves()

        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.axis('off')

        for move in moves:
            start, end = move
            ax.plot([start[1] + 0.5, end[1] + 0.5], [start[0] + 0.5, end[0] + 0.5], 'b-')

        plt.xlim([-0.5, self.board_size - 0.5])
        plt.ylim([-0.5, self.board_size - 0.5])
        plt.show()






def fun():
    board_size = 8  # 8x8 chessboard
    print('hello')
    knight_tour = KnightTour(board_size)
    knight_tour.solve()
    queen_moves_graph = QueenMovesGraph(board_size)
    queen_moves_graph.plot_moves()
    king_moves_graph = KingMovesGraph(board_size)
    king_moves_graph.plot_moves()
    pawn_moves_graph = PawnMovesGraph(board_size)
    pawn_moves_graph.plot_moves()
    rook_moves_graph = RookMovesGraph(board_size)
    rook_moves_graph.plot_moves()
    print('bishop')
    bishop_moves_graph = BishopMovesGraph(board_size)
    bishop_moves_graph.plot_moves()
