"""
Chess PGN Recorder

A command-line application that records chess games in Standard Algebraic Notation
and exports them as PGN files with full legal move validation.
"""

from .chess_pgn import ChessPGNApp, main
from .chess_game import ChessGame
from .move_validator import MoveValidator
from .pgn_exporter import PGNExporter

__all__ = ['ChessPGNApp', 'main', 'ChessGame', 'MoveValidator', 'PGNExporter']
__version__ = '0.1.0-alpha'

