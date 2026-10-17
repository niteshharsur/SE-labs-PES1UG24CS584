# Static analysis issue table

Line numbers refer to the original `parcel_tracker.py` in upstream commit
`7a12c93ce109f67f2a8ea24ac7e32b88b716c422`. Findings are ordered with high
and medium security severity first. Pylint categories are not Bandit severities.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| B602: shell injection | Security, High | 55 | A hub address is concatenated into a shell command. | Validate a literal IPv4/IPv6 address, resolve ping's executable, pass an argument list with `shell=False`, and bound execution with a timeout. Use the platform's count option. |
| B306: insecure temporary name | Security, Medium | 50 | `mktemp` returns an unreserved name, allowing a race before the file is created. | Atomically create a file with `mkstemp`, close its descriptor, and return the reserved path; the caller owns cleanup. |
| B311: predictable OTP | Security, Low | 72 | `random.randint` is not suitable for a delivery authentication code. | Use `1000 + secrets.randbelow(9000)` to preserve the four-digit range with cryptographic randomness. |
| B404: subprocess import | Security review, Low | 2 | Process launching requires review even when no shell is used. | Retain necessary ICMP ping functionality; audit the safe call and annotate only B404 and the resulting generic B603 warning, with inline reasons. B602 is fixed, not suppressed. |
| W0102: mutable default | Pylint warning | 11 | The default history list is shared across independent bookings. | Default to `None` and create a fresh list for each call, while still appending to an explicitly provided list. |
| W0718: broad exception | Pylint warning | 37 | Catching `Exception` can conceal errors unrelated to a missing tracking ID. | Catch only `KeyError`; let unexpected errors propagate. |
| C0103: naming | Pylint convention | 11-67 | Function, argument, and local names use camelCase. | Rename functions and their callers to snake_case; use `PARCELS` for the module-level store. |
| C0114/C0116: missing documentation | Pylint convention | 1, 11-58 | The module and functions lack docstrings. | Document purpose, behavior, and helper ownership/input requirements. |
| R1714: repeated comparison | Pylint refactor | 45 | Two equality comparisons repeat the same status variable. | Use membership in a tuple of courier statuses. |
| E225: operator spacing | Flake8 style | 28 | `cost=50` lacks spaces around `=`. | Use `cost = 50`. |
| E261: inline comment spacing | Flake8 style | 71 | The comment has only one preceding space. | Insert two spaces before the inline comment. |
| E231: comma spacing | Flake8 style | 74 | A print argument lacks a space after its comma. | Insert one space after the comma. |
| E305: top-level spacing | Flake8 style | 75 | The main call immediately follows a function body. | Separate the top-level entry-point guard with two blank lines. |

## Targeted security review

The standard-library subprocess import and a subprocess call without a shell
trigger broad Bandit review rules B404/B603. The two narrowly scoped `nosec`
annotations record that review; no tool configuration or global skips are used.
The executable is resolved from the local system PATH (assumed trusted), and the
hub must be a literal IP address. Shell fragments, options, and hostnames are
rejected before launching a process. The original command-injection finding
B602 is removed by the implementation. This review does not claim that running
an arbitrary executable from an untrusted PATH would be safe.
