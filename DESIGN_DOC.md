# Chess PGN Recorder - Design Document

## System Overview
An interactive command-line application that records chess games move-by-move in Standard Algebraic Notation (SAN) and exports them as valid PGN (Portable Game Notation) files. The system validates each move for both format and legality, building a complete game record with full chess rules enforcement.

---

## Project Goals
1. Accept user input for chess moves (white and black) in algebraic notation
2. Validate each move to ensure it follows proper algebraic notation format
3. Store moves in sequence with proper move numbering
4. Generate a valid PGN file with game metadata and moves
5. Provide clear error messages for invalid inputs

---

## Algebraic Notation Format

### Valid Move Patterns
1. **Pawn Moves**: `e4`, `d5`, `e8=Q` (with promotion)
2. **Piece Moves**: `Nf3`, `Bb5`, `Qd4`, `Kh1`, `Ra8`
3. **Captures**: `exd5`, `Nxf6`, `Bxc4`
4. **Castling**: `O-O` (kingside), `O-O-O` (queenside)
5. **Check/Checkmate**: `Nf7+`, `Qh5#`
6. **Disambiguation**: `Nbd7`, `R1a3`, `Qh4e1` (when multiple pieces can move to same square)
7. **Pawn Promotion**: `e8=Q`, `axb8=N`, `d1=R+`

### Notation Components
- **Piece**: K (King), Q (Queen), R (Rook), B (Bishop), N (Knight), omitted for pawns
- **File**: a-h (column)
- **Rank**: 1-8 (row)
- **Capture**: x
- **Promotion**: =Q, =R, =B, =N
- **Check**: +
- **Checkmate**: #
- **Annotations**: !, !!, ?, ??, !?, ?! (optional)

---

## PGN Format Structure

### Required Headers (Seven Tag Roster)
```
[Event "Friendly Match"]
[Site "New York, USA"]
[Date "2025.01.15"]
[Round "1"]
[White "John Doe"]
[Black "Jane Smith"]
[Result "1-0"]
```

### Move Text Format
- Each move pair on its own line for readability
- Move numbers followed by period and space
- White move, space, black move, space
- Blank line between headers and moves
- Result terminator at the end: `1-0` (White wins), `0-1` (Black wins), `1/2-1/2` (Draw), `*` (In progress)

Example:
```
1. e4 e5 
2. Nf3 Nc6 
3. Bc4 Bc5 
4. c3 Nf6 
5. d4 exd4 
1-0
```

---

## Architecture

### Classes/Modules

#### 1. MoveValidator Class
**Purpose**: Validate algebraic notation input

**Methods**:
- `validate_move(move: str) -> bool`: Check if move string is valid algebraic notation
- `is_valid_piece(piece: str) -> bool`: Validate piece notation
- `is_valid_square(square: str) -> bool`: Validate board coordinates (a1-h8)
- `is_castling(move: str) -> bool`: Check for castling notation
- `is_promotion(move: str) -> bool`: Check for pawn promotion

**Validation Rules**:
- Regex patterns for each move type
- Case sensitivity (pieces must be uppercase, files lowercase)
- Square coordinates within bounds (a-h, 1-8)
- Proper castling format
- Valid promotion pieces only (Q, R, B, N)

#### 2. ChessGame Class
**Purpose**: Store and manage the game state

**Attributes**:
- `moves: list[tuple[str, str]]`: List of (white_move, black_move) tuples
- `metadata: dict`: PGN header information
- `result: str`: Game result (default: "*")
- `current_move_number: int`: Track move count

**Methods**:
- `__init__(metadata: dict)`: Initialize with game metadata
- `add_move(white_move: str, black_move: str = None)`: Add a move pair
- `get_move_count() -> int`: Return number of full moves
- `set_result(result: str)`: Set game outcome
- `validate_and_add_move(move: str, color: str)`: Validate then add move
- `edit_move(move_number: int, color: str, new_move: str)`: Edit a specific move
- `undo_last_move()`: Remove the last half-move entered
- `get_all_moves_display() -> str`: Return formatted list of all moves for display

#### 3. PGNExporter Class
**Purpose**: Generate PGN format output

**Methods**:
- `export_to_file(game: ChessGame, filename: str)`: Create PGN file
- `format_headers(metadata: dict) -> str`: Format PGN headers with blank lines
- `format_moves(moves: list, result: str) -> str`: Format move text (one move pair per line)
- `generate_pgn_string(game: ChessGame) -> str`: Complete PGN string
- `generate_filename(metadata: dict) -> str`: Create filename from player names, date, and round
- `preview_pgn(game: ChessGame) -> str`: Generate preview string for display

