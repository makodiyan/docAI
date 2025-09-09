# Developer Setup Guide – docAI Monorepo

Welcome to **docAI**.  
This repository is organized as a **monorepo** that will eventually contain **many services** (microservices) and **many shared libraries**.

- A **service** represents one microservice in the docAI architecture (example: `excel_preprocess`).  
- A **library** represents reusable functionality shared across services (example: `file_name_check`).

This guide explains how to set up your local development environment so you can work with **all services and libraries** consistently.

---

## 1. Clone the Repository
```bash
git clone https://github.com/makodiyan/docAI.git
cd docAI
```

---

## 2. Install Miniforge
We standardize on **Miniforge** (a minimal Conda distribution with `conda-forge` as the default channel).

- **macOS/Linux**:  
  Download from Miniforge releases and install. Example:
  ```bash
  curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
  bash Miniforge3-MacOSX-arm64.sh
  ```

- **Windows**:  
  Download the `.exe` installer from Miniforge releases and run it.  
  Make sure “Add conda to PATH” is enabled.

Restart your terminal after install.

---

## 3. Create the Conda Environment
From the repo root:

```bash
conda env update -f environment.yml --prune
conda activate docAI
```

Check:
```bash
which python   # macOS/Linux
where python   # Windows
```
It should point into `.../envs/docAI/bin/python` (Unix) or `...\envs\docAI\python.exe` (Windows).

---

## 4. Install Editable Packages
We use **editable installs** so that code changes in services and libraries take effect immediately without re-installing.


As the repo grows, you will add more services under `services/` and more libraries under `libs/`.  
Each one should be added to the `pip:` section of `environment.yml` like this:

```yaml
- -e ./services/new_service
- -e ./libs/new_library
```

Then update your env:
```bash
conda env update -f environment.yml --prune
```

---

## 5. VS Code Setup
1. Open VS Code at the repo root:
   ```bash
   code docAI
   ```
   (or open `docAI.code-workspace` at root)

2. Select the interpreter:
   - Press `Ctrl+Shift+P` / `Cmd+Shift+P`
   - Choose **Python: Select Interpreter**
   - Pick the `docAI` conda environment.

3. Recommended extensions:
   - **Python** (ms-python.python)
   - **Pylance** (ms-python.vscode-pylance)
   - **Black Formatter** (ms-python.black-formatter)
   - **Ruff** (charliermarsh.ruff)

---

## 6. VS Code Configurations
We provide root-level configs under `.vscode/`.

- **settings.json** → pins the Python interpreter and enables pytest.  
- **launch.json** → debug configs for services, libraries, and pytest.  
- **tasks.json** → helper tasks for installing/editable installs, running tests, linting, formatting.

---

## 7. Pre-commit Hooks
We enforce code quality with **Black** (formatting) and **Ruff** (linting).

### One-time setup:
```bash
pip install pre-commit
pre-commit install
```

### Run checks manually:
```bash
pre-commit run --all-files
```

> Pre-commit will also run automatically on every `git commit`.

---

## 8. Running & Debugging

### Run an example service
```bash
python -m excel_preprocess.main
```
Or in VS Code: **Run → Start Debugging → 🐍 Run excel_preprocess.main**

### Run tests
```bash
pytest -q services libs
```
Or in VS Code:  
**Run → Start Debugging → 🧪 Pytest: services + libs**

---

## 9. Locking Dependencies
We keep two env files:
- `environment.yml` → editable by humans, loose pins (`>=`).  
- `environment.lock.yml` → generated snapshot of exact versions.

When you add a dependency:
```bash
conda env update -f environment.yml --prune
conda env export > environment.lock.yml
```

Commit **both files**.

This will make sure that all our installs use the correct versions of the dependencies.

---

## 10. Common Issues

- **Imports not found**  
  → Ensure you ran `pip install -e ...` for all services/libs.  
  → Confirm VS Code is using the `docAI` environment.

- **Tests not discovered**  
  → Ensure tests live under a `tests/` directory, and test files start with `test_`.

- **Extra packages in your env**  
  → Run `conda env update -f environment.yml --prune` to clean.

---

## 11. Adding New Services & Libraries
As the architecture grows, follow this pattern:

### Add a new service
```
services/new_service/
  pyproject.toml
  src/new_service/__init__.py
  src/new_service/main.py
  tests/test_main.py
```
Then add:
```yaml
- -e ./services/new_service
```
to `environment.yml`.

### Add a new library
```
libs/new_library/
  pyproject.toml
  src/new_library/__init__.py
  src/new_library/core.py
  tests/test_core.py
```
Then add:
```yaml
- -e ./libs/new_library
```
to `environment.yml`.

Update and reinstall:
```bash
conda env update -f environment.yml --prune
```

---

With this setup, you can develop, debug, and test **multiple services and libraries** in the monorepo.
