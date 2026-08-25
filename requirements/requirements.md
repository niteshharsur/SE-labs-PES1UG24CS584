# Requirements Specification

## Functional Requirements

### FR-001
- **Type:** Functional
- **Description:** The system shall record solar generation units (kWh) from smart-meter feeds and allow prosumers to transfer surplus credits to neighbor accounts.
- **Priority:** High
- **Acceptance Criteria:** **PASS** if an hourly smart-meter feed containing a valid household identifier, timestamp, and kWh value is stored with the corresponding account, and a surplus-credit transfer can be initiated from that account to a valid neighbor account. **FAIL** if either the valid feed is not stored or the transfer cannot be initiated.
- **Rationale:** Accurate generation records establish the credit balance from which community transfers are made.

### FR-002
- **Type:** Functional
- **Description:** The system shall allow a Prosumer Resident to view their current solar credit balance.
- **Priority:** High
- **Acceptance Criteria:** **PASS** if an authenticated Prosumer Resident can open the balance view and it displays the account's current credit balance in kWh. **FAIL** if the balance is absent, does not match the stored balance, or is visible to an unauthenticated user.
- **Rationale:** Residents need a clear view of available credits before deciding whether to transfer them.

### FR-003
- **Type:** Functional
- **Description:** The system shall allow a Prosumer Resident to initiate a peer-to-peer solar credit transfer to a neighbor account.
- **Priority:** High
- **Acceptance Criteria:** **PASS** if an authenticated Prosumer Resident can submit a valid neighbor account and a positive transfer amount, and the system begins the transfer validation process. **FAIL** if valid transfer details cannot be submitted or validation is not started.
- **Rationale:** Peer-to-peer transfer is the central community-sharing capability of the system.

### FR-004
- **Type:** Functional
- **Description:** The system shall calculate and display the monthly utility billing offset produced by solar credits applied to an account.
- **Priority:** Medium
- **Acceptance Criteria:** **PASS** if the account view displays the billing-period credit total and resulting monthly utility billing offset, calculated from credits applied during that period. **FAIL** if either value is unavailable or the displayed offset differs from the configured billing calculation.
- **Rationale:** Billing offsets show residents the financial effect of their solar participation.

### FR-005
- **Type:** Functional
- **Description:** The system shall allow the Co-op Manager to review community solar credit balances and transfer records.
- **Priority:** Medium
- **Acceptance Criteria:** **PASS** if an authenticated Co-op Manager can retrieve a community view containing household credit balances and transfer records with source, destination, amount, and timestamp. **FAIL** if any of those record fields or balances cannot be reviewed.
- **Rationale:** The co-op needs oversight to support transparent, accountable credit allocation.

## Non-Functional Requirements

### NFR-001
- **Type:** Non-Functional
- **Description:** The smart-meter telemetry processing pipeline shall validate and store hourly generation data for 500 households with 99.9% uptime.
- **Priority:** High
- **Acceptance Criteria:** **PASS** if a 500-household hourly telemetry test validates and stores all valid records, and monitored pipeline availability is at least 99.9% over a calendar month. **FAIL** if a valid tested record is not stored or availability is below 99.9%.
- **Rationale:** Reliable telemetry is necessary for trustworthy balances at community scale.

### NFR-002
- **Type:** Non-Functional
- **Description:** The system shall protect solar-credit and billing-offset records from unauthorized modification and shall log every successful credit transfer with its source account, destination account, amount, and timestamp.
- **Priority:** High
- **Acceptance Criteria:** **PASS** if an unauthorized modification attempt is denied and every successful transfer has an immutable audit-log entry containing source account, destination account, amount, and timestamp. **FAIL** if an unauthorized modification succeeds or any successful transfer lacks one required audit field.
- **Rationale:** Financially meaningful credit records require integrity, accountability, and traceability.
