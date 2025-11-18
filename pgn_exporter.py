"""
PGN Exporter Module

Generates PGN (Portable Game Notation) format output from chess games.
"""

import os
from typing import List, Tuple, Optional
from chess_game import ChessGame


class PGNExporter:
    """Exports chess games to PGN format."""
    
    REQUIRED_HEADERS = ['Event', 'Site', 'Date', 'Round', 'White', 'Black', 'Result']
    
    def __init__(self):
        """Initialize the PGN exporter."""
        pass
    
    def format_headers(self, metadata: dict) -> str:
        """
        Format PGN headers from metadata dictionary.
        
        Args:
            metadata: Dictionary with game metadata
            
        Returns:
            Formatted header string with each header on its own line
        """
        headers = []
        
        for header in self.REQUIRED_HEADERS:
            value = metadata.get(header, '?')
            headers.append(f'[{header} "{value}"]')
        
        return '\n'.join(headers)
    
    def format_moves(self, moves: List[Tuple[str, Optional[str]]], result: str) -> str:
        """
        Format moves in PGN format with one move pair per line.
        
        Args:
            moves: List of (white_move, black_move) tuples
            result: Game result ('1-0', '0-1', '1/2-1/2', or '*')
            
        Returns:
            Formatted move text with result
        """
        if not moves:
            return result
        
        lines = []
        for i, (white_move, black_move) in enumerate(moves, 1):
            if black_move:
                lines.append(f"{i}. {white_move} {black_move} ")
            else:
                lines.append(f"{i}. {white_move} ")
        
        lines.append(result)
        
        return '\n'.join(lines)
    
    def generate_pgn_string(self, game: ChessGame) -> str:
        """
        Generate complete PGN string from a chess game.
        
        Args:
            game: ChessGame object
            
        Returns:
            Complete PGN formatted string
        """
        headers = self.format_headers(game.metadata)
        moves = self.format_moves(game.get_moves_list(), game.result)
        
        return f"{headers}\n\n{moves}\n"
    
    def preview_pgn(self, game: ChessGame) -> str:
        """
        Generate PGN preview string with decorative borders.
        
        Args:
            game: ChessGame object
            
        Returns:
            PGN string with preview borders
        """
        pgn_content = self.generate_pgn_string(game)
        
        border = "=" * 50
        preview = f"\n{border}\n{pgn_content}{border}\n"
        
        return preview
    
    def generate_filename(self, metadata: dict) -> str:
        """
        Generate filename from metadata.
        
        Format: white_black_date_round.pgn
        Example: Alice_Bob_2025.11.18_1.pgn
        
        Args:
            metadata: Dictionary with game metadata
            
        Returns:
            Generated filename
        """
        white = metadata.get('White', 'Player1').replace(' ', '_')
        black = metadata.get('Black', 'Player2').replace(' ', '_')
        date = metadata.get('Date', '0000.00.00')
        round_num = metadata.get('Round', '1')
        
        filename = f"{white}_{black}_{date}_{round_num}.pgn"
        
        return filename
    
    def ensure_unique_filename(self, filename: str, directory: str = '.') -> str:
        """
        Ensure filename is unique by appending number if file exists.
        
        Args:
            filename: Proposed filename
            directory: Directory to check in
            
        Returns:
            Unique filename
        """
        filepath = os.path.join(directory, filename)
        
        if not os.path.exists(filepath):
            return filename
        
        base_name = filename[:-4]
        counter = 2
        
        while True:
            new_filename = f"{base_name}_{counter}.pgn"
            new_filepath = os.path.join(directory, new_filename)
            
            if not os.path.exists(new_filepath):
                return new_filename
            
            counter += 1
    
    def export_to_file(self, game: ChessGame, filename: Optional[str] = None, 
                       directory: str = '.') -> str:
        """
        Export game to PGN file.
        
        Args:
            game: ChessGame object to export
            filename: Optional custom filename (if None, auto-generate)
            directory: Directory to save file in
            
        Returns:
            Path to the saved file
        """
        if filename is None:
            filename = self.generate_filename(game.metadata)
        
        if not filename.endswith('.pgn'):
            filename += '.pgn'
        
        filename = self.ensure_unique_filename(filename, directory)
        pgn_content = self.generate_pgn_string(game)
        
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(pgn_content)
        
        return filepath

