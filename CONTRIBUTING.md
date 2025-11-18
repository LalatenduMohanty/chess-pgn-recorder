# Contributing to Chess PGN Recorder

Thank you for your interest in contributing to Chess PGN Recorder! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Getting Started

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/chess_pgn_recorder.git
   cd chess_pgn_recorder
   ```

2. **Install Hatch** (recommended)
   ```bash
   pip install hatch
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

## Development Workflow

### Running Tests

Always run tests before submitting a pull request:

```bash
# Run all tests
hatch run test

# Run tests with coverage
hatch run test-cov

# Run verbose tests
hatch run test-verbose
```

### Code Quality Checks

We use several tools to maintain code quality:

```bash
# Run all quality checks
hatch run check-all

# Or run individually:
hatch run lint         # Flake8 linting
hatch run typecheck    # Mypy type checking
hatch run format-check # Black formatting check
```

### Auto-formatting Code

Format your code with Black before committing:

```bash
hatch run format
```

## Code Standards

### Style Guidelines
- **Line length**: Maximum 127 characters (Flake8) / 100 (Black)
- **Complexity**: Keep functions simple (max complexity: 10)
- **Docstrings**: Use Google-style docstrings for all public functions and classes
- **Type hints**: Encouraged for function signatures
- **Comments**: Avoid inline comments; use docstrings and clear variable names

### Example Function

```python
def validate_move(move: str, color: str) -> tuple[bool, str]:
    """
    Validate a chess move in algebraic notation.
    
    Args:
        move: The move in algebraic notation (e.g., 'e4', 'Nf3')
        color: The color of the player ('white' or 'black')
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    pass
```

## Testing Guidelines

### Writing Tests
- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Follow the existing test structure

### Test Organization
```
tests/
└── test_chess_pgn.py
    ├── TestMoveValidator
    ├── TestChessGame
    ├── TestPGNExporter
    └── TestIntegration
```

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following the style guidelines
   - Add tests for new functionality
   - Update documentation if needed

3. **Run all checks**
   ```bash
   hatch run check-all
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format
Follow conventional commits format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `style:` Code style changes (formatting, etc.)
- `chore:` Maintenance tasks

### Pull Request Checklist
- [ ] Tests pass (`hatch run test`)
- [ ] Code is formatted (`hatch run format`)
- [ ] Linting passes (`hatch run lint`)
- [ ] Type checking passes (`hatch run typecheck`)
- [ ] Documentation is updated (if applicable)
- [ ] CHANGELOG.md is updated (for significant changes)

## Continuous Integration

All pull requests must pass CI checks:
- **Tests**: Run on Python 3.8, 3.9, 3.10, 3.11, and 3.12
- **Linting**: Flake8 code quality checks
- **Type Checking**: Mypy type validation
- **Formatting**: Black code style verification

The CI pipeline runs automatically on all pull requests.

## Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

## Questions?

Feel free to open an issue for questions or discussions about:
- Feature requests
- Bug reports
- Development questions
- Documentation improvements

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

