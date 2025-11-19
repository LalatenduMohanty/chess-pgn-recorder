# Chess PGN Recorder - Design Overview

Quick technical reference for contributors and maintainers.

---

## Architecture

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌──────────────┐
│ chess_pgn   │──▶│ chess_game  │──▶│ pgn_exporter│──▶│ File output  │
│ (CLI/UI)    │◀──│ + python-   │◀──│ (formatting)│◀──│ pgn_output_* │
└─────────────┘   │   chess     │   └─────────────┘   └──────────────┘
       │          └─────────────┘
       ▼
┌─────────────┐
│ move_       │  
│ validator   │  (regex SAN check before board validation)
└─────────────┘
```

| Module | Responsibility |
|--------|----------------|
| `chess_pgn.py` | CLI workflow, command handling, move editing UI |
| `chess_game.py` | Game state, `python-chess` board integration, undo/edit |
| `move_validator.py` | Lightweight SAN format validation (regex) |
| `pgn_exporter.py` | PGN formatting, filename generation, file I/O |

---

## Component Details

### MoveValidator
- 5 regex patterns: pawns, pieces, captures, castling, promotion
- Returns `(is_valid: bool, error_message: str)`
- Fast pre-check before heavier board validation

### ChessGame
- Stores `list[tuple[white_move, black_move]]` + metadata
- Wraps `chess.Board` for legal move checking
- Key methods: `validate_and_add_move()`, `edit_move()`, `undo_last_move()`, `get_legal_moves()`

### PGNExporter
- Formats Seven Tag Roster + move text (one pair per line)
- Auto-generates filenames: `{white}_{black}_{date}_{round}.pgn`
- Saves to `pgn_output_files/` with collision handling

### ChessPGNApp
- Orchestrates CLI prompts and ANSI terminal tricks
- Helper methods keep complexity <15: `_get_validated_move()`, `_enter_move_pair()`, `_edit_single_move()`

---

## CLI Flow

1. **Metadata collection** - Event, Site, Date, Round, players
2. **Move entry loop** - Validate each half-move, display confirmations, handle commands
3. **Stop/finalize** - Count moves, prompt for result
4. **Preview/edit phase** - User can edit moves or add more
5. **Save** - Export to `pgn_output_files/` with auto-generated filename

**Commands available anytime:** `done`, `undo`, `show`, `preview`, `legal`, `help`, `Ctrl+C`

---

## Validation Pipeline

1. **Syntax** - Regex check in `MoveValidator`
2. **Semantics** - `python-chess` board rejects illegal moves (checks, pins, etc.)
3. **Turn enforcement** - Ensures alternating white/black
4. **Game-over detection** - Auto-stops on checkmate/stalemate

---

## Testing

| Suite | Count | Focus |
|-------|-------|-------|
| `TestMoveValidator` | 15 | SAN regex patterns, edge cases |
| `TestChessGame` | 19 | State updates, undo/edit, legal moves |
| `TestPGNExporter` | 8 | Formatting, filename conflicts |
| `TestIntegration` | 4 | End-to-end workflows |

**Total:** 46 tests | **Coverage:** 84-91% on core modules | **CI:** Python 3.8-3.12

---

## Build & Release

- **Build system:** Hatchling (`pyproject.toml`)
- **Packaging:** `hatch build` → wheel + sdist
- **Publishing:** `hatch publish` or GitHub Actions on release tags
- **Version:** `0.1.1a1` (alpha) - see [CHANGELOG.md](CHANGELOG.md)

Full guide: [docs/RELEASE.md](docs/RELEASE.md)

---

## Code Quality Standards

- **Max line length:** 127 (Flake8) / 100 (Black)
- **Max complexity:** 15 (enforced via Flake8)
- **Type hints:** Present (Mypy checked, `ignore_missing_imports`)
- **Formatting:** Black auto-format required
- **Tests:** Must pass before merge

Run `hatch run check-all` before commits.

---

## Future Work

- Load/edit existing PGN files
- Move annotations and variations
- Time control tracking
- FEN export
- Multiple games per session
- Optional GUI

---

## Using Generated PGN Files

Output files are compatible with all major chess platforms:
- **Chess.com** / **Lichess.org** - Upload for analysis and study
- **ChessBase** / **SCID** - Import into chess databases
- **Stockfish** / **Komodo** - Analyze with chess engines
- Standard PGN format works everywhere

---

## References

- **python-chess:** https://github.com/niklasf/python-chess
- **PGN Spec:** http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm
- **FIDE Handbook:** https://handbook.fide.com/
- **Chess.com Analysis:** https://www.chess.com/analysis
- **Lichess Study:** https://lichess.org/study

For detailed usage examples, see [docs/USAGE.md](docs/USAGE.md).

---

**Maintained by:** Lalatendu Mohanty | Apache 2.0
