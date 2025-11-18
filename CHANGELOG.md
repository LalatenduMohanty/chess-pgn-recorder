# Changelog

## [0.1.1-alpha] - 2025-11-18

### Added
- **GitHub Actions CI/CD Pipeline** (`.github/workflows/ci.yml`)
  - Multi-version testing on Python 3.8, 3.9, 3.10, 3.11, 3.12
  - Automated linting with Flake8
  - Type checking with Mypy
  - Code formatting validation with Black
  - Coverage report integration with Codecov
  
- **Development Tools Configuration**
  - `.flake8` configuration file for linting standards
  - Black formatter configuration in `pyproject.toml`
  - Mypy type checker configuration in `pyproject.toml`
  
- **Hatch Scripts for Code Quality**
  - `hatch run lint` - Run Flake8 linter
  - `hatch run typecheck` - Run Mypy type checker
  - `hatch run format` - Auto-format code with Black
  - `hatch run format-check` - Check code formatting
  - `hatch run check-all` - Run all quality checks
  
- **CONTRIBUTING.md** - Comprehensive contributor guidelines
  - Development setup instructions
  - Code quality standards
  - Testing guidelines
  - Pull request process
  - Commit message conventions
  
- **CI Badges in README**
  - GitHub Actions CI status badge
  - PyPI version badge
  - PyPI downloads badge
  - Python version badge
  - License badge
  - Code style badge

- **PyPI Publishing Setup**
  - `RELEASE.md` - Comprehensive release guide
  - `PYPI_SETUP.md` - Quick start guide for PyPI publishing
  - GitHub Actions workflow for automated PyPI publishing
  - Hatch scripts for building and publishing
  - Package metadata configured for PyPI
  - Author email added to pyproject.toml
- **Documentation Refresh**
  - README trimmed to essentials (quick start, workflow, commands)
  - DESIGN_DOC rewritten as concise architecture brief
  - Documentation map added for quicker discovery

### Changed
- **Code Refactoring for Reduced Complexity**
  - Extracted helper methods from complex functions
  - Reduced cyclomatic complexity to ≤15 for all methods
  - `enter_moves()`: 78 lines → 10 lines (uses `_enter_move_pair()` helper)
  - `add_more_moves()`: 115 lines → 30 lines (uses extracted helpers)
  - `preview_and_edit()`: 77 lines → 50 lines (uses `_edit_single_move()` helper)
  - Added 6 private helper methods: `_get_validated_move()`, `_display_move_confirmation()`, etc.
  - Total code reduction: ~75 lines eliminated through DRY principles

- **Code Cleanup**
  - Removed all inline comments from source files
  - Documentation now provided through docstrings only
  - Code is self-documenting with clear function/variable names
  - Black auto-formatting applied to all files
  
- **Documentation Reorganization**
  - README.md: 621 lines → 139 lines (77% reduction)
  - DESIGN_DOC.md: 867 lines → 132 lines (85% reduction)
  - Moved detailed docs to `docs/` directory:
    - `docs/USAGE.md` - Detailed usage examples and notation (202 lines)
    - `docs/DEVELOPMENT.md` - Architecture and dev setup (251 lines)
    - `docs/README.md` - Documentation index (46 lines)
  - Relocated release guides: RELEASE.md, PYPI_SETUP.md, PYPI_CHECKLIST.md to `docs/`
  - Root README now scannable and focused on quick start
  
- **Updated `.gitignore`**
  - Added `.ruff_cache/` directory
  
- **Development Dependencies**
  - Added `flake8>=6.0.0` for linting
  - Added `mypy>=1.0.0` for type checking
  - Added `black>=23.0.0` for code formatting

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

