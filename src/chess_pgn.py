#!/usr/bin/env python3
"""
Chess Notation to PGN Converter

A command-line application that captures chess moves in Standard Algebraic 
Notation (SAN) and exports them as a valid PGN (Portable Game Notation) file.
"""

from datetime import date
from .chess_game import ChessGame
from .pgn_exporter import PGNExporter
from .move_validator import MoveValidator


class ChessPGNApp:
    """Main application for chess PGN converter."""
    
    def __init__(self):
        """Initialize the application."""
        self.game = None
        self.exporter = PGNExporter()
        self.validator = MoveValidator()
    
    def print_welcome(self):
        """Print welcome message."""
        print("\n" + "=" * 60)
        print("   Chess Notation to PGN Converter")
        print("=" * 60)
        print("\nConvert your chess game moves to PGN format!")
        print("Type 'help' for commands | Type 'done' to finish at any time\n")
    
    def print_help(self):
        """Print help message with available commands and notation examples."""
        print("\n" + "-" * 60)
        print("AVAILABLE COMMANDS:")
        print("-" * 60)
        print("  quit/exit/done - End game and save")
        print("  undo           - Remove last move")
        print("  show           - Display all moves entered")
        print("  preview        - Show PGN preview")
        print("  help           - Display this help message")
        print("\n" + "-" * 60)
        print("VALID MOVE NOTATION:")
        print("-" * 60)
        print("  Pawn moves:     e4, d5, a6")
        print("  Piece moves:    Nf3, Bb5, Qd4, Ke2, Ra1")
        print("  Captures:       exd5, Nxf6, Bxc4")
        print("  Castling:       O-O (kingside), O-O-O (queenside)")
        print("  Promotion:      e8=Q, axb8=N")
        print("  Check:          Nf7+, Qh5+")
        print("  Checkmate:      Qh5#")
        print("  Disambiguation: Nbd7, R1a3")
        print("\nNOTE: Only legal moves are accepted!")
        print("-" * 60 + "\n")
    
    def collect_metadata(self) -> dict:
        """
        Collect game metadata from user.
        
        Returns:
            Dictionary with game metadata
        """
        print("Enter game information:\n")
        
        event = input("Event [Casual Game]: ").strip()
        if not event:
            event = "Casual Game"
        
        site = input("Site [Local]: ").strip()
        if not site:
            site = "Local"
        
        date_str = input(f"Date (YYYY.MM.DD) [press Enter for today]: ").strip()
        if not date_str:
            today = date.today()
            date_str = f"{today.year}.{today.month:02d}.{today.day:02d}"
        
        round_num = input("Round [1]: ").strip()
        if not round_num:
            round_num = "1"
        
        white = input("White player: ").strip()
        if not white:
            white = "Player 1"
        
        black = input("Black player: ").strip()
        if not black:
            black = "Player 2"
        
        metadata = {
            'Event': event,
            'Site': site,
            'Date': date_str,
            'Round': round_num,
            'White': white,
            'Black': black,
            'Result': '*'
        }
        
        return metadata
    
    def handle_command(self, command: str) -> str:
        """
        Handle special commands during move entry.
        
        Args:
            command: The command string
            
        Returns:
            'continue' to continue game, 'quit' to end game
        """
        command = command.lower().strip()
        
        if command in ['quit', 'exit', 'done']:
            return 'quit'
        
        elif command == 'undo':
            if self.game.undo_last_move():
                print("✓ Last move removed")
            else:
                print("✗ No moves to undo")
        
        elif command == 'show':
            print("\nCurrent moves:")
            print(self.game.get_all_moves_display())
            print()
        
        elif command == 'preview':
            print(self.exporter.preview_pgn(self.game))
        
        elif command == 'legal':
            legal_moves = self.game.get_legal_moves()
            print(f"\nLegal moves ({len(legal_moves)}):")
            print(", ".join(sorted(legal_moves)))
            print()
        
        elif command == 'help':
            self.print_help()
        
        else:
            print(f"Unknown command: {command}. Type 'help' for command list.")
        
        return 'continue'
    
    def get_move_input(self, color: str, move_number: int) -> str:
        """
        Get move input from user with prompt.
        
        Args:
            color: 'white' or 'black'
            move_number: Current move number
            
        Returns:
            The move string or command
        """
        if color == 'white':
            prompt = f"\nMove {move_number}\nWhite's move: "
        else:
            prompt = f"Black's move: "
        
        return input(prompt).strip()
    
    def enter_moves(self):
        """Main loop for entering moves."""
        move_number = 1
        
        while True:
            while True:
                white_input = self.get_move_input('white', move_number)
                
                if white_input.lower() in ['quit', 'exit', 'done', 'undo', 'show', 'preview', 'legal', 'help']:
                    result = self.handle_command(white_input)
                    if result == 'quit':
                        self.game.finalize_pending_move()
                        return
                    continue
                
                success, message = self.game.validate_and_add_move(white_input, 'white')
                if not success:
                    print(f"✗ Invalid move: {message}")
                    continue
                
                break
            
            print(f"\033[A\033[KWhite's move: {white_input} ✓")
            
            board_state = self.game.get_board_state()
            if board_state:
                print(f"  {board_state}")
            
            if self.game.is_game_over():
                break
            
            while True:
                black_input = self.get_move_input('black', move_number)
                
                if black_input.lower() in ['quit', 'exit', 'done', 'undo', 'show', 'preview', 'legal', 'help']:
                    result = self.handle_command(black_input)
                    if result == 'quit':
                        self.game.finalize_pending_move()
                        return
                    continue
                
                success, message = self.game.validate_and_add_move(black_input, 'black')
                if not success:
                    print(f"✗ Invalid move: {message}")
                    continue
                
                break
            
            print(f"\033[A\033[KBlack's move: {black_input} ✓")
            
            board_state = self.game.get_board_state()
            if board_state:
                print(f"  {board_state}")
            
            if self.game.is_game_over():
                break
            
            move_number += 1
        
        self.game.finalize_pending_move()
    
    def get_result(self) -> str:
        """
        Get game result from user.
        
        Returns:
            Result string ('1-0', '0-1', '1/2-1/2', or '*')
        """
        print("\nGame ended. Enter result:")
        print("  1-0       White wins")
        print("  0-1       Black wins")
        print("  1/2-1/2   Draw")
        print("  *         In progress/Unknown")
        
        while True:
            result = input("\nResult: ").strip()
            if result in ['1-0', '0-1', '1/2-1/2', '*']:
                return result
            print("Invalid result. Please enter 1-0, 0-1, 1/2-1/2, or *")
    
    def add_more_moves(self):
        """
        Allow user to add more moves to the game after stopping early.
        
        This method handles two scenarios:
        1. If there's a pending white move (user stopped after white's move),
           prompt for black's move first to complete the pair
        2. Otherwise, start fresh with a new move pair
        """
        print("\n" + "-" * 60)
        print("Adding more moves...")
        print("Type 'done' to finish | Type 'help' for commands")
        print("-" * 60)
        
        move_count = self.game.get_move_count()
        has_pending = self.game.has_pending_white_move()
        
        if has_pending:
            move_number = move_count + 1
            
            while True:
                black_input = self.get_move_input('black', move_number)
                
                if black_input.lower() in ['quit', 'exit', 'done']:
                    return
                
                if black_input.lower() in ['undo', 'show', 'preview', 'legal', 'help']:
                    result = self.handle_command(black_input)
                    if result == 'quit':
                        return
                    continue
                
                success, message = self.game.validate_and_add_move(black_input, 'black')
                if success:
                    print(f"\033[A\033[KBlack's move: {black_input} ✓")
                    
                    board_state = self.game.get_board_state()
                    if board_state:
                        print(f"  {board_state}")
                    
                    if self.game.is_game_over():
                        return
                    
                    move_number += 1
                    break
                else:
                    print(f"✗ Invalid move: {message}")
                    continue
        else:
            move_number = move_count + 1
        
        while True:
            while True:
                white_input = self.get_move_input('white', move_number)
                
                if white_input.lower() in ['quit', 'exit', 'done']:
                    self.game.finalize_pending_move()
                    return
                
                if white_input.lower() in ['undo', 'show', 'preview', 'legal', 'help']:
                    result = self.handle_command(white_input)
                    if result == 'quit':
                        self.game.finalize_pending_move()
                        return
                    continue
                
                success, message = self.game.validate_and_add_move(white_input, 'white')
                if not success:
                    print(f"✗ Invalid move: {message}")
                    continue
                
                break
            
            print(f"\033[A\033[KWhite's move: {white_input} ✓")
            
            board_state = self.game.get_board_state()
            if board_state:
                print(f"  {board_state}")
            
            if self.game.is_game_over():
                break
            
            while True:
                black_input = self.get_move_input('black', move_number)
                
                if black_input.lower() in ['quit', 'exit', 'done']:
                    self.game.finalize_pending_move()
                    return
                
                if black_input.lower() in ['undo', 'show', 'preview', 'legal', 'help']:
                    result = self.handle_command(black_input)
                    if result == 'quit':
                        self.game.finalize_pending_move()
                        return
                    continue
                
                success, message = self.game.validate_and_add_move(black_input, 'black')
                if not success:
                    print(f"✗ Invalid move: {message}")
                    continue
                
                break
            
            print(f"\033[A\033[KBlack's move: {black_input} ✓")
            
            board_state = self.game.get_board_state()
            if board_state:
                print(f"  {board_state}")
            
            if self.game.is_game_over():
                break
            
            move_number += 1
        
        self.game.finalize_pending_move()
    
    def preview_and_edit(self) -> bool:
        """
        Show preview and allow editing of moves or adding more moves.
        
        Users can:
        - Edit individual moves by entering the move number
        - Add more moves by typing 'add'
        - Finish and save by typing 'done'
        
        Returns:
            True to continue with save, False to cancel
        """
        preview_input = input("\nWould you like to preview the PGN file? (y/n): ").strip().lower()
        
        if preview_input in ['y', 'yes']:
            print(self.exporter.preview_pgn(self.game))
        
        edit_input = input("\nWould you like to edit moves or add more moves? (y/n): ").strip().lower()
        
        if edit_input not in ['y', 'yes']:
            return True
        
        while True:
            print("\nCurrent moves:")
            print(self.game.get_all_moves_display())
            print()
            
            move_count = self.game.get_move_count()
            if move_count > 0:
                edit_choice = input(f"Enter move number to edit (1-{move_count}), 'add' to add more moves, or 'done' to finish: ").strip()
            else:
                edit_choice = input("Enter 'add' to add moves, or 'done' to finish: ").strip()
            
            if edit_choice.lower() == 'done':
                break
            
            if edit_choice.lower() == 'add':
                self.add_more_moves()
                continue
            
            try:
                move_num = int(edit_choice)
                if move_num < 1 or move_num > move_count:
                    print(f"Invalid move number. Please enter 1-{move_count}")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number, 'add', or 'done'")
                continue
            
            color = input("Which color? (white/black): ").strip().lower()
            if color not in ['white', 'black']:
                print("Invalid color. Please enter 'white' or 'black'")
                continue
            
            moves = self.game.get_moves_list()
            white_move, black_move = moves[move_num - 1]
            
            if color == 'white':
                print(f"Current move: {white_move}")
            else:
                if black_move:
                    print(f"Current move: {black_move}")
                else:
                    print("This move pair has no black move")
                    continue
            
            new_move = input("Enter new move: ").strip()
            
            success, message = self.game.edit_move(move_num, color, new_move)
            if success:
                print("✓ Move updated")
            else:
                print(f"✗ {message}")
        
        print("\nFinal PGN:")
        print(self.exporter.preview_pgn(self.game))
        
        return True
    
    def save_game(self):
        """Save the game to a PGN file."""
        print("\nSaving PGN file...")
        
        try:
            filepath = self.exporter.export_to_file(self.game)
            print(f"✓ PGN file saved: {filepath}")
        except Exception as e:
            print(f"✗ Error saving file: {e}")
    
    def run(self):
        """
        Run the main application.
        
        Application flow:
        1. Display welcome message
        2. Collect game metadata (event, site, players, etc.)
        3. Enter moves with full validation
        4. Get game result
        5. Allow preview, editing, and adding more moves
        6. Save to PGN file
        
        Handles KeyboardInterrupt (Ctrl+C) gracefully at any point.
        """
        try:
            self.print_welcome()
            
            metadata = self.collect_metadata()
            self.game = ChessGame(metadata)
            
            print("\n" + "-" * 60)
            print("Ready to enter moves!")
            print("Type 'done' at any point to stop | Type 'help' for commands")
            print("-" * 60)
            
            self.enter_moves()
            
            if self.game.get_move_count() == 0 and not self.game.has_pending_white_move():
                print("\nNo moves entered. Exiting without saving.")
                return
            
            move_count = self.game.get_move_count()
            if self.game.has_pending_white_move():
                print(f"\n✓ Game stopped. {move_count} complete move(s) + 1 white move recorded.")
            else:
                print(f"\n✓ Game stopped. {move_count} move(s) recorded.")
            
            result = self.get_result()
            self.game.set_result(result)
            
            should_save = self.preview_and_edit()
            
            if should_save:
                self.save_game()
            else:
                print("\nSave cancelled.")
            
            print("\nThank you for using Chess PGN Converter!")
            
        except KeyboardInterrupt:
            print("\n\n" + "=" * 60)
            print("   Program interrupted (Ctrl+C)")
            print("=" * 60)
            
            if self.game and (self.game.get_move_count() > 0 or self.game.has_pending_white_move()):
                print(f"\nYou have {self.game.get_move_count()} move(s) recorded.")
                try:
                    save_choice = input("Would you like to save before exiting? (y/n): ").strip().lower()
                    if save_choice in ['y', 'yes']:
                        if self.game.result == '*' or not self.game.result:
                            self.game.set_result('*')
                        self.save_game()
                except KeyboardInterrupt:
                    print("\n\nExiting without saving.")
            
            print("\nGoodbye!")
            return


def main():
    """Main entry point."""
    app = ChessPGNApp()
    app.run()


if __name__ == '__main__':
    main()
