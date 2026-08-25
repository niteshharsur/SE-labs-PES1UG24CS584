"""Validate the required Lab 1 Requirements Engineering and UML deliverables."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent


def read(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.is_file():
        raise FileNotFoundError(f"Missing required file: {relative_path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    problems: list[str] = []
    try:
        requirements = read("requirements/requirements.md")
        diagram = read("uml/community_solar_use_case.puml")
        flow = read("use-case-flow/UC-03_Transfer_Solar_Credits.md")
    except FileNotFoundError as error:
        print(error)
        return 1

    fr_ids = sorted(set(re.findall(r"^### (FR-\d{3})$", requirements, re.MULTILINE)))
    nfr_ids = sorted(set(re.findall(r"^### (NFR-\d{3})$", requirements, re.MULTILINE)))
    if fr_ids != [f"FR-{number:03d}" for number in range(1, 6)]:
        problems.append(f"Expected exactly FR-001 through FR-005; found: {', '.join(fr_ids) or 'none'}")
    if nfr_ids != ["NFR-001", "NFR-002"]:
        problems.append(f"Expected exactly NFR-001 and NFR-002; found: {', '.join(nfr_ids) or 'none'}")

    for req_id in fr_ids + nfr_ids:
        section = re.search(rf"### {req_id}\n(.*?)(?=\n### |\Z)", requirements, re.DOTALL)
        if not section or any(field not in section.group(1) for field in ("**Description:**", "**Priority:**", "**Acceptance Criteria:**", "**Rationale:**")):
            problems.append(f"{req_id} is missing one or more required fields")

    actor_count = len(re.findall(r'^actor "', diagram, re.MULTILINE))
    use_case_count = len(re.findall(r'^    usecase "', diagram, re.MULTILINE))
    if actor_count < 3:
        problems.append(f"Expected at least 3 actors; found {actor_count}")
    if use_case_count < 5:
        problems.append(f"Expected at least 5 use cases; found {use_case_count}")
    if "<<include>>" not in diagram:
        problems.append("Missing <<include>> relationship")
    if "<<extend>>" not in diagram:
        problems.append("Missing <<extend>> relationship")
    if "UC-03" not in diagram:
        problems.append("Missing UC-03 in UML diagram")
    if "Main Success Scenario" not in flow:
        problems.append("Missing Main Success Scenario in UC-03 flow")
    if "Alternate Flow" not in flow:
        problems.append("Missing Alternate Flow in UC-03 flow")

    if problems:
        print("LAB 1 VALIDATION FAILED")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("LAB 1 VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
