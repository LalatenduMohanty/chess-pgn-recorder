# Chess PGN Recorder

[![CI](https://github.com/LalatenduMohanty/chess_pgn_recorder/actions/workflows/ci.yml/badge.svg)](https://github.com/LalatenduMohanty/chess_pgn_recorder/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/chess-pgn-recorder.svg)](https://pypi.org/project/chess-pgn-recorder/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Downloads](https://pepy.tech/badge/chess-pgn-recorder)](https://pepy.tech/project/chess-pgn-recorder)

Record chess games move-by-move in Standard Algebraic Notation, validate every move for legality using `python-chess`, and export polished PGN files that work with any chess analysis tool (Chess.com, Lichess, etc.).

---

## Quick Start

```bash
pip install chess-pgn-recorder
chess-pgn-recorder
```

Or from source:
```bash
git clone https://github.com/LalatenduMohanty/chess_pgn_recorder.git
cd chess_pgn_recorder
pip install -r requirements.txt
python chess_pgn_recorder.py
```

---

## What It Does

- **Legal move validation** - Every move checked using `python-chess`
- **Interactive workflow** - Stop, edit, or add moves at any time
- **Standards compliant** - Generates valid PGN with Seven Tag Roster
- **User-friendly** - Commands: `done`, `undo`, `show`, `preview`, `legal`, `help`
- **Graceful Ctrl+C** - Save partial games on interrupt

---

## Example Usage

```
$ chess-pgn-recorder
Event: Friendly Match
White player: Alice | Black player: Bob

Move 1  White: e4 ✓  Black: e5 ✓
Move 2  White: Nf3 ✓  Black: Nc6 ✓
Move 3  White: Bb5 ✓  Black: done

Preview PGN? y
[Event "Friendly Match"]...
1. e4 e5  2. Nf3 Nc6  3. Bb5 *

Edit or add moves? n
PGN saved: pgn_output_files/Alice_Bob_2025.11.18_1.pgn
```

---

## Commands

| Command | Action |
|---------|--------|
| `done`, `quit`, `exit` | Stop and save |
| `undo` | Remove last move |
| `show` | Display all moves |
| `preview` | Show PGN |
| `legal` | List legal moves |
| `help` | Show notation guide |

---

## What To Do With Your PGN Files

Generated files work with all major chess platforms:

- **[Chess.com Analysis](https://www.chess.com/analysis)** - Upload for computer analysis, move accuracy scores, and insights
- **[Lichess Study](https://lichess.org/study)** - Free Stockfish analysis, add comments, share with others  
- **ChessBase / SCID** - Build and manage your game database
- **Chess engines** - Analyze with Stockfish, Komodo, or other UCI engines
- **Share & embed** - Standard PGN format works everywhere

Find your PGN files in the `pgn_output_files/` directory.

---

## Development

```bash
# Run tests
hatch run test              # All tests
hatch run test-cov          # With coverage

# Code quality
hatch run lint              # Flake8
hatch run typecheck         # Mypy
hatch run format            # Black formatter
hatch run check-all         # All checks

# Build & publish
hatch build                 # Create wheel
hatch publish -r test       # TestPyPI
hatch publish               # PyPI
```

---

## Documentation

- **[Usage Guide](docs/USAGE.md)** - Detailed examples and move notation
- **[Development Guide](docs/DEVELOPMENT.md)** - Architecture and contributing  
- **[Release Guide](docs/RELEASE.md)** - Publishing to PyPI
- **[CHANGELOG](CHANGELOG.md)** - Version history
- **[All Docs](docs/)** - Complete documentation index

---

## Project Structure

```
chess_pgn_recorder/
├── src/                  # Source code
│   ├── chess_pgn.py      # CLI + workflow
│   ├── chess_game.py     # Board + state management
│   ├── move_validator.py # SAN validation
│   └── pgn_exporter.py   # PGN formatting
├── tests/                # 46 pytest tests (85%+ coverage)
├── docs/                 # Detailed documentation
└── .github/workflows/    # CI/CD pipelines
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

1. Fork and clone
2. Create feature branch
3. Run `hatch run check-all`
4. Submit PR

Issues and suggestions welcome!

---

## License

Apache License 2.0 © 2025 Lalatendu Mohanty

---

**Happy Chess Recording!**
