# sts-utils

Shared STS naming conventions, label validation, address encoding/decoding and
existing unit constants. This is an independent Python project and Git repository.
It requires Python 3.10+ and has no runtime dependencies beyond the standard library.

- Distribution/dependency name: `sts-utils`.
- Python import name: `sts_utils`.
- The only implementation lives in `src/sts_utils/`; consumers must not copy it.

## One-time editable installation

Activate each consuming project's virtual environment, then install this checkout:

```sh
python -m pip install -e /u/dramirez/WORK/sts_tools/sts_utils
```

Use the actual checkout path if it is moved. Multiple virtual environments can
point at the same checkout. Edits take effect without reinstalling; reinstall if
package metadata or dependencies change. No `PYTHONPATH` changes are needed.

In the current `sts_tools` working directory, install the utilities and inspector
in one operation:

```sh
python3 -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install -e ./sts_utils -e ./sts_geo_utils/geo_inspector
```

For PyROOT workflows, use an environment where `import ROOT` already works; a new
virtual environment does not necessarily inherit the external ROOT installation.

The package is not published to an index. Supply its local checkout when installing
consumers; installing a consumer alone cannot fetch this private dependency.

## Use and dependency declarations

```python
from sts_utils.sts_naming import build_module_name_prefix

assert build_module_name_prefix(3, "D", "R", 1, "T", 0) == "M4DR1T0"
assert build_module_name_prefix(3, "D", "R", 1, "T", 0, version="STS8") == "M3DR1T0"
```

Consumers declare their compatible implementation range in `pyproject.toml`:

```toml
[project]
dependencies = ["sts-utils>=0.1.0,<0.2.0"]
```

Package releases (`0.1.0`), naming schemes (`STS8`, `STS3_5`) and packed-address
versions (`0`, `1`) are separate concepts. Naming defaults to `STS3_5`; unsupported
prefix naming versions raise `ValueError` rather than returning `None`. Existing
unit constants and address behavior have otherwise been preserved.

Editable installs deliberately share live changes. For reproducible analyses,
record the naming scheme and exact utilities Git commit; use a non-editable install
of that revision in a separate environment. A compatibility range alone does not
freeze an installation. After the initial migration, commit utilities changes in
this repository, not the surrounding working directory. No remote is configured
and no initial commit is created automatically.

Workspace callers import `sts_utils` directly; the former root-level `utils/`
compatibility package has been removed. Install this checkout in each environment
used by `sts_geo_layout`, `sts_ladder_metrology`, `sts_module_test` or the workspace tests:

```sh
# From the sts_tools working directory, with the intended environment activated:
python -m pip install -e ./sts_utils
```

Use `from sts_utils import sts_naming`, `from sts_utils.sts_naming import ...`, or
`from sts_utils.units import CM, MM`. The application-local
`sts_metrology_db/utils/hashing.py` is unrelated and remains local to that utility.

## Development and packaging

From this project's directory:

```sh
python -m pip install -e '.[test]'
python -m pytest
python -m pip wheel --no-deps . --wheel-dir dist
```

The tests and package work without the surrounding workspace or ROOT. Keep
application-specific dependencies and configuration out of this library.
