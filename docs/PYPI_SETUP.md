# PyPI Publishing Quick Start Guide

## One-Time Setup

### 1. Create PyPI Accounts
- TestPyPI: https://test.pypi.org/account/register/
- PyPI: https://pypi.org/account/register/

### 2. Generate API Tokens

**TestPyPI:**
- Go to: https://test.pypi.org/manage/account/token/
- Create token with scope "Entire account"  
- Save as: `TEST_PYPI_API_TOKEN`

**PyPI:**
- Go to: https://pypi.org/manage/account/token/
- Create token with scope "Entire account"
- Save as: `PYPI_API_TOKEN`

### 3. Add Secrets to GitHub

Go to your repository: Settings → Secrets and variables → Actions

Add two secrets:
- `TEST_PYPI_API_TOKEN` = your TestPyPI token
- `PYPI_API_TOKEN` = your PyPI production token

### 4. Install Build Tools

```bash
pip install --upgrade hatch twine build
```

## Quick Release Process

### Method 1: Manual Release

```bash
# 1. Update version in 3 places:
#    - pyproject.toml: version = "0.1.2a1"
#    - src/__init__.py: __version__ = '0.1.2-alpha'
#    - CHANGELOG.md: Add [0.1.2-alpha] section

# 2. Run all checks
hatch run check-all

# 3. Clean and build
rm -rf dist/
hatch build

# 4. Check the build
twine check dist/*

# 5. Test on TestPyPI first
hatch publish -r test

# 6. Test installation
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ chess-pgn-recorder

# 7. If all good, publish to PyPI
hatch publish
```

### Method 2: GitHub Release (Automated)

```bash
# 1. Update version and commit changes
git add .
git commit -m "chore: bump version to 0.1.2-alpha"
git push

# 2. Create and push a tag
git tag v0.1.2-alpha
git push origin v0.1.2-alpha

# 3. Create GitHub Release
#    Go to: https://github.com/yourusername/chess_pgn_recorder/releases/new
#    - Choose the tag: v0.1.2-alpha
#    - Title: v0.1.2-alpha
#    - Description: Copy from CHANGELOG.md
#    - Click "Publish release"

# GitHub Actions will automatically build and publish to PyPI!
```

### Method 3: Manual Trigger (for testing)

```bash
# Go to: https://github.com/yourusername/chess_pgn_recorder/actions
# Click on "Publish to PyPI" workflow
# Click "Run workflow"
# Choose target: testpypi or pypi
# Click "Run workflow"
```

## Version Numbering Guide

```
Alpha:   0.1.0a1, 0.1.1a1, 0.1.2a1
Beta:    0.1.0b1, 0.1.1b1, 0.1.2b1
RC:      0.1.0rc1, 0.1.1rc1
Stable:  0.1.0, 0.1.1, 0.2.0, 1.0.0
```

**Update in 3 places:**
1. `pyproject.toml` - PEP 440 format: `0.1.2a1`
2. `src/__init__.py` - Semantic: `0.1.2-alpha`
3. `CHANGELOG.md` - Semantic: `[0.1.2-alpha]`

## Pre-Release Checklist

- [ ] All tests passing: `hatch run test`
- [ ] Code formatted: `hatch run format`
- [ ] Linting passes: `hatch run lint`
- [ ] Type checking: `hatch run typecheck`
- [ ] Version updated in 3 files
- [ ] CHANGELOG.md updated
- [ ] README.md reviewed
- [ ] Test on TestPyPI first

## Post-Release Checklist

- [ ] Verify on PyPI: https://pypi.org/project/chess-pgn-recorder/
- [ ] Test installation: `pip install chess-pgn-recorder`
- [ ] Test CLI: `chess-pgn-recorder`
- [ ] Create GitHub release with notes
- [ ] Update badges if needed
- [ ] Announce (optional)

## Common Commands

```bash
# Build and check
hatch build
twine check dist/*

# Publish to TestPyPI
hatch publish -r test

# Publish to PyPI  
hatch publish

# Or use twine directly
twine upload --repository testpypi dist/*
twine upload dist/*
```

## Configure ~/.pypirc (Optional)

Create `~/.pypirc` for easier publishing:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-production-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-testpypi-token-here
```

Then you can use:
```bash
hatch publish              # PyPI
hatch publish -r test      # TestPyPI
```

## Troubleshooting

**"File already exists" error:**
- You cannot re-upload the same version
- Increment version number

**Package not found after upload:**
- Wait a few minutes for PyPI to process
- Check spelling: `chess-pgn-recorder` (with hyphens)

**Import error:**
- Ensure `src/__init__.py` exists
- Check entry point in `pyproject.toml`

**Dependencies not installing:**
- Verify `dependencies = ["chess>=1.10.0"]` in `pyproject.toml`

## Resources

- PyPI: https://pypi.org/project/chess-pgn-recorder/
- TestPyPI: https://test.pypi.org/project/chess-pgn-recorder/
- Full guide: See `RELEASE.md`
- Packaging docs: https://packaging.python.org/

