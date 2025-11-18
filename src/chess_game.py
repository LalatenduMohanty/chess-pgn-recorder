"""
Chess Game Module

Manages chess game state, moves, and metadata.
Uses python-chess library for board state tracking and legal move validation.
"""

from typing import List, Tuple, Optional, Dict
import chess
from .move_validator import MoveValidator


class ChessGame:
    """Manages a chess game with moves and metadata using python-chess board."""

    def __init__(self, metadata: Dict[str, str]):
        """
        Initialize a chess game with metadata.

        Args:
            metadata: Dictionary containing game information (Event, Site, Date, etc.)
        """
        self.metadata = metadata
        self.moves: List[Tuple[str, Optional[str]]] = []
        self.result = metadata.get("Result", "*")
        self.validator = MoveValidator()
        self.board = chess.Board()
        self._pending_white_move: Optional[str] = None

    def add_move(self, white_move: Optional[str] = None, black_move: Optional[str] = None):
        """
        Add a move pair to the game.

        Args:
            white_move: White's move in algebraic notation
            black_move: Black's move in algebraic notation (can be None for incomplete pair)
        """
        if white_move is not None and black_move is not None:
            self.moves.append((white_move, black_move))
        elif white_move is not None:
            self.moves.append((white_move, None))

    def validate_and_add_move(self, move: str, color: str) -> Tuple[bool, str]:
        """
        Validate a move and add it to the game if valid.
        Checks both format (algebraic notation) and legality (chess rules).

        Args:
            move: The move string to validate and add
            color: 'white' or 'black'

        Returns:
            Tuple of (success, message)
        """
        is_valid_format, error_msg = self.validator.validate_move(move)

        if not is_valid_format:
            return False, error_msg

        expected_white_turn = self.board.turn == chess.WHITE
        is_white_move = color == "white"

        if expected_white_turn != is_white_move:
            expected_color = "White" if expected_white_turn else "Black"
            return False, f"It's {expected_color}'s turn to move"

        try:
            chess_move = self.board.parse_san(move)
            self.board.push(chess_move)
        except (chess.IllegalMoveError, chess.InvalidMoveError, chess.AmbiguousMoveError) as e:
            return False, f"Illegal move: {str(e)}"

        if color == "white":
            self._pending_white_move = move
        else:
            if self._pending_white_move is not None:
                self.add_move(self._pending_white_move, move)
                self._pending_white_move = None
            else:
                return False, "Cannot add black move without a white move first"

        return True, ""

    def finalize_pending_move(self):
        """Add any pending white move as an incomplete pair."""
        if self._pending_white_move is not None:
            self.add_move(self._pending_white_move, None)
            self._pending_white_move = None

    def edit_move(self, move_number: int, color: str, new_move: str) -> Tuple[bool, str]:
        """
        Edit a specific move in the game.
        Replays all moves from the start to validate the new move.

        Args:
            move_number: The move number (1-indexed)
            color: 'white' or 'black'
            new_move: The new move in algebraic notation

        Returns:
            Tuple of (success, message)
        """
        is_valid, error_msg = self.validator.validate_move(new_move)
        if not is_valid:
            return False, error_msg

        if move_number < 1 or move_number > len(self.moves):
            return False, f"Invalid move number: {move_number}"

        idx = move_number - 1
        white_move, black_move = self.moves[idx]

        if color == "black" and black_move is None:
            return False, "This move pair has no black move to edit"

        temp_moves = self.moves.copy()
        if color == "white":
            temp_moves[idx] = (new_move, black_move)
        else:
            temp_moves[idx] = (white_move, new_move)

        temp_board = chess.Board()
        try:
            for w_move, b_move in temp_moves:
                temp_board.push_san(w_move)
                if b_move:
                    temp_board.push_san(b_move)
        except (chess.IllegalMoveError, chess.InvalidMoveError, chess.AmbiguousMoveError):
            return False, "This edit would create an illegal position"

        self.moves = temp_moves
        self.board = temp_board

        return True, "Move updated successfully"

    def undo_last_move(self) -> bool:
        """
        Remove the last half-move entered.

        Returns:
            True if a move was removed, False if no moves to undo
        """
        if self._pending_white_move is not None:
            self.board.pop()
            self._pending_white_move = None
            return True

        if not self.moves:
            return False

        white_move, black_move = self.moves[-1]

        if black_move is not None:
            self.board.pop()
            self.moves[-1] = (white_move, None)
            self._pending_white_move = white_move
            self.moves.pop()
        else:
            self.board.pop()
            self.moves.pop()

        return True

    def get_move_count(self) -> int:
        """Return the number of complete move pairs."""
        return len(self.moves)

    def set_result(self, result: str):
        """
        Set the game result.

        Args:
            result: '1-0', '0-1', '1/2-1/2', or '*'
        """
        valid_results = ["1-0", "0-1", "1/2-1/2", "*"]
        if result in valid_results:
            self.result = result
            self.metadata["Result"] = result
        else:
            raise ValueError(f"Invalid result: {result}. Must be one of {valid_results}")

    def get_all_moves_display(self) -> str:
        """
        Return a formatted string of all moves for display.

        Returns:
            Formatted move list like:
            1. e4 e5
            2. Nf3 Nc6
        """
        if not self.moves:
            return "No moves yet"

        lines = []
        for i, (white_move, black_move) in enumerate(self.moves, 1):
            if black_move:
                lines.append(f"{i}. {white_move} {black_move}")
            else:
                lines.append(f"{i}. {white_move}")

        return "\n".join(lines)

    def get_moves_list(self) -> List[Tuple[str, Optional[str]]]:
        """Return the list of move pairs."""
        return self.moves.copy()

    def has_pending_white_move(self) -> bool:
        """Check if there's a pending white move not yet added to moves list."""
        return self._pending_white_move is not None

    def get_board_state(self) -> str:
        """
        Get current board state information.

        Returns:
            String with board status (check, checkmate, stalemate, etc.)
        """
        if self.board.is_checkmate():
            return "Checkmate!"
        elif self.board.is_stalemate():
            return "Stalemate"
        elif self.board.is_check():
            return "Check"
        elif self.board.is_insufficient_material():
            return "Draw (insufficient material)"
        elif self.board.is_fifty_moves():
            return "Draw available (50-move rule)"
        elif self.board.is_repetition():
            return "Draw available (threefold repetition)"
        return ""

    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.board.is_game_over()

    def get_legal_moves(self) -> List[str]:
        """
        Get list of legal moves in current position.

        Returns:
            List of legal moves in algebraic notation
        """
        return [self.board.san(move) for move in self.board.legal_moves]