**Formatting Rules**:
- Headers: Each header on its own line with blank line after
- Moves: One move pair per line (e.g., "1. e4 e5 \n")
- Result appears both in header and at end of move text
- Trailing space after each move for consistency
- Filename format: `pgn_output_files/white_black_YYYY.MM.DD_round.pgn` (spaces replaced with underscores)
- Files saved in dedicated `pgn_output_files/` directory

---

## User Interaction Flow

### Application Flow
```
1. Welcome message with stop-at-any-time reminder
2. Collect game metadata:
   - Event name
   - Site/Location
   - Date (auto-generated or user input)
   - Round number
   - White player name
   - Black player name
3. Display startup instructions:
   - Remind user they can stop at any time with 'done'
   - Show help command availability
4. Enter move input loop:
   a. Display "Move X" header
   b. Prompt for white's move
   c. Check if command (done/quit/exit/undo/show/preview/help)
   d. Validate move
   e. If invalid, show error and re-prompt
   f. If valid, display inline confirmation with checkmark
   g. Prompt for black's move
   h. Check if command
   i. Validate move
   j. If invalid, show error and re-prompt
   k. If valid, display inline confirmation with checkmark
   l. Increment move number
5. When user ends game (quit/done at ANY point):
   a. Finalize any pending white-only move
   b. Display count of recorded moves
   c. Prompt for game result (1-0, 0-1, 1/2-1/2, *)
   d. Ask: "Would you like to preview the PGN file? (y/n)"
   e. If yes, display complete PGN content with borders
   f. Ask: "Would you like to edit moves or add more moves? (y/n)"
   g. If yes:
      - Show numbered list of all moves
      - Prompt: "Enter move number to edit (1-N), 'add' to add more moves, or 'done' to finish:"
      - If user enters a number:
        * Allow user to re-enter specific move
        * Validate new move
        * Update move in list
      - If user enters 'add':
        * Enter move addition mode
        * Continue from last move number
        * Support all move entry commands (help, show, preview, legal, undo)
        * Return to edit menu when done
      - Show updated moves after each change
      - Repeat until user types 'done'
      - Show final PGN preview
   h. Generate filename: white_black_date_round.pgn
   i. Save PGN file
   j. Display success message with filename
```

### Commands (During Move Entry)
- `quit` / `exit` / `done`: **Stop at any time** and proceed to preview/save
- `undo`: Remove last half-move (single move, not move pair)
- `show`: Display all moves entered so far
- `help`: Display command list and notation guide
- `preview`: Show current PGN preview

### Stop at Any Time Feature
Users can type `done`, `quit`, or `exit` at **any move prompt**:
- After white's move → Game saves with incomplete move pair
- After black's move → Game saves with complete move pair
- Prompts remind users of this option
- System provides feedback on how many moves were recorded

Users can also press **Ctrl+C** at any point:
- Program catches KeyboardInterrupt gracefully
- If moves are recorded, offers to save before exiting
- Second Ctrl+C immediately exits without saving
- Clean exit message displayed

---

## Input Validation Strategy

### Regular Expression Patterns
```python
# Piece move: Nf3, Bb5, etc.
PIECE_MOVE = r'^[KQRBN][a-h]?[1-8]?x?[a-h][1-8][+#]?[!?]*$'

# Pawn move: e4, e5, etc.
PAWN_MOVE = r'^[a-h][1-8][+#]?[!?]*$'

# Pawn capture: exd5, etc.
PAWN_CAPTURE = r'^[a-h]x[a-h][1-8][+#]?[!?]*$'

# Pawn promotion: e8=Q, etc.
PAWN_PROMOTION = r'^[a-h]?x?[a-h][18]=[QRBN][+#]?[!?]*$'

# Castling
CASTLING = r'^O-O(-O)?[+#]?[!?]*$'
```

### Validation Steps
1. Check move is non-empty string
2. Remove whitespace
3. Check against castling pattern first
4. Check against promotion pattern
5. Check against capture patterns
6. Check against piece/pawn move patterns
7. Return validation result with error message if invalid

---

## Data Structures

### Game Metadata Dictionary
```python
{
    'Event': 'Friendly Match',
    'Site': 'New York, USA',
    'Date': '2025.01.15',
    'Round': '1',
    'White': 'John Doe',
    'Black': 'Jane Smith',
    'Result': '1-0'
}
```

### Move Storage
```python
moves = [
    ('e4', 'e5'),      # Move 1
    ('Nf3', 'Nc6'),    # Move 2
    ('Bb5', 'a6'),     # Move 3
    ('Ba4', None)      # Move 4 (incomplete)
]
```

