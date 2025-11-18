"""
Unit Tests for Chess PGN Converter

Tests for MoveValidator, ChessGame, and PGNExporter classes.
Includes tests for board state tracking with python-chess integration.
"""

import unittest
import os
import sys
import tempfile
import chess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.move_validator import MoveValidator
from src.chess_game import ChessGame
from src.pgn_exporter import PGNExporter


class TestMoveValidator(unittest.TestCase):
    """Test cases for MoveValidator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = MoveValidator()
    
    def test_valid_pawn_moves(self):
        """Test valid pawn moves."""
        valid_moves = ['e4', 'd5', 'a6', 'h3', 'b7', 'c2']
        for move in valid_moves:
            is_valid, msg = self.validator.validate_move(move)
            self.assertTrue(is_valid, f"Move {move} should be valid")
    
    def test_valid_piece_moves(self):
        """Test valid piece moves."""
        valid_moves = ['Nf3', 'Bb5', 'Qd4', 'Ke2', 'Ra1', 'Bg5']
        for move in valid_moves:
            is_valid, msg = self.validator.validate_move(move)
            self.assertTrue(is_valid, f"Move {move} should be valid")
    
    def test_valid_captures(self):
        """Test valid capture notation."""
        valid_captures = ['exd5', 'Nxf6', 'Bxc4', 'Qxd8', 'Rxh1', 'axb6']
        for move in valid_captures:
            is_valid, msg = self.validator.validate_move(move)
            self.assertTrue(is_valid, f"Move {move} should be valid")
    
    def test_valid_castling(self):
        """Test valid castling notation."""
        valid_castling = ['O-O', 'O-O-O', 'O-O+', 'O-O-O#']
        for move in valid_castling:
            is_valid, msg = self.validator.validate_move(move)
            self.assertTrue(is_valid, f"Move {move} should be valid")
    
    def test_valid_promotions(self):
        """Test valid pawn promotion notation."""
        valid_promotions = ['e8=Q', 'a1=N', 'axb8=R', 'd1=B', 'e8=Q+', 'h1=Q#']
        for move in valid_promotions:
            is_valid, msg = self.validator.validate_move(move)
            self.assertTrue(is_valid, f"Move {move} should be valid")
    
    def test_valid_check_checkmate(self):
        """Test valid check and checkmate notation."""
        valid_moves = ['Nf7+', 'Qh5#', 'e8=Q+', 'Ra8#', 'O-O+']
        for move in valid_moves:
            is_valid, msg = self.validator.validate_move(move)
            self.assertTrue(is_valid, f"Move {move} should be valid")
    
    def test_valid_disambiguation(self):
        """Test valid disambiguation notation."""
        valid_moves = ['Nbd7', 'R1a3', 'Qh4e1', 'N5f3', 'Rae1']
        for move in valid_moves:
            is_valid, msg = self.validator.validate_move(move)
            self.assertTrue(is_valid, f"Move {move} should be valid")
    
    def test_invalid_rank(self):
        """Test invalid rank numbers."""
        invalid_moves = ['e9', 'a0', 'd10']
        for move in invalid_moves:
            is_valid, msg = self.validator.validate_move(move)
            self.assertFalse(is_valid, f"Move {move} should be invalid")
    
    def test_invalid_file(self):
        """Test invalid file letters."""
        invalid_moves = ['i4', 'z5', 'k4']  # k should be uppercase for king
        for move in invalid_moves:
            is_valid, msg = self.validator.validate_move(move)
            self.assertFalse(is_valid, f"Move {move} should be invalid")
    
    def test_lowercase_pieces(self):
        """Test that lowercase piece notation is rejected."""
        invalid_moves = ['nf3', 'bb5', 'qd4', 'ke2', 'ra1']
        for move in invalid_moves:
            is_valid, msg = self.validator.validate_move(move)
            self.assertFalse(is_valid, f"Move {move} should be invalid (lowercase)")
            self.assertIn("uppercase", msg.lower())
    
    def test_invalid_promotion_piece(self):
        """Test invalid promotion pieces."""
        invalid_moves = ['e8=K', 'a1=P', 'e8=X']
        for move in invalid_moves:
            is_valid, msg = self.validator.validate_move(move)
            self.assertFalse(is_valid, f"Move {move} should be invalid")
    
    def test_empty_move(self):
        """Test empty or whitespace-only moves."""
        invalid_moves = ['', '   ', '\t', '\n']
        for move in invalid_moves:
            is_valid, msg = self.validator.validate_move(move)
            self.assertFalse(is_valid, f"Empty move should be invalid")
    
    def test_is_castling(self):
        """Test castling detection."""
        self.assertTrue(self.validator.is_castling('O-O'))
        self.assertTrue(self.validator.is_castling('O-O-O'))
        self.assertFalse(self.validator.is_castling('e4'))
    
    def test_is_promotion(self):
        """Test promotion detection."""
        self.assertTrue(self.validator.is_promotion('e8=Q'))
        self.assertTrue(self.validator.is_promotion('axb8=N'))
        self.assertFalse(self.validator.is_promotion('e4'))
    
    def test_is_valid_square(self):
        """Test square validation."""
        self.assertTrue(self.validator.is_valid_square('e4'))
        self.assertTrue(self.validator.is_valid_square('a1'))
        self.assertTrue(self.validator.is_valid_square('h8'))
        self.assertFalse(self.validator.is_valid_square('i4'))
        self.assertFalse(self.validator.is_valid_square('e9'))
        self.assertFalse(self.validator.is_valid_square('e'))


class TestChessGame(unittest.TestCase):
    """Test cases for ChessGame class with board state tracking."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.metadata = {
            'Event': 'Test Game',
            'Site': 'Test',
            'Date': '2025.11.18',
            'Round': '1',
            'White': 'Player 1',
            'Black': 'Player 2',
            'Result': '*'
        }
        self.game = ChessGame(self.metadata)
    
    def test_initialization(self):
        """Test game initialization with chess board."""
        self.assertEqual(self.game.metadata, self.metadata)
        self.assertEqual(self.game.result, '*')
        self.assertEqual(len(self.game.moves), 0)
        self.assertIsInstance(self.game.board, chess.Board)
        self.assertEqual(self.game.board.fen(), chess.STARTING_FEN)
    
    def test_add_complete_move(self):
        """Test adding complete move pairs."""
        self.game.add_move('e4', 'e5')
        self.assertEqual(len(self.game.moves), 1)
        self.assertEqual(self.game.moves[0], ('e4', 'e5'))
    
    def test_add_incomplete_move(self):
        """Test adding incomplete move (white only)."""
        self.game.add_move('e4', None)
        self.assertEqual(len(self.game.moves), 1)
        self.assertEqual(self.game.moves[0], ('e4', None))
    
    def test_validate_and_add_legal_move(self):
        """Test validating and adding legal moves."""
        success, msg = self.game.validate_and_add_move('e4', 'white')
        self.assertTrue(success, f"e4 should be legal: {msg}")
        
        success, msg = self.game.validate_and_add_move('e5', 'black')
        self.assertTrue(success, f"e5 should be legal: {msg}")
        
        self.assertEqual(len(self.game.moves), 1)
        self.assertEqual(self.game.moves[0], ('e4', 'e5'))
    
    def test_validate_illegal_move(self):
        """Test that illegal moves are rejected."""
        self.game.validate_and_add_move('e4', 'white')
        
        success, msg = self.game.validate_and_add_move('e4', 'black')
        self.assertFalse(success)
        self.assertIn("Illegal", msg)
    
    def test_validate_invalid_format(self):
        """Test validating invalid format moves."""
        success, msg = self.game.validate_and_add_move('e9', 'white')
        self.assertFalse(success)
        self.assertIn("Invalid", msg)
    
    def test_turn_enforcement(self):
        """Test that turn order is enforced."""
        success, msg = self.game.validate_and_add_move('e4', 'black')
        self.assertFalse(success)
        self.assertIn("White's turn", msg)
    
    def test_edit_move_white(self):
        """Test editing white's move with board replay."""
        self.game.validate_and_add_move('e4', 'white')
        self.game.validate_and_add_move('e5', 'black')
        
        success, msg = self.game.edit_move(1, 'white', 'd4')
        self.assertTrue(success, f"Edit should succeed: {msg}")
        self.assertEqual(self.game.moves[0], ('d4', 'e5'))
    
    def test_edit_move_black(self):
        """Test editing black's move with board replay."""
        self.game.validate_and_add_move('e4', 'white')
        self.game.validate_and_add_move('e5', 'black')
        
        success, msg = self.game.edit_move(1, 'black', 'd5')
        self.assertTrue(success, f"Edit should succeed: {msg}")
        self.assertEqual(self.game.moves[0], ('e4', 'd5'))
    
    def test_edit_move_with_replay_validation(self):
        """Test that move editing properly replays and validates the game."""
        self.game.validate_and_add_move('e4', 'white')
        self.game.validate_and_add_move('e5', 'black')
        self.game.validate_and_add_move('Nf3', 'white')
        self.game.validate_and_add_move('Nc6', 'black')
        
        success, msg = self.game.edit_move(2, 'white', 'd4')
        self.assertTrue(success, f"Editing to d4 should be valid: {msg}")
        self.assertEqual(self.game.moves[1], ('d4', 'Nc6'))
    
    def test_edit_invalid_move_number(self):
        """Test editing with invalid move number."""
        self.game.add_move('e4', 'e5')
        success, msg = self.game.edit_move(10, 'white', 'd4')
        self.assertFalse(success)
    
    def test_undo_last_move(self):
        """Test undoing moves with board sync."""
        self.game.validate_and_add_move('e4', 'white')
        self.game.validate_and_add_move('e5', 'black')
        self.game.validate_and_add_move('Nf3', 'white')
        self.game.validate_and_add_move('Nc6', 'black')
        
        result = self.game.undo_last_move()
        self.assertTrue(result)
        self.assertEqual(len(self.game.moves), 1)
        self.assertTrue(self.game.board.turn == chess.BLACK)
    
    def test_set_result(self):
        """Test setting game result."""
        self.game.set_result('1-0')
        self.assertEqual(self.game.result, '1-0')
        self.assertEqual(self.game.metadata['Result'], '1-0')
    
    def test_set_invalid_result(self):
        """Test setting invalid result."""
        with self.assertRaises(ValueError):
            self.game.set_result('invalid')
    
    def test_get_move_count(self):
        """Test getting move count."""
        self.assertEqual(self.game.get_move_count(), 0)
        self.game.validate_and_add_move('e4', 'white')
        self.game.validate_and_add_move('e5', 'black')
        self.assertEqual(self.game.get_move_count(), 1)
        self.game.validate_and_add_move('Nf3', 'white')
        self.game.validate_and_add_move('Nc6', 'black')
        self.assertEqual(self.game.get_move_count(), 2)
    
    def test_get_all_moves_display(self):
        """Test getting formatted move display."""
        self.game.validate_and_add_move('e4', 'white')
        self.game.validate_and_add_move('e5', 'black')
        self.game.validate_and_add_move('Nf3', 'white')
        self.game.validate_and_add_move('Nc6', 'black')
        display = self.game.get_all_moves_display()
        self.assertIn('1. e4 e5', display)
        self.assertIn('2. Nf3 Nc6', display)
    
    def test_get_board_state_normal(self):
        """Test getting board state for normal position."""
        self.game.validate_and_add_move('e4', 'white')
        self.game.validate_and_add_move('e5', 'black')
        state = self.game.get_board_state()
        self.assertEqual(state, "")
    
    def test_get_board_state_check(self):
        """Test detecting check."""
        moves = ['e4', 'e5', 'Bc4', 'Nc6', 'Qh5', 'Nf6']
        for i, move in enumerate(moves):
            color = 'white' if i % 2 == 0 else 'black'
            self.game.validate_and_add_move(move, color)
        
        self.game.validate_and_add_move('Qxf7', 'white')
        state = self.game.get_board_state()
        self.assertIn('Check', state)
    
    def test_get_board_state_checkmate(self):
        """Test detecting checkmate (Scholar's Mate)."""
        moves = ['e4', 'e5', 'Bc4', 'Nc6', 'Qh5', 'Nf6', 'Qxf7']
        for i, move in enumerate(moves):
            color = 'white' if i % 2 == 0 else 'black'
            self.game.validate_and_add_move(move, color)
        
        state = self.game.get_board_state()
        self.assertEqual(state, "Checkmate!")
    
    def test_is_game_over(self):
        """Test game over detection."""
        self.assertFalse(self.game.is_game_over())
        
        moves = ['e4', 'e5', 'Bc4', 'Nc6', 'Qh5', 'Nf6', 'Qxf7']
        for i, move in enumerate(moves):
            color = 'white' if i % 2 == 0 else 'black'
            self.game.validate_and_add_move(move, color)
        
        self.assertTrue(self.game.is_game_over())
    
    def test_get_legal_moves(self):
        """Test getting legal moves."""
        legal_moves = self.game.get_legal_moves()
        self.assertIsInstance(legal_moves, list)
        self.assertIn('e4', legal_moves)
        self.assertIn('d4', legal_moves)
        self.assertIn('Nf3', legal_moves)
        self.assertEqual(len(legal_moves), 20)
        
        self.game.validate_and_add_move('e4', 'white')
        legal_moves = self.game.get_legal_moves()
        self.assertEqual(len(legal_moves), 20)


