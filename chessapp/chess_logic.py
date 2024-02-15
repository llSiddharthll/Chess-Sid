# chess/chess_logic.py
import chess
import chess.svg

class ChessLogic:
        
    def __init__(self):
        self.board = chess.Board()
        
    def get_initial_board_fen(self):
        # Return the FEN for the initial board position
        return self.get_board_state()
    
    def get_board_state(self):
        self.update_status()
        return self.board.fen()

    def set_board_state(self, fen):
        self.board.set_fen(fen)

    def make_move(self, move_uci):
        try:
            move = chess.Move.from_uci(move_uci)
            if move and move in self.board.legal_moves:
                self.board.push(move)
                self.update_status()
                print(self.board)  # Print after updating the status
                return True
            else:
                print(f"Invalid move: {move_uci}")
                return False
        except ValueError as e:
            print(f"Error parsing move: {e}")
            return False
    
    def update_status(self):
        status = ''

        move_color = 'White' if self.board.turn == chess.WHITE else 'Black'

        # checkmate?
        if self.board.is_checkmate():
            status = f'Game over, {move_color} is in checkmate.'
        # draw?
        elif self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_seventyfive_moves():
            status = 'Game over, drawn position'
        # game still on
        else:
            status = f'{move_color} to move'

            # check?
            if self.board.is_check():
                status += f', {move_color} is in check'

        # Include updating the board state in FEN format
        self.set_board_state(self.board.fen())

        return status

    def get_board_svg(self):
        return chess.svg.board(board=self.board)

    def get_possible_moves(self, square):
        possible_moves = []

        # Convert square to integer
        square_index = chess.SQUARE_NAMES.index(square)

        # Get the piece at the specified square
        piece = self.board.piece_at(square_index)

        # Check if the piece exists and is of the correct color
        if piece and piece.color == self.board.turn:
            # Get the legal moves for the piece
            legal_moves = self.board.legal_moves
            for move in legal_moves:
                if move.from_square == square_index:
                    # Convert the destination square back to alphanumeric form
                    destination_square = chess.SQUARE_NAMES[move.to_square]
                    possible_moves.append(destination_square)
        else:
            # Initialize possible_moves as an empty list if the piece condition is not satisfied
            possible_moves = []

        return possible_moves

    def on_drag_start(self, piece):
        # do not pick up pieces if the game is over
        if self.board.is_game_over():
            return False

        # Ensure piece is not None before calling lower()
        if piece and ((self.board.turn == chess.WHITE and piece.lower() == 'b') or
                      (self.board.turn == chess.BLACK and piece.lower() == 'w')):
            return False

    def on_drop(self, target):
        # Save the current board state
        current_board_state = self.board.copy()

        # Initialize move to None
        move = None

        # See if the move is legal
        if target == '0000':
            move = chess.Move.null()
        else:
            try:
                move = chess.Move.from_uci(target)
            except chess.InvalidMoveError as e:
                # Handle the case where the UCI is invalid
                return 'snapback'

        # Check if move is not None and is legal
        if move is not None and move in self.board.legal_moves:
            self.board.push(move)
            self.update_status()
            print(self.board)
            return None
        else:
            # Revert to the previous board state in case of an illegal move
            self.board = current_board_state
            return 'snapback'

    def on_snap_end(self):
        self.set_board_state(self.get_board_state())