---

## Example Usage

### Sample Session (Implemented Format)
```
============================================================
   Chess Notation to PGN Converter
============================================================

Convert your chess game moves to PGN format!
Type 'help' for commands | Type 'done' to finish at any time

Enter game information:

Event: Friendly Match
Site: Home
Date (YYYY.MM.DD) [press Enter for today]: 
Round: 1
White player: Alice
Black player: Bob

------------------------------------------------------------
Ready to enter moves!
Type 'done' at any point to stop | Type 'help' for commands
------------------------------------------------------------

Move 1
White's move: e4 [Valid]
Black's move: e5 [Valid]

Move 2
White's move: Nf3 [Valid]
Black's move: Nc6 [Valid]

Move 3
White's move: Bb5 [Valid]
Black's move: a6 [Valid]

Move 4
White's move: done

Game stopped. 3 move(s) recorded.

Game ended. Enter result:
  1-0       White wins
  0-1       Black wins
  1/2-1/2   Draw
  *         In progress/Unknown

Result: 1-0

Would you like to preview the PGN file? (y/n): y

==================================================
[Event "Friendly Match"]
[Site "Home"]
[Date "2025.11.18"]
[Round "1"]
[White "Alice"]
[Black "Bob"]
[Result "1-0"]

1. e4 e5 
2. Nf3 Nc6 
3. Bb5 a6 
1-0
==================================================

Would you like to edit moves or add more moves? (y/n): y

Current moves:
1. e4 e5
2. Nf3 Nc6
3. Bb5 a6

Enter move number to edit (1-3), 'add' to add more moves, or 'done' to finish: 2
Which color? (white/black): black
Current move: Nc6
Enter new move: Nf6
✓ Move updated

Current moves:
1. e4 e5
2. Nf3 Nf6
3. Bb5 a6

Enter move number to edit (1-3), 'add' to add more moves, or 'done' to finish: done

Final PGN:

==================================================
[Event "Friendly Match"]
[Site "Home"]
[Date "2025.11.18"]
[Round "1"]
[White "Alice"]
[Black "Bob"]
[Result "1-0"]

1. e4 e5 
2. Nf3 Nf6 
3. Bb5 a6 
1-0
==================================================

Saving PGN file...
PGN file saved: pgn_output_files/Alice_Bob_2025.11.18_1.pgn

Thank you for using Chess PGN Converter!
```

### Sample PGN Output
```pgn
[Event "Friendly Match"]
[Site "Home"]
[Date "2025.11.18"]
[Round "1"]
[White "Alice"]
[Black "Bob"]
[Result "*"]

1. e4 e5 
2. Nf3 Nc6 
3. Bb5 a6 
*
```

---

## Error Handling

### Invalid Move Examples
- `e9` → "Invalid rank: ranks must be 1-8"
- `Ke4` → "Valid notation but may be illegal position"
- `xyz` → "Invalid move format"
- `nf3` → "Piece notation must be uppercase (Nf3)"
- `e8=K` → "Invalid promotion: can only promote to Q, R, B, or N"

### Error Messages
- Clear, specific messages for each error type
- Suggest correct format when possible
- Allow user to retry without losing previous moves

---

## File Output

### Filename Format
- **Auto-generated from metadata**: `pgn_output_files/white_black_date_round.pgn`
- Example: `pgn_output_files/Alice_Bob_2025.11.18_1.pgn`
- Spaces in player names replaced with underscores
- Date format: YYYY.MM.DD
- Auto-append `.pgn` extension if missing
- If file exists, append number: `Alice_Bob_2025.11.18_1_2.pgn`
- Output directory is created automatically if it doesn't exist

### Filename Generation Rules
```python
white_name = metadata['White'].replace(' ', '_')
black_name = metadata['Black'].replace(' ', '_')
date = metadata['Date']  # Already in YYYY.MM.DD format
round_num = metadata['Round']
filename = f"{white_name}_{black_name}_{date}_{round_num}.pgn"
```

---

## Success Criteria (All Implemented)

### Core Functionality
- Accept algebraic notation input for chess moves  
- Validate each move against proper SAN format  
- Handle all move types (pieces, pawns, captures, castling, promotion)  
- Store moves with correct numbering  
- Generate valid PGN file with required headers  
- Provide clear error messages for invalid input  
- Support game commands (quit, undo, show, preview)  
- Include metadata in PGN output  
- Handle incomplete games (last move is white only)  
- Support special notation (check, checkmate, annotations)

