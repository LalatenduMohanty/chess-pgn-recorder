#!/usr/bin/env python3
"""
Chess PGN Recorder - Main Entry Point

Record chess games in Standard Algebraic Notation and export as PGN files.

Usage:
    python chess_pgn_recorder.py
    
Or make it executable and run directly:
    chmod +x chess_pgn_recorder.py
    ./chess_pgn_recorder.py
"""

from src.chess_pgn import main

if __name__ == '__main__':
    main()

