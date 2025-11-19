# Development Guide

Technical details for contributors.

---

## Setup

### Requirements
- Python 3.8+
- Hatch (recommended) or pip

### Getting Started

```bash
git clone https://github.com/LalatenduMohanty/chess_pgn_recorder.git
cd chess_pgn_recorder

# Option 1: Using Hatch
pip install hatch
hatch shell

# Option 2: Using pip
pip install -r requirements.txt
pip install -e ".[dev]"
```

---

## Development Commands

```bash
# Testing
hatch run test              # Run all tests
hatch run test-verbose      # Verbose output
hatch run test-cov          # With coverage report

# Code Quality
hatch run lint              # Flake8 linting
hatch run typecheck         # Mypy type checking
hatch run format            # Black auto-format
hatch run format-check      # Check formatting only
hatch run check-all         # Run all checks

# Build & Publish
hatch build                 # Build wheel + sdist
hatch publish -r test       # Publish to TestPyPI
hatch publish               # Publish to PyPI
```

---

## Code Standards

### Style
- **Line length:** 127 characters (Flake8) / 100 (Black)
- **Complexity:** Maximum 15 per function
- **Formatting:** Black (auto-format before commit)
- **Imports:** Sorted, `isort` compatible

### Documentation
- **Docstrings:** Google style for all public methods
- **Type hints:** Required for function signatures
- **Comments:** Avoid inline comments - use docstrings

### Testing
- **Coverage target:** >80% on core modules
- **Test naming:** `test_<feature>_<scenario>`
- **Fixtures:** Use pytest fixtures for common setup
- **Integration tests:** Cover full workflows

---

## Architecture

### File Organization

```
src/
├── chess_pgn.py       # CLI application (505 lines)
├── chess_game.py      # Game state + board (244 lines)
├── move_validator.py  # SAN validation (147 lines)
└── pgn_exporter.py    # PGN formatting (177 lines)
```

### Key Classes

#### ChessPGNApp
- **Purpose:** CLI orchestration
- **Complexity:** Reduced via helper methods (`_get_validated_move`, `_enter_move_pair`)
- **UI:** ANSI escape sequences for clean terminal output

#### ChessGame
- **Purpose:** Game state management
- **Board:** Wraps `chess.Board` from python-chess
- **Features:** Undo, edit, legal move validation
- **State:** Maintains move list + pending white move

#### MoveValidator
- **Purpose:** Fast SAN format validation
- **Method:** Regex patterns before board validation
- **Returns:** `(success, error_message)` tuple

#### PGNExporter
- **Purpose:** PGN generation and file output
- **Features:** Filename generation, collision handling
- **Format:** Seven Tag Roster + one move pair per line

---

## Testing Strategy

### Test Coverage

| Module | Coverage | Critical Paths |
|--------|----------|----------------|
| `chess_game.py` | 84% | Move validation, board replay, edit |
| `move_validator.py` | 91% | All SAN patterns, edge cases |
| `pgn_exporter.py` | 88% | Formatting, file I/O |
| `chess_pgn.py` | ~9% | UI code (hard to test, manually verified) |

### Running Tests

```bash
# All tests
pytest tests/

# Specific test class
pytest tests/test_chess_pgn.py::TestChessGame

# With coverage
pytest --cov=src --cov-report=html

# CI simulation
hatch run check-all
```

---

## CI/CD

### GitHub Actions

**.github/workflows/ci.yml** - Runs on all PRs and pushes to main
- Tests on Python 3.8, 3.9, 3.10, 3.11, 3.12
- Flake8 linting
- Mypy type checking
- Black formatting validation
- Coverage upload to Codecov

**.github/workflows/publish.yml** - Triggered by release tags
- Runs tests
- Builds package
- Publishes to PyPI

### Pre-commit Checklist

```bash
hatch run format       # Auto-format
hatch run check-all    # Lint + typecheck + tests
git add .
git commit -m "feat: your changes"
git push
```

---

## Adding Features

### Process

1. **Create branch:** `git checkout -b feature/your-feature`
2. **Write code** with tests
3. **Run checks:** `hatch run check-all`
4. **Update docs:** README, CHANGELOG, relevant guides
5. **Submit PR** with clear description

### Complexity Management

If a function exceeds complexity 15:
1. Extract helper methods (prefix with `_` for private)
2. Use descriptive method names
3. Keep each method focused on one task

Example refactoring:
```python
# Before: Complex function
def complex_function():
    # 100 lines of nested logic
    pass

# After: Extracted helpers
def complex_function():
    self._step_one()
    self._step_two()
    self._step_three()

def _step_one(self):
    # Focused logic
    pass
```

---

## Debugging

### Common Issues

**Import errors:**
- Ensure `src/__init__.py` exists
- Check relative imports in src modules

**Test failures:**
- Run `hatch run test-verbose` for details
- Check test isolation (use fixtures)

**Linter errors:**
- Run `hatch run format` to auto-fix most issues
- Check `.flake8` configuration

**Type errors:**
- Run `hatch run typecheck` for details
- Add type: ignore comments only when necessary

---

## Release Process

See [docs/RELEASE.md](RELEASE.md) for full publishing guide.

Quick steps:
1. Update version in 3 files: `pyproject.toml`, `src/__init__.py`, `CHANGELOG.md`
2. Run `hatch run check-all`
3. Build: `hatch build`
4. Test on TestPyPI: `hatch publish -r test`
5. Publish to PyPI: `hatch publish`

---

## Resources

- **Hatch docs:** https://hatch.pypa.io/
- **pytest docs:** https://docs.pytest.org/
- **python-chess:** https://python-chess.readthedocs.io/
- **PEP 440 (versioning):** https://peps.python.org/pep-0440/
- **Contributing guide:** [CONTRIBUTING.md](../CONTRIBUTING.md)

---

For questions, open an issue on GitHub.

