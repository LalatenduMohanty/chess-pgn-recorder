# Chess PGN Recorder

[![CI](https://github.com/LalatenduMohanty/chess_pgn_recorder/actions/workflows/ci.yml/badge.svg)](https://github.com/LalatenduMohanty/chess_pgn_recorder/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An interactive command-line application that records chess games move-by-move in Standard Algebraic Notation (SAN) and exports them as valid PGN (Portable Game Notation) files with full legal move validation.

## Features

- **Legal move validation** - Uses `python-chess` to validate moves are legal, not just format  
- **Board state tracking** - Maintains full chess board state with check/checkmate detection  
- **Input validation** - Validates all chess moves in Standard Algebraic Notation  
- **Complete move support** - Handles pieces, pawns, captures, castling, promotions, check, and checkmate  
- **Interactive CLI** - User-friendly command-line interface  
- **Stop at any time** - Type 'done' at any point to finish and save partial games  
- **Graceful interruption** - Press Ctrl+C to exit with option to save progress  
- **Preview before save** - Review your game before creating the PGN file  
- **Edit moves** - Modify any move before finalizing  
- **Add more moves** - Continue adding moves after stopping early  
- **Auto-generated filenames** - Files named as `white_black_date_round.pgn`  
- **Standards compliant** - Generates valid PGN format with Seven Tag Roster  

## Installation

Requires Python 3.8+ and the `chess` library.

### Option 1: Using pip (Simple)
```bash
cd chess_pgn_recorder
pip install -r requirements.txt
```

### Option 2: Using Hatch (Recommended for Development)
```bash
cd chess_pgn_recorder
pip install hatch
hatch shell  # Creates virtual environment with dependencies
```

### Option 3: Install as Package
```bash
cd chess_pgn_recorder
pip install -e .  # Install in editable mode
```

### Option 4: Install Directly
```bash
pip install chess>=1.10.0
```

## Usage

### Running the Application

**Option 1: Using the entry point script (Recommended)**
```bash
python chess_pgn_recorder.py
```

or

```bash
python3 chess_pgn_recorder.py
```

or if executable:

```bash
./chess_pgn_recorder.py
```

**Option 2: If installed as package**
```bash
chess-pgn-recorder
```

### Example Session

```
$ python chess_pgn_recorder.py

============================================================
   Chess Notation to PGN Converter
============================================================

Convert your chess game moves to PGN format!
Type 'help' during move entry for command list.

Enter game information:

Event: Friendly Match
Site: Home
Date (YYYY.MM.DD) [press Enter for today]: 
Round: 1
White player: Alice
Black player: Bob

Ready to enter moves! (Type 'help' for commands)


Move 1
White's move: e4 [Valid]
Black's move: e5 [Valid]

Move 2
White's move: Nf3 [Valid]
Black's move: Nc6 [Valid]

Move 3
White's move: Bb5 [Valid]
Black's move: done

Game ended. Enter result:
  1-0       White wins
  0-1       Black wins
  1/2-1/2   Draw
  *         In progress/Unknown

Result: *

Would you like to preview the PGN file? (y/n): y

==================================================
[Event "Friendly Match"]
[Site "Home"]
[Date "2025.11.18"]
[Round "1"]
[White "Alice"]
[Black "Bob"]
[Result "*"]

1. e4 e5 
2. Nf3 Nc6 
3. Bb5 
*
==================================================

Would you like to edit moves or add more moves? (y/n): n

Saving PGN file...
PGN file saved: pgn_output_files/Alice_Bob_2025.11.18_1.pgn

Thank you for using Chess PGN Converter!
```

### Example: Stopping Mid-Game

You can stop at any point and save partial games:

```
Move 1
White's move: e4 [Valid]
Black's move: e5 [Valid]

Move 2
White's move: Nf3 [Valid]
Black's move: done

Game stopped. 1 complete move(s) + 1 white move recorded.

Game ended. Enter result:
  1-0       White wins
  0-1       Black wins
  1/2-1/2   Draw
  *         In progress/Unknown

Result: *
```

The resulting PGN will include:
```pgn
[Event "Friendly Match"]
[Site "Home"]
[Date "2025.11.18"]
[Round "1"]
[White "Alice"]
[Black "Bob"]
[Result "*"]

1. e4 e5 
2. Nf3 
*
```

### Example: Adding More Moves

If you stop early, you can add more moves during the edit phase:

```
Move 1
White's move: e4 ✓
Black's move: e5 ✓

Move 2
White's move: done

✓ Game stopped. 1 move(s) recorded.

Game ended. Enter result:
  1-0       White wins
  0-1       Black wins
  1/2-1/2   Draw
  *         In progress/Unknown

Result: *

Would you like to preview the PGN file? (y/n): y

==================================================
[Event "Friendly Match"]
[Site "Home"]
[Date "2025.11.18"]
[Round "1"]
[White "Alice"]
[Black "Bob"]
[Result "*"]

1. e4 e5 
*
==================================================

Would you like to edit moves or add more moves? (y/n): y

Current moves:
1. e4 e5

Enter move number to edit (1), 'add' to add more moves, or 'done' to finish: add

------------------------------------------------------------
Adding more moves...
Type 'done' to finish | Type 'help' for commands
------------------------------------------------------------

Move 2
White's move: Nf3 ✓
Black's move: Nc6 ✓

Move 3
White's move: Bb5 ✓
Black's move: a6 ✓

Move 4
White's move: done

Current moves:
1. e4 e5
2. Nf3 Nc6
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
[Result "*"]

1. e4 e5 
2. Nf3 Nc6 
3. Bb5 a6 
*
==================================================

Saving PGN file...
PGN file saved: pgn_output_files/Alice_Bob_2025.11.18_1.pgn

Thank you for using Chess PGN Converter!
```

## Valid Move Notation

### Piece Moves
- **Pieces**: Use uppercase letters: K (King), Q (Queen), R (Rook), B (Bishop), N (Knight)
- **Format**: `Piece + Square`
- **Examples**: `Nf3`, `Bb5`, `Qd4`, `Ke2`, `Ra1`

### Pawn Moves
- **Format**: `Square` (no piece letter needed)
- **Examples**: `e4`, `d5`, `a6`, `h3`

### Captures
- **Format**: `Piece + x + Square` or `File + x + Square` (for pawns)
- **Examples**: `Nxf6`, `Bxc4`, `exd5`, `axb6`

### Castling
- **Kingside**: `O-O`
- **Queenside**: `O-O-O`

### Pawn Promotion
- **Format**: `Move + = + Piece`
- **Examples**: `e8=Q`, `axb8=N`, `d1=R`

### Check and Checkmate
- **Check**: Add `+` after the move: `Nf7+`, `Qh5+`
- **Checkmate**: Add `#` after the move: `Qh5#`, `Ra8#`

### Disambiguation
When multiple pieces of the same type can move to the same square:
- **By file**: `Nbd7`, `Rfe1`
- **By rank**: `R1a3`, `N5f3`
- **By both**: `Qh4e1`

## Available Commands

During move entry, you can use these commands:

| Command | Description |
|---------|-------------|
| `quit`, `exit`, `done` | **Stop at any time** and proceed to save |
| `undo` | Remove the last move entered |
| `show` | Display all moves entered so far |
| `preview` | Show current PGN preview |
| `legal` | **Show all legal moves** in current position |
| `help` | Display help message with notation guide |

### Stop at Any Time

You can type `done` (or `quit`, `exit`) at **any point** during move entry:
- After entering White's move → Game saves with that last White move
- After entering Black's move → Game saves with complete move pair
- At the very start → Exit without saving (no moves recorded)

You can also press **Ctrl+C** at any time to interrupt the program. If you have recorded moves, you'll be prompted to save before exiting.

The system will automatically save whatever moves you've entered so far.

## Output Format

Generated PGN files follow the standard format with:

### Seven Tag Roster (Required Headers)
```
[Event "?"]
[Site "?"]
[Date "YYYY.MM.DD"]
[Round "?"]
[White "?"]
[Black "?"]
[Result "?"]
```

### Move Text
- One move pair per line
- Format: `1. e4 e5`
- Result marker at the end

### Example Output
```pgn
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
4. Ba4 Nf6 
5. O-O Nxe4 
1-0
```

## File Naming

Files are automatically named based on the game metadata and saved in the `pgn_output_files/` directory:

**Format**: `pgn_output_files/white_black_date_round.pgn`

**Examples**:
- `pgn_output_files/Alice_Bob_2025.11.18_1.pgn`
- `pgn_output_files/John_Doe_Jane_Smith_2025.11.18_2.pgn`

If a file with the same name exists, a number is appended: `Alice_Bob_2025.11.18_1_2.pgn`

The output directory is created automatically if it doesn't exist.

## Testing

### Using Hatch (Recommended)

```bash
# Run all tests
hatch run test

# Run with verbose output
hatch run test-verbose

# Run with coverage report
hatch run test-cov
```

### Using pytest directly

```bash
# Basic test run
pytest test_chess_pgn.py

# Verbose output
pytest test_chess_pgn.py -v

# With coverage
pytest --cov=. --cov-report=term-missing test_chess_pgn.py
```

### Test Coverage

The test suite includes **46 comprehensive tests**:
- Move validation (all notation types) - 15 tests
- Legal move validation - 4 tests
- Board state tracking - 7 tests
- Game state management - 10 tests
- Move editing and undo - 6 tests
- PGN generation and formatting - 8 tests
- File output and naming - 4 tests
- Integration tests - 2 tests

**Coverage**: 84-91% for core modules

## Development with Hatch

This project uses [Hatch](https://hatch.pypa.io/) for modern Python project management.

### Hatch Commands

```bash
# Testing
hatch run test              # Run all tests
hatch run test-verbose      # Run tests with verbose output
hatch run test-cov          # Run tests with coverage report

# Code Quality
hatch run lint              # Run flake8 linter
hatch run typecheck         # Run mypy type checker
hatch run format-check      # Check code formatting with black
hatch run format            # Auto-format code with black
hatch run check-all         # Run all checks (lint + typecheck + test-cov)

# Environment
hatch shell                 # Enter virtual environment shell
hatch env prune             # Clean environment
```

### Benefits of Using Hatch
- Automatic virtual environment management
- Dependency isolation
- Consistent testing across environments
- Modern Python packaging standards
- Easy script execution
- Integrated code quality tools

## Continuous Integration

This project uses GitHub Actions for continuous integration:

### CI Pipeline
- **Multi-version testing**: Tests run on Python 3.8, 3.9, 3.10, 3.11, and 3.12
- **Code linting**: Flake8 checks for code quality and style issues
- **Type checking**: Mypy validates type hints and catches type errors
- **Code formatting**: Black ensures consistent code style
- **Test coverage**: Coverage reports are generated and uploaded to Codecov

### Running CI Checks Locally

Before pushing code, run all CI checks locally:

```bash
# Run all checks at once
hatch run check-all

# Or run individually
hatch run lint        # Linting with flake8
hatch run typecheck   # Type checking with mypy
hatch run test-cov    # Tests with coverage
```

### Code Quality Standards
- **Line length**: Maximum 127 characters
- **Complexity**: Maximum complexity of 10
- **Type hints**: Encouraged but not strictly enforced
- **Code style**: Black formatting (100 character line length)

## Project Structure

```
chess_pgn_recorder/
├── chess_pgn_recorder.py   # Main entry point script
├── pyproject.toml          # Project configuration (hatchling)
├── requirements.txt        # Dependencies
├── DESIGN_DOC.md           # Detailed design documentation
├── README.md               # This file
├── src/                    # Source code directory
│   ├── __init__.py        # Package initialization
│   ├── chess_pgn.py       # Main application logic
│   ├── chess_game.py      # Game state management
│   ├── move_validator.py  # Move validation logic
│   └── pgn_exporter.py    # PGN file generation
├── tests/                  # Test directory
│   ├── __init__.py        # Test package initialization
│   └── test_chess_pgn.py  # Unit tests (46 tests)
├── examples/
│   └── sample_game.pgn    # Example output
└── pgn_output_files/       # Generated PGN files (auto-created)
```

## Common Errors and Solutions

### "Piece notation must be uppercase"
Invalid: `nf3`  
Valid: `Nf3`

Piece letters must be uppercase: K, Q, R, B, N

### "Invalid rank: ranks must be 1-8"
Invalid: `e9`  
Valid: `e8`

Valid ranks are 1 through 8 only.

### "Invalid promotion piece"
Invalid: `e8=K`  
Valid: `e8=Q`

Can only promote to Queen (Q), Rook (R), Bishop (B), or Knight (N).

### "Invalid castling notation"
Invalid: `0-0` (zeros)  
Valid: `O-O` (capital letter O)

Use the letter O, not the number 0.

## Chess Engine Integration

This application uses the **`python-chess`** library by Niklas Fiekas for:
- Full chess rules enforcement  
- Legal move validation
- Board state tracking
- Check/checkmate detection
- Stalemate and draw detection

**Only legal moves are accepted!** The system will reject:
- Moves that leave your king in check
- Moves that don't follow piece movement rules  
- Castling when not allowed
- Any move that's illegal in the current position

## Future Enhancements

Potential features for future versions:
- Board state tracking for legal move validation
- Load and edit existing PGN files
- Multiple game support in one session
- Move comments and annotations
- Time control tracking
- FEN position export
- Game database integration

## Contributing

This is an educational project for learning Python. Feel free to:
- Report issues or bugs
- Suggest new features
- Submit improvements
- Use as a learning resource

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

Copyright 2025 Lalatendu Mohanty

## Support

For questions or issues:
1. Check the DESIGN_DOC.md for detailed technical information
2. Review the examples in this README
3. Run tests to ensure proper installation
4. Type `help` in the application for quick reference

## Contributing

This project is part of a Python training repository but welcomes contributions:
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## Acknowledgments

- Chess notation standards: [FIDE Handbook](https://handbook.fide.com/)
- PGN specification: [PGN Standard](http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm)
- Chess engine: [python-chess](https://github.com/niklasf/python-chess) by Niklas Fiekas

---

**Happy Chess Recording!**

