# PyPI Publishing Checklist

## Package Verification

Package successfully built and verified:
- `chess_pgn_recorder-0.1.1a1-py3-none-any.whl` (21K)
- `chess_pgn_recorder-0.1.1a1.tar.gz` (37K)
- Twine check passed
- All 46 tests passing

## Pre-Publication Checklist

### Package Metadata
- [x] Package name: `chess-pgn-recorder`
- [x] Version: `0.1.1a1` (alpha)
- [x] Description: Clear and concise
- [x] README.md: Comprehensive with examples
- [x] LICENSE: Apache 2.0
- [x] Author name: Lalatendu Mohanty
- [x] Author email: lala.mohanty@gmail.com
- [x] Python version requirement: >=3.8
- [x] Dependencies: `chess>=1.10.0`
- [x] Keywords: chess, pgn, algebraic-notation, etc.
- [x] Classifiers: Development Status, License, Python versions
- [x] Entry point: `chess-pgn-recorder` command
- [x] Project URLs: Repository, Documentation, Issues

### Build Configuration
- [x] Build system: Hatchling
- [x] Source layout: `src/` directory
- [x] Package includes: All Python files, docs, examples
- [x] Tests: Separate `tests/` directory
- [x] Clean build: No artifacts or cache files

### Documentation
- [x] README.md: Installation, usage, examples
- [x] CONTRIBUTING.md: Developer guidelines
- [x] CHANGELOG.md: Version history
- [x] DESIGN_DOC.md: Technical documentation
- [x] RELEASE.md: Detailed release process
- [x] PYPI_SETUP.md: Quick start guide
- [x] LICENSE: Apache 2.0 license file

### Code Quality
- [x] All tests passing (46/46)
- [x] Test coverage: 84-91%
- [x] No linter errors
- [x] Type hints present
- [x] Code formatted with Black
- [x] No inline comments

### CI/CD
- [x] GitHub Actions CI: Multi-version testing
- [x] GitHub Actions Publish: Automated PyPI publishing
- [x] Badges in README
- [x] All workflows configured

## First-Time PyPI Setup

### 1. Create Accounts (if not done)
- [ ] TestPyPI account: https://test.pypi.org/account/register/
- [ ] PyPI account: https://pypi.org/account/register/

### 2. Generate API Tokens
- [ ] TestPyPI token generated
- [ ] PyPI production token generated

### 3. Add GitHub Secrets
- [ ] `TEST_PYPI_API_TOKEN` added to repository secrets
- [ ] `PYPI_API_TOKEN` added to repository secrets

### 4. Configure Local Publishing (optional)
- [ ] Create `~/.pypirc` with tokens
- [ ] Test Hatch publishing commands

## Publishing Steps

### Test Release to TestPyPI

```bash
# 1. Build
rm -rf dist/
hatch build

# 2. Check
twine check dist/*

# 3. Publish to TestPyPI
hatch publish -r test
# OR: twine upload --repository testpypi dist/*

# 4. Test installation
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            chess-pgn-recorder

# 5. Verify
chess-pgn-recorder
```

### Production Release to PyPI

**ONLY after successful TestPyPI verification!**

```bash
# Publish to PyPI
hatch publish
# OR: twine upload dist/*
```

## Post-Publication

- [ ] Verify on PyPI: https://pypi.org/project/chess-pgn-recorder/
- [ ] Test installation: `pip install chess-pgn-recorder`
- [ ] Test CLI: `chess-pgn-recorder`
- [ ] Create GitHub release
- [ ] Update version for next development cycle
- [ ] Tweet/announce (optional)

## Quick Commands

```bash
# Full release process
rm -rf dist/
hatch run check-all      # Tests, lint, typecheck
hatch build              # Build wheel and sdist
twine check dist/*       # Verify package
hatch publish -r test    # Upload to TestPyPI
hatch publish            # Upload to PyPI (after testing)
```

## Important Notes

**IMPORTANT:**
- Cannot re-upload same version - Once published, a version is permanent
- Test first - Always test on TestPyPI before production
- Tag releases - Create git tags for version tracking
- Update CHANGELOG - Document all changes before release

## Next Steps After First Release

1. Monitor downloads and feedback
2. Address any installation issues
3. Plan next version features
4. Continue regular releases
5. Build community and gather feedback

## Resources

- **PyPI Project Page**: https://pypi.org/project/chess-pgn-recorder/
- **TestPyPI Project Page**: https://test.pypi.org/project/chess-pgn-recorder/
- **Packaging Guide**: https://packaging.python.org/
- **PEP 517**: https://peps.python.org/pep-0517/
- **PEP 440**: https://peps.python.org/pep-0440/