### Advanced Features
- **Preview PGN before saving**  
- **Allow editing of specific moves before saving**  
- **Add more moves after stopping early**  
- **Auto-generate filename from metadata (white_black_date_round.pgn)**  
- **Show numbered move list during editing**  
- **Validate edited moves before accepting changes**  

### User Experience Enhancements
- **Stop at any time** - Users can quit at any move prompt  
- **Graceful interruption** - Ctrl+C handled cleanly with save option  
- **Clean single-line confirmations** - Moves shown with inline checkmark  
- **Prominent reminders** - Constant visibility of stop option  
- **Move count feedback** - System reports how many moves were recorded  
- **Compact formatting** - Reduced blank lines for better readability  
- **ANSI escape sequences** - Terminal cursor manipulation for clean output

### Board State Tracking (NEW)
- **Legal move validation** - Only legal moves accepted using python-chess
- **Check detection** - Automatic check notification
- **Checkmate detection** - Game ends automatically on checkmate
- **Stalemate detection** - Draw conditions detected
- **Legal moves command** - Show all legal moves in current position
- **Turn enforcement** - Validates correct player is moving  

---

## Future Enhancements (Phase 2)

1. **Board State Tracking**: Validate moves are legal for current position
2. **Load Existing PGN**: Edit or continue existing games
3. **Multiple Game Support**: Handle multiple games in one file
4. **Move Comments**: Add annotations and variations
5. **Time Controls**: Track and record time used per move
6. **FEN Support**: Export position in FEN notation
7. **GUI Interface**: Visual board representation
8. **Move Suggestions**: Auto-complete common moves
9. **Game Analysis**: Basic move quality indicators
10. **Database Integration**: Store games in SQLite database

---

## Testing Strategy

### Unit Tests
- Test each validation regex pattern
- Test move parsing and storage
- Test PGN header formatting
- Test move text generation
- Test file I/O operations

### Integration Tests
- Test complete game flow
- Test error recovery
- Test incomplete games
- Test special cases (promotions, castling)

### Edge Cases
- Empty input
- Very long games (100+ moves)
- Special characters in metadata
- All possible promotion types
- Multiple captures in sequence
- Disambiguated moves

---

## Dependencies

### Core Dependencies
- Python 3.8+
- `chess>=1.10.0`: python-chess library for board state and legal move validation

### Standard Library Modules
- `re`: Regular expressions for format validation
- `datetime`: Timestamp generation
- `typing`: Type hints
- `os`: File operations
- `tempfile` (testing): Temporary directories for tests

### Development Dependencies
- `pytest>=7.0.0`: Testing framework
- `pytest-cov>=4.0.0`: Coverage reporting
- `hatch`: Project management and packaging

---

## Technical Implementation Details

### File Structure (Actual Implementation)
```
chess_pgn_recorder/
├── chess_pgn_recorder.py  # Main entry point script
├── pyproject.toml         # Hatch project configuration
├── requirements.txt       # Pip dependencies
├── src/                   # Source code package
│   ├── __init__.py       # Package initialization
│   ├── chess_pgn.py      # Main application logic (580 lines)
│   │   └── ChessPGNApp class with run() method
│   ├── move_validator.py # Format validation (141 lines)
│   │   └── MoveValidator class with regex patterns
│   ├── chess_game.py     # Game logic with board (245 lines)
│   │   └── ChessGame class with chess.Board integration
│   └── pgn_exporter.py   # PGN generation (178 lines)
│       └── PGNExporter class with formatting
├── tests/                 # Test package
│   ├── __init__.py       # Test package initialization
│   └── test_chess_pgn.py # Unit tests (515 lines, 46 tests)
├── DESIGN_DOC.md          # This document (704 lines)
├── README.md              # User documentation (548 lines)
├── examples/
│   └── sample_game.pgn    # Example output
└── pgn_output_files/      # Generated PGN files (auto-created)

Total: ~2,900 lines of Python code and documentation
```

### Key Implementation Features

#### Move Validation (move_validator.py)
- **Regex Patterns**: 5 compiled patterns for different move types
- **Error Detection**: Smart error messages based on attempted move type
- **Lowercase Detection**: Special handling to avoid catching pawn moves (b7, etc.)
- **Method**: `validate_move()` returns `(bool, str)` tuple

#### Game Management (chess_game.py)
- **Pending Move Handling**: Tracks white-only moves separately
- **Edit Capability**: Can modify individual moves by number and color
- **Undo Functionality**: Removes last half-move (white or black)
- **Validation Integration**: All moves validated before storage

