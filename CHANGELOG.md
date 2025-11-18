# Changelog

## [0.1.0-alpha] - 2025-11-18

### Changed - Project Restructure
- **Reorganized project structure** to follow Python best practices
  - Moved all source code to `src/` directory
  - Moved tests to `tests/` directory
  - Created `src/__init__.py` for package initialization
  - Created `tests/__init__.py` for test package
  
- **New entry point**: `chess_pgn_recorder.py`
  - Simple, user-friendly script in project root
  - Can be run with `python chess_pgn_recorder.py`
  - Can be made executable with `chmod +x chess_pgn_recorder.py`
  
- **Updated imports**: All source files now use relative imports
  - `src/chess_pgn.py` imports from `src/chess_game`, etc.
  - Tests properly import from `src.` package
  
- **Updated configuration**:
  - `pyproject.toml` updated for new structure
  - Test paths now point to `tests/` directory
  - Coverage source now points to `src/` directory
  - Package script entry point: `chess-pgn-recorder`

- **Updated documentation**:
  - README.md reflects new project structure
  - DESIGN_DOC.md updated with new file organization
  - Installation and usage instructions updated

### Added
- `src/__init__.py` - Package initialization with version info
- `tests/__init__.py` - Test package initialization
- `chess_pgn_recorder.py` - Main entry point script
- This CHANGELOG.md file

### Project Structure
```
chess_pgn_recorder/
├── chess_pgn_recorder.py   # Main entry point (executable)
├── src/                    # Source code package
│   ├── __init__.py
│   ├── chess_pgn.py
│   ├── chess_game.py
│   ├── move_validator.py
│   └── pgn_exporter.py
├── tests/                  # Test package
│   ├── __init__.py
│   └── test_chess_pgn.py
└── ...
```

## Previous Versions

### Added Features
- Legal move validation using python-chess
- Board state tracking with check/checkmate detection
- Interactive move entry with undo, show, preview commands
- Edit moves and add more moves after stopping
- Graceful Ctrl+C handling
- Auto-generated PGN filenames
- Output files saved in `pgn_output_files/` directory
- Comprehensive error messages
- 46 unit tests with 84-91% coverage

