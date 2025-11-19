"""
Move Validator Module

Validates chess moves in Standard Algebraic Notation (SAN).
Supports all standard move types including pieces, pawns, captures,
castling, and promotions.
"""

import re
from typing import Tuple


class MoveValidator:
    """Validates chess moves in algebraic notation.

    Regex patterns cover: castling, pawn moves, pawn captures,
    pawn promotions, and piece moves with disambiguation.
    """

    CASTLING = r"^O-O(-O)?[+#]?[!?]*$"
    PAWN_PROMOTION = r"^[a-h]?x?[a-h][18]=[QRBN][+#]?[!?]*$"
    PAWN_CAPTURE = r"^[a-h]x[a-h][1-8][+#]?[!?]*$"
    PAWN_MOVE = r"^[a-h][1-8][+#]?[!?]*$"
    PIECE_MOVE = r"^[KQRBN][a-h]?[1-8]?x?[a-h][1-8][+#]?[!?]*$"

    def __init__(self):
        """Initialize the MoveValidator with compiled regex patterns."""
        self.patterns = {
            "castling": re.compile(self.CASTLING),
            "promotion": re.compile(self.PAWN_PROMOTION),
            "pawn_capture": re.compile(self.PAWN_CAPTURE),
            "pawn_move": re.compile(self.PAWN_MOVE),
            "piece_move": re.compile(self.PIECE_MOVE),
        }

    def validate_move(self, move: str) -> Tuple[bool, str]:
        """
        Validate a chess move in algebraic notation.

        Args:
            move: The move string to validate

        Returns:
            Tuple of (is_valid, error_message)
            If valid: (True, "")
            If invalid: (False, "error message")
        """
        if not move or not move.strip():
            return False, "Move cannot be empty"

        move = move.strip()

        if len(move) > 0 and move[0] in "kqrbn":
            if not (len(move) == 2 and move[1] in "12345678"):
                piece_upper = move[0].upper()
                return (
                    False,
                    f"Piece notation must be uppercase (use '{piece_upper}{move[1:]}' instead of '{move}')",
                )

        rank_matches = re.findall(r"[0-9]", move)
        for rank in rank_matches:
            if rank not in "12345678":
                return False, f"Invalid rank '{rank}': ranks must be 1-8"

        file_pattern = re.findall(r"[a-z]", move)
        for potential_file in file_pattern:
            if potential_file not in "abcdefgh":
                if potential_file not in "xkqrbn":
                    return False, f"Invalid character '{potential_file}' in move"

        if "=" in move:
            promo_match = re.search(r"=([A-Z])", move)
            if promo_match:
                promo_piece = promo_match.group(1)
                if promo_piece not in "QRBN":
                    return (
                        False,
                        f"Invalid promotion piece '{promo_piece}': can only promote to Q, R, B, or N",
                    )
            else:
                return False, "Invalid promotion format: use '=Q', '=R', '=B', or '=N'"

        for pattern_name, pattern in self.patterns.items():
            if pattern.match(move):
                return True, ""

        return False, self._generate_error_message(move)

    def _generate_error_message(self, move: str) -> str:
        """
        Generate a helpful error message for an invalid move.

        Args:
            move: The invalid move string

        Returns:
            A descriptive error message
        """
        if move.lower().startswith("o-o"):
            return "Invalid castling notation: use 'O-O' (kingside) or 'O-O-O' (queenside) with capital letter O"

        if "=" in move:
            return "Invalid promotion format: examples - e8=Q, axb8=N, d1=R+"

        if "x" in move and len(move) >= 3:
            return "Invalid capture notation: examples - exd5, Nxf6, Bxc4"

        return (
            f"Invalid move format: '{move}'\n"
            "Valid examples:\n"
            "  - Pawn moves: e4, d5\n"
            "  - Piece moves: Nf3, Bb5, Qd4\n"
            "  - Captures: exd5, Nxf6\n"
            "  - Castling: O-O, O-O-O\n"
            "  - Promotion: e8=Q, axb8=N\n"
            "  - Check/Checkmate: Nf7+, Qh5#"
        )

    def is_castling(self, move: str) -> bool:
        """Check if a move is castling notation."""
        return self.patterns["castling"].match(move.strip()) is not None

    def is_promotion(self, move: str) -> bool:
        """Check if a move is a pawn promotion."""
        return self.patterns["promotion"].match(move.strip()) is not None

    def is_valid_piece(self, piece: str) -> bool:
        """Check if a character is a valid piece notation."""
        return piece in "KQRBN"

    def is_valid_square(self, square: str) -> bool:
        """
        Check if a string represents a valid board square.

        Args:
            square: String like 'e4', 'a1', etc.

        Returns:
            True if valid square (a-h, 1-8), False otherwise
        """
        if len(square) != 2:
            return False

        file, rank = square[0], square[1]
        return file in "abcdefgh" and rank in "12345678"
