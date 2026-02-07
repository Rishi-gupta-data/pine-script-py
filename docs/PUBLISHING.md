# Publishing Pinepy to PyPI

This guide covers PyPI publishing via the standard build + twine flow.

## 1) Create a PyPI account
- Create an account on PyPI and verify email.
- Optional: enable 2FA.

## 2) Create a project token
- In PyPI, create an API token scoped to your project.
- Save the token securely.

## 3) Build the package
From the project root:
```
python -m pip install --upgrade build
python -m build
```
This produces `dist/*.whl` and `dist/*.tar.gz`.

## 4) Upload
```
python -m pip install --upgrade twine
python -m twine upload dist/*
```
When prompted for username, use `__token__`. For password, paste the token.

## 5) Verify
- Check the project page on PyPI.
- Try `pip install pinepy` in a clean env.

## Optional: TestPyPI first
```
python -m twine upload --repository testpypi dist/*
python -m pip install -i https://test.pypi.org/simple/ pinepy
```

## Common issues
- Version already exists: bump `version` in `pyproject.toml`.
- Missing files: check `MANIFEST.in` or package discovery.
