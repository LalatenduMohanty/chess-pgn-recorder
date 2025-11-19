# Usage Guide

Detailed examples and notation reference for Chess PGN Recorder.

---

## Basic Workflow

1. Run `chess-pgn-recorder` or `python chess_pgn_recorder.py`
2. Enter game metadata (Event, Site, Date, Round, players)
3. Input moves in Standard Algebraic Notation
4. Stop anytime with `done` - partial games are preserved
5. Preview, edit, or add more moves
6. Save to `pgn_output_files/`

---

## Move Notation Reference

### Piece Moves
- **K** (King), **Q** (Queen), **R** (Rook), **B** (Bishop), **N** (Knight)
- Format: `Piece + Square`
- Examples: `Nf3`, `Bb5`, `Qd4`, `Ke2`

### Pawn Moves
- Format: `Square` (no piece letter)
- Examples: `e4`, `d5`, `a6`, `h3`

### Captures
- Format: `Piece + x + Square` or `File + x + Square` (pawns)
- Examples: `Nxf6`, `Bxc4`, `exd5`, `axb6`

### Special Moves
- **Castling:** `O-O` (kingside), `O-O-O` (queenside)
- **Promotion:** `e8=Q`, `axb8=N`, `d1=R`
- **Check:** `Nf7+`, `Qh5+`
- **Checkmate:** `Qh5#`, `Ra8#`
- **Disambiguation:** `Nbd7`, `R1a3`, `Qh4e1`

---

## Commands

| Command | Description |
|---------|-------------|
| `done`, `quit`, `exit` | Stop and save game |
| `undo` | Remove last move |
| `show` | Display all moves |
| `preview` | Show PGN preview |
| `legal` | List all legal moves |
| `help` | Show notation guide |
| `Ctrl+C` | Interrupt with save option |

---

## Example Sessions

### Complete Game

```
$ chess-pgn-recorder

Event: Club Tournament
Site: Chess Club
White player: Alice
Black player: Bob

Move 1
White's move: e4 ✓
Black's move: e5 ✓

Move 2
White's move: Nf3 ✓
Black's move: Nc6 ✓

Move 3
White's move: Bb5 ✓
Black's move: a6 ✓

Move 4
White's move: Ba4 ✓
Black's move: Nf6 ✓

Move 5
White's move: O-O ✓
Black's move: Nxe4 ✓

Move 6
White's move: done

Result: 1-0

✓ PGN saved: pgn_output_files/Alice_Bob_2025.11.18_1.pgn
```

### Stopping Mid-Game

```
Move 1
White's move: e4 ✓
Black's move: e5 ✓

Move 2
White's move: done

✓ Game stopped. 1 move(s) recorded.
Result: *
```

Output:
```pgn
[Event "Club Tournament"]
[Site "Chess Club"]
[Date "2025.11.18"]
[Round "1"]
[White "Alice"]
[Black "Bob"]
[Result "*"]

1. e4 e5 
*
```

### Adding More Moves

If you stop early, you can continue during the edit phase:

```
✓ Game stopped. 1 move(s) recorded.
Result: *

Preview PGN? y
[Shows: 1. e4 e5 *]

Edit or add moves? y

Current moves:
1. e4 e5

Enter move number to edit (1), 'add' to add more moves, or 'done': add

Move 2
White's move: Nf3 ✓
Black's move: Nc6 ✓

Move 3
White's move: done

Enter move number to edit (1-2), 'add', or 'done': done

✓ PGN saved: pgn_output_files/Alice_Bob_2025.11.18_1.pgn
```

---

## Common Errors

| Error | Fix |
|-------|-----|
| `nf3` - "Piece must be uppercase" | Use `Nf3` |
| `e9` - "Invalid rank" | Ranks are 1-8 |
| `e8=K` - "Invalid promotion" | Only Q, R, B, N |
| `0-0` - "Invalid castling" | Use letter O: `O-O` |
| Empty move | Enter a valid move or command |

---

## Output Files

- **Location:** `pgn_output_files/` (auto-created)
- **Format:** `{white}_{black}_{date}_{round}.pgn`
- **Example:** `Alice_Bob_2025.11.18_1.pgn`
- **Conflicts:** Auto-numbered: `..._1_2.pgn`

### Using Your PGN Files

Generated PGN files work with all major chess platforms:

**Analysis & Study:**
- **Chess.com** - Upload to Analysis Board for computer analysis
- **Lichess.org** - Import to Study feature for analysis
- **Chess.com Insights** - Get move accuracy and blunder detection
- **Lichess Analysis** - Free Stockfish analysis with best moves

**Database & Organization:**
- **ChessBase** - Import into professional database
- **SCID** - Free chess database software
- **ChessTempo** - Study tactics from your games

**Sharing:**
- **PGN Viewer websites** - Embed games on websites
- **Chess forums** - Share games with standard PGN format
- **Study groups** - Distribute games to teammates

**Example - Chess.com:**
1. Go to Chess.com → Analysis Board
2. Click "Import" → "From PGN"
3. Upload your `.pgn` file
4. Get instant computer analysis, move classification, and insights

**Example - Lichess:**
1. Go to Lichess.org → Learn → Study
2. Click "Import PGN"
3. Paste or upload your `.pgn` file
4. Analyze with Stockfish, add comments, share with others

---

## Advanced Features

### Legal Move Validation
Only legal moves are accepted. The system rejects:
- Moves leaving king in check
- Illegal piece movements
- Invalid castling
- Moves violating chess rules

### Board State Tracking
- Automatic check detection
- Checkmate auto-ends game
- Stalemate detection
- Turn enforcement

### Edit Mode
- Edit individual moves by number
- Add more moves after stopping
- Re-validate all edited moves
- Preview before saving

---

For architecture details, see [DESIGN_DOC.md](../DESIGN_DOC.md).  
For development setup, see [docs/DEVELOPMENT.md](DEVELOPMENT.md).

