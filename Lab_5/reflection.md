# Lab 5 reflection

The supplied three-page handout requests reflection answers, and the source
README refers to four questions, but neither includes the actual questions.
The following four topic-based draft responses cover the lab's learning
outcomes. They are not presented as quotations of missing questions or as a
claim about the student's personal experience; review them before submission.

## 1. What did the three tools contribute?

Pylint identified quality and maintainability problems, including the shared
mutable default, broad exception handling, missing documentation, inconsistent
naming, and repeated comparisons. Bandit identified security risks in shell
execution, temporary-file creation, and OTP randomness. Flake8 identified
spacing and layout errors. Their different scopes made the combined review
more useful than relying on a single score.

## 2. Which findings deserved priority, and how were they fixed?

The high-severity shell-injection issue was addressed first by rejecting
non-IP inputs and passing a validated address to a resolved ping executable
without a shell. The medium-severity temporary-name race was fixed using
atomic file creation. Cryptographic randomness replaced the predictable OTP
generator. The shared default list and overly broad exception handling were
then corrected before the remaining style cleanup.

## 3. How was correctness checked after the changes?

The original demo output and all three baseline reports were saved before
editing. The tools were rerun after the relevant changes and again on the
final file. The final Pylint score is 10.00/10, Flake8 emits no findings, and
Bandit reports no unreviewed findings. Two specific generic subprocess
review warnings are documented inline; they are not blanket disables.
Regression tests compare the demo with its original output except for the
random OTP and check status boundaries, prices, history behavior, temporary
files, safe process arguments, malicious inputs, errors, and import behavior.

## 4. What are the limitations, and how should static analysis be used?

A clean report cannot prove business correctness or complete security.
The tools do not establish correct shipping rules, delivery policies,
OTP expiry, or rate limits. Their findings need contextual review: a
subprocess import is a review prompt, while a shell command containing
untrusted input is a concrete vulnerability. Static analysis should run
alongside tests and code review, with narrowly justified exceptions rather
than hiding whole classes of findings to improve a score.