class TestPGNExporter(unittest.TestCase):
    """Test cases for PGNExporter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.exporter = PGNExporter()
        self.metadata = {
            'Event': 'Test Game',
            'Site': 'Test Site',
            'Date': '2025.11.18',
            'Round': '1',
            'White': 'Alice',
            'Black': 'Bob',
            'Result': '1-0'
        }
        self.game = ChessGame(self.metadata)
        self.game.add_move('e4', 'e5')
        self.game.add_move('Nf3', 'Nc6')
    
    def test_format_headers(self):
        """Test PGN header formatting."""
        headers = self.exporter.format_headers(self.metadata)
        self.assertIn('[Event "Test Game"]', headers)
        self.assertIn('[Site "Test Site"]', headers)
        self.assertIn('[White "Alice"]', headers)
        self.assertIn('[Black "Bob"]', headers)
    
    def test_format_moves(self):
        """Test move formatting."""
        moves = [('e4', 'e5'), ('Nf3', 'Nc6')]
        formatted = self.exporter.format_moves(moves, '1-0')
        self.assertIn('1. e4 e5', formatted)
        self.assertIn('2. Nf3 Nc6', formatted)
        self.assertIn('1-0', formatted)
    
    def test_format_incomplete_moves(self):
        """Test formatting with incomplete last move."""
        moves = [('e4', 'e5'), ('Nf3', None)]
        formatted = self.exporter.format_moves(moves, '*')
        self.assertIn('1. e4 e5', formatted)
        self.assertIn('2. Nf3', formatted)
    
    def test_generate_pgn_string(self):
        """Test complete PGN string generation."""
        pgn = self.exporter.generate_pgn_string(self.game)
        self.assertIn('[Event "Test Game"]', pgn)
        self.assertIn('1. e4 e5', pgn)
        self.assertIn('2. Nf3 Nc6', pgn)
    
    def test_generate_filename(self):
        """Test filename generation."""
        filename = self.exporter.generate_filename(self.metadata)
        self.assertEqual(filename, 'Alice_Bob_2025.11.18_1.pgn')
    
    def test_generate_filename_with_spaces(self):
        """Test filename generation with spaces in names."""
        metadata = self.metadata.copy()
        metadata['White'] = 'Alice Smith'
        metadata['Black'] = 'Bob Jones'
        filename = self.exporter.generate_filename(metadata)
        self.assertEqual(filename, 'Alice_Smith_Bob_Jones_2025.11.18_1.pgn')
    
    def test_export_to_file(self):
        """Test exporting to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = self.exporter.export_to_file(self.game, directory=tmpdir)
            self.assertTrue(os.path.exists(filepath))
            
            with open(filepath, 'r') as f:
                content = f.read()
                self.assertIn('[Event "Test Game"]', content)
                self.assertIn('1. e4 e5', content)
    
    def test_unique_filename(self):
        """Test that duplicate filenames get numbered."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath1 = self.exporter.export_to_file(self.game, directory=tmpdir)
            filepath2 = self.exporter.export_to_file(self.game, directory=tmpdir)
            
            self.assertNotEqual(filepath1, filepath2)
            self.assertTrue(os.path.exists(filepath1))
            self.assertTrue(os.path.exists(filepath2))


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflow with board state tracking."""
    
    def test_complete_game_workflow(self):
        """Test a complete game from start to finish with legal moves."""
        metadata = {
            'Event': 'Integration Test',
            'Site': 'Test Suite',
            'Date': '2025.11.18',
            'Round': '1',
            'White': 'Alice',
            'Black': 'Bob',
            'Result': '*'
        }
        
        game = ChessGame(metadata)
        
        moves = [
            ('e4', 'white'),
            ('e5', 'black'),
            ('Nf3', 'white'),
            ('Nc6', 'black'),
            ('Bb5', 'white'),
            ('a6', 'black'),
            ('Ba4', 'white'),
            ('Nf6', 'black'),
            ('O-O', 'white'),
            ('Nxe4', 'black')
        ]
        
        for move, color in moves:
            success, msg = game.validate_and_add_move(move, color)
            self.assertTrue(success, f"Move {move} should be legal: {msg}")
        
        game.set_result('1-0')
        
        exporter = PGNExporter()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = exporter.export_to_file(game, directory=tmpdir)
            
            self.assertTrue(os.path.exists(filepath))
            
            with open(filepath, 'r') as f:
                content = f.read()
                
                self.assertIn('[Event "Integration Test"]', content)
                self.assertIn('[Result "1-0"]', content)
                
                self.assertIn('1. e4 e5', content)
                self.assertIn('5. O-O Nxe4', content)
                self.assertIn('1-0', content)
    
    def test_checkmate_game(self):
        """Test a complete game ending in checkmate (Scholar's Mate)."""
        metadata = {
            'Event': 'Checkmate Test',
            'Site': 'Test Suite',
            'Date': '2025.11.18',
            'Round': '1',
            'White': 'Alice',
            'Black': 'Bob',
            'Result': '1-0'
        }
        
        game = ChessGame(metadata)
        
        moves = [
            ('e4', 'white'),
            ('e5', 'black'),
            ('Bc4', 'white'),
            ('Nc6', 'black'),
            ('Qh5', 'white'),
            ('Nf6', 'black'),
            ('Qxf7', 'white')
        ]
        
        for move, color in moves:
            success, msg = game.validate_and_add_move(move, color)
            self.assertTrue(success, f"Move {move} should be legal: {msg}")
        
        game.finalize_pending_move()
        
        self.assertTrue(game.is_game_over())
        self.assertEqual(game.get_board_state(), "Checkmate!")
        
        exporter = PGNExporter()
        pgn = exporter.generate_pgn_string(game)
        
        self.assertIn('1. e4 e5', pgn)
        self.assertIn('4. Qxf7', pgn)


if __name__ == '__main__':
    unittest.main()

