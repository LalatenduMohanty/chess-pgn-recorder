# Release Guide for Chess PGN Recorder

This guide explains how to build and publish Chess PGN Recorder to PyPI.

## Prerequisites

### 1. PyPI Account Setup

Create accounts on both platforms:
- **TestPyPI** (for testing): https://test.pypi.org/account/register/
- **Production PyPI**: https://pypi.org/account/register/

### 2. API Tokens

Generate API tokens for secure publishing:

**TestPyPI:**
1. Go to https://test.pypi.org/manage/account/token/
2. Create a new API token with scope: "Entire account"
3. Copy the token (starts with `pypi-`)
4. Save it securely

**Production PyPI:**
1. Go to https://pypi.org/manage/account/token/
2. Create a new API token with scope: "Entire account"
3. Copy the token
4. Save it securely

### 3. Install Build Tools

```bash
pip install --upgrade build twine hatch
```

## Building the Package

### Step 1: Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf dist/ build/ *.egg-info
```

### Step 2: Update Version

Update version in three places:
1. `pyproject.toml` - `version = "0.1.1a1"`
2. `src/__init__.py` - `__version__ = '0.1.1-alpha'`
3. `CHANGELOG.md` - Add new version section

### Step 3: Run Tests

```bash
hatch run test-cov
```

All tests must pass before releasing!

### Step 4: Build the Distribution

Using Hatch (recommended):
```bash
hatch build
```

Or using build directly:
```bash
python -m build
```

This creates:
- `dist/chess_pgn_recorder-0.1.1a1-py3-none-any.whl` (wheel)
- `dist/chess_pgn_recorder-0.1.1a1.tar.gz` (source)

### Step 5: Verify the Build

```bash
# Check the package
twine check dist/*

# List contents
tar -tzf dist/chess_pgn_recorder-*.tar.gz
```

## Publishing to PyPI

### Test on TestPyPI First (Recommended)

**Step 1: Upload to TestPyPI**
```bash
twine upload --repository testpypi dist/*
```

When prompted:
- Username: `__token__`
- Password: Your TestPyPI API token

Or configure in `~/.pypirc`:
```ini
[testpypi]
username = __token__
password = pypi-your-testpypi-token-here
```

Then:
```bash
twine upload --repository testpypi dist/*
```

**Step 2: Test Installation from TestPyPI**
```bash
# Create a test environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ chess-pgn-recorder

# Test the installation
chess-pgn-recorder --help
python -c "from src import __version__; print(__version__)"

# Deactivate and remove test environment
deactivate
rm -rf test_env
```

### Publish to Production PyPI

**ONLY after testing on TestPyPI!**

```bash
twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: Your PyPI API token

Or configure in `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-your-production-token-here
```

**Verify on PyPI:**
- Visit: https://pypi.org/project/chess-pgn-recorder/
- Check metadata, description, and download links

**Test Installation:**
```bash
pip install chess-pgn-recorder
chess-pgn-recorder
```

## Using Hatch for Publishing

Hatch can handle everything:

```bash
# Build
hatch build

# Publish to TestPyPI
hatch publish -r test

# Publish to PyPI (production)
hatch publish
```

Configure `~/.pypirc` for Hatch:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-production-token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-testpypi-token
```

## Automated Release with GitHub Actions

See `.github/workflows/publish.yml` for automated releases triggered by tags.

To create a release:
```bash
# Create and push a tag
git tag v0.1.1-alpha
git push origin v0.1.1-alpha
```

GitHub Actions will automatically:
1. Run all tests
2. Build the package
3. Publish to PyPI

## Post-Release Checklist

- [ ] Package appears on PyPI: https://pypi.org/project/chess-pgn-recorder/
- [ ] Installation works: `pip install chess-pgn-recorder`
- [ ] Command works: `chess-pgn-recorder`
- [ ] Update GitHub release notes
- [ ] Update version badges in README
- [ ] Announce release (if applicable)

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **Alpha**: `0.1.0a1`, `0.1.1a1`, etc.
- **Beta**: `0.1.0b1`, `0.1.1b1`, etc.
- **Release Candidate**: `0.1.0rc1`
- **Stable**: `0.1.0`, `1.0.0`, etc.

For pyproject.toml, use PEP 440 format:
- `0.1.1a1` for alpha
- `0.1.1b1` for beta
- `0.1.1rc1` for release candidate
- `0.1.1` for stable

## Troubleshooting

### "File already exists" Error
You cannot re-upload the same version. Options:
1. Increment the version number
2. Delete the release from PyPI (only for test releases)
3. Use a post-release version: `0.1.1a1.post1`

### Import Error After Installation
Check that:
- `src/__init__.py` exists
- Entry point in `pyproject.toml` is correct: `src.chess_pgn:main`
- Package structure is correct

### Missing Dependencies
Ensure `chess>=1.10.0` is in `pyproject.toml` dependencies.

### README Not Showing on PyPI
- Ensure `readme = "README.md"` in `pyproject.toml`
- README must be valid Markdown
- Check for rendering errors with: `twine check dist/*`

## Resources

- **PyPI Documentation**: https://packaging.python.org/
- **PEP 440** (Version Identification): https://peps.python.org/pep-0440/
- **PEP 517** (Build System): https://peps.python.org/pep-0517/
- **Hatch Documentation**: https://hatch.pypa.io/
- **Twine Documentation**: https://twine.readthedocs.io/