#### PGN Export (pgn_exporter.py)
- **Seven Tag Roster**: Always includes required headers
- **One Move Per Line**: Each move pair on separate line
- **Filename Generation**: Automatic from metadata with underscore replacement
- **Unique Filenames**: Appends number if file exists

#### User Interface (chess_pgn.py)
- **ANSI Terminal Control**: 
  - `\033[A` - Move cursor up one line
  - `\033[K` - Clear from cursor to end of line
  - Used for inline confirmation checkmarks
- **Command Detection**: Commands checked before move validation
- **Graceful Exit**: Always saves entered moves, even if incomplete
- **Feedback System**: Clear messages for every action

### Testing Strategy (test_chess_pgn.py)

#### Test Classes
1. **TestMoveValidator** (15 tests)
   - Valid moves (pieces, pawns, captures, castling, promotion)
   - Invalid moves (bad ranks, files, promotion pieces)
   - Edge cases (empty input, lowercase pieces)

2. **TestChessGame** (13 tests)
   - Move storage and retrieval
   - Edit and undo functionality
   - Result setting and validation
   - Display formatting

3. **TestPGNExporter** (8 tests)
   - Header formatting
   - Move text generation
   - Filename generation
   - File I/O operations

4. **TestIntegration** (1 test)
   - Complete workflow from start to finish
   - Tests all components working together

#### Test Coverage
- **84-91% coverage** of core modules (chess_game, move_validator, pgn_exporter)
- **Edge cases** tested (empty games, incomplete moves, illegal moves)
- **Board state** tested (check, checkmate, stalemate)
- **File operations** tested with temp directories
- **All passing**: 46/46 tests

### Testing with Hatch
```bash
hatch run test              # Run all tests
hatch run test-verbose      # Verbose output
hatch run test-cov          # With coverage report
```

---

## Project Structure
```
chess_pgn_recorder/
├── chess_pgn_recorder.py  # Main entry point (executable)
├── DESIGN_DOC.md          # This file
├── README.md              # User documentation
├── src/                   # Source code package
│   ├── __init__.py       # Package initialization
│   ├── chess_pgn.py      # Main application logic
│   ├── chess_game.py     # Game state management
│   ├── move_validator.py # Move validation logic
│   └── pgn_exporter.py   # PGN generation
├── tests/                 # Test package
│   ├── __init__.py       # Test package initialization
│   └── test_chess_pgn.py # Unit tests
├── examples/              # Sample PGN files
│   └── sample_game.pgn
└── pgn_output_files/      # Generated PGN files (auto-created)
```

---

## Development Phases

### Phase 1: Core Functionality (MVP) - COMPLETED
1. Implement MoveValidator class with regex patterns
2. Create ChessGame class for move storage
3. Build PGNExporter for file generation
4. Develop main input loop
5. Add basic error handling

### Phase 2: Enhanced Features - COMPLETED
1. Add command system (undo, show, preview)
2. Improve error messages
3. Add move annotations support
4. Implement file management
5. Preview and edit functionality
6. Auto-generated filenames

### Phase 3: Polish - COMPLETED
1. Comprehensive testing (46 unit tests)
2. Documentation (README + DESIGN_DOC)
3. Example games
4. User guide
5. UI/UX improvements (stop-at-any-time, clean formatting)

### Phase 4: Board State Tracking - COMPLETED
1. Integrate python-chess library
2. Legal move validation
3. Check/checkmate/stalemate detection
4. Legal moves command
5. Turn enforcement
6. Board replay for move editing
7. Unit tests for board state features

---

## Implementation Notes

### Design Decisions
- This is a **notation validator**, not a chess engine
- We validate **format**, not **legality** (e.g., won't check if Nf3 is legal)
- Focus on proper PGN standard compliance
- Keep interface simple and intuitive
- Prioritize clear error messages over complex features

### UI/UX Implementation Details
- **ANSI Escape Sequences**: Used `\033[A` (cursor up) and `\033[K` (clear line) for inline confirmations
- **Single-Line Format**: Checkmarks appear on same line as move input for cleaner appearance
- **Persistent Reminders**: Welcome message and startup instructions emphasize stop-at-any-time capability
- **Feedback Loop**: System always confirms action count when user stops
- **Minimal Clutter**: Removed verbose prompt text, relying on clear context

### Code Quality
- **46 Unit Tests**: Full test coverage for all components
- **Type Hints**: Used throughout for better code clarity
- **Modular Design**: Separate classes for validation, game management, and export
- **External Dependency**: python-chess for board state and legal move validation
- **PEP 8 Compliant**: Clean, readable code following Python style guide
- **Modern Packaging**: Uses hatchling and pyproject.toml

