# Community Solar Credit Allocation Manager

## Lab 1 - Requirements Engineering & UML Use-Case Modelling

Problem Statement #63

## Problem Overview

This Requirements Engineering and UML lab defines a community-solar system that ingests rooftop solar generation metrics, facilitates peer-to-peer solar-credit transfers, and tracks monthly utility billing offsets. It contains deliverable artifacts only; it is not a software application.

## Actors

- Prosumer Resident
- Co-op Manager
- Smart Meter System

## Functional Requirements

- **FR-001:** Record solar generation units and support surplus-credit transfers to neighbor accounts.
- **FR-002:** Allow a Prosumer Resident to view the current solar-credit balance.
- **FR-003:** Allow a Prosumer Resident to initiate a peer-to-peer solar-credit transfer.
- **FR-004:** Calculate and display the monthly utility billing offset.
- **FR-005:** Allow the Co-op Manager to review community balances and transfer records.

## Non-Functional Requirements

- **NFR-001:** Validate and store hourly generation data for 500 households with 99.9% uptime.
- **NFR-002:** Protect credit and billing records from unauthorized modification and audit every successful transfer.

## Use Cases

- UC-01 - Record Solar Generation
- UC-02 - View Credit Balance
- UC-03 - Transfer Solar Credits
- UC-04 - Track Monthly Billing Offset
- UC-05 - Review Community Credit Activity
- UC-06 - Validate Credit Balance
- UC-07 - Handle Insufficient Credit Balance

## UML Relationships

`UC-03 <<include>> UC-06` means every transfer validates the source credit balance.

`UC-07 <<extend>> UC-03` means insufficient-credit handling occurs only when a requested transfer exceeds the available balance.

## Deliverables

| File | Purpose |
|---|---|
| `requirements/requirements.md` | Complete functional and non-functional requirement specification. |
| `requirements/requirements.csv` | Requirements in CSV format. |
| `uml/community_solar_use_case.puml` | PlantUML source for the use-case model. |
| `uml/community_solar_use_case.svg` | Rendered scalable use-case diagram. |
| `uml/community_solar_use_case.png` | Rendered PNG use-case diagram. |
| `use-case-flow/UC-03_Transfer_Solar_Credits.md` | UC-03 flow specification. |
| `use-case-flow/UC-03_Transfer_Solar_Credits.pdf` | Clean one-page PDF version of UC-03. |
| `traceability/requirements_traceability.md` | Requirement-to-use-case mapping. |
| `validate_lab1.py` | Deliverable validation script. |

## How to Render UML

With PlantUML installed, run the following from this project directory:

```bash
plantuml -tsvg uml/community_solar_use_case.puml
plantuml -tpng uml/community_solar_use_case.puml
```

Alternatively, run `java -jar plantuml.jar -tsvg uml/community_solar_use_case.puml` and repeat with `-tpng`.
