# Lab 5: Static Code Analysis

## Scope and evidence

The source is `SETAPESU26/L5_35_parcel_tracker`, upstream commit
`7a12c93ce109f67f2a8ea24ac7e32b88b716c422`. Its script matched the supplied
ZIP before editing. The original program was run before analysis.

| Check | Before | Final |
|-------|--------|-------|
| Pylint | 4.91/10; 27 messages | 10.00/10; no messages |
| Bandit | 1 High, 1 Medium, 2 Low | No unreviewed findings; two specific reviewed subprocess annotations |
| Flake8 | 4 findings | No findings (empty report is the tool's success output) |
| Functional regression checks | Original demo output saved | 8 tests pass; demo matches except random OTP |

`issues.md` contains the required issue table with original line numbers and
fix approaches. `reflection.md` provides four draft thematic reflections and
explicitly records that the referenced reflection questions are missing
from the supplied materials.

## Three separate fix commits

1. **Fix Bandit security findings in parcel tracker:** preserve all original
   reports and demo output; fix shell injection, temporary-file creation, and
   OTP randomness; record issue inventory and the targeted subprocess review.
2. **Fix Pylint quality findings and reach 10.00 out of 10:** remove the shared
   mutable default, narrow exception handling, standardize names, add
   docstrings, simplify status comparison, and save the intermediate report.
3. **Fix Flake8 formatting and complete Lab 5 evidence:** correct spacing,
   indentation, and line lengths; add an entry-point guard, final reports,
   regression checks, reproducible tool versions, and reflections.

## Reports

- `reports/before/`: original `pylint_report.txt`, `bandit_report.txt`,
  `flake8_report.txt`, and `demo_output.txt`.
- `reports/after-bandit/bandit_report.txt`: security-phase verification.
- `reports/after-pylint/pylint_report.txt`: quality-phase verification.
- `reports/after/`: final reports for all three tools and the final demo.
- Root `pylint_report.txt`, `bandit_report.txt`, and `flake8_report.txt`:
  exact copies of the final reports for the handout's required filenames.
- `regression_report.txt`: the executed regression test results.

Reports were produced with Python 3.12.14 on Windows, Pylint 4.1.3,
Bandit 1.9.4, and Flake8 7.4.1. Bandit report timestamps are UTC.
Analysis targets `parcel_tracker.py`, as specified by the handout.

## Reproduce

Run these commands from the lab folder. Windows PowerShell uses the activation
line below; on Linux/macOS use `source venv/bin/activate` instead.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python parcel_tracker.py
python -m pylint --persistent=n parcel_tracker.py > pylint_report.txt
python -m bandit -r parcel_tracker.py -f txt > bandit_report.txt
python -m flake8 parcel_tracker.py > flake8_report.txt
python -m unittest discover -s tests -v
```

`--persistent=n` only prevents Pylint from writing its user cache; it does not
change the checks or scoring. No analysis rules were globally disabled.
The installed virtual environment is intentionally excluded from submission.

## Deliberate behavior changes

The demonstration's routes, stages, prices, and unknown-ID message are
preserved. The OTP remains four digits but uses cryptographic randomness.
Public function names now use snake_case. Importing the module no longer
runs the demo. `label_path` creates the file atomically rather than returning
an unreserved name; the caller removes it when finished. `ping_hub` accepts
literal IPv4/IPv6 addresses, rejects hostnames and shell fragments, resolves
the system ping from a trusted PATH, handles Windows and POSIX count flags,
and imposes a ten-second process timeout. These helper changes are documented
and tested; no ping to an external hub is needed for the regression suite.
