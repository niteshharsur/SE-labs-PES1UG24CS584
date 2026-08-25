# UC-03 - Transfer Solar Credits

| Field | Details |
|---|---|
| **Use Case ID** | UC-03 |
| **Use Case Name** | Transfer Solar Credits |
| **Primary Actor** | Prosumer Resident |

## Preconditions

1. The Prosumer Resident has access to the portal.
2. The source account has a recorded solar-credit balance.
3. The recipient is a valid neighbor account.

## Postconditions

1. The requested credits are deducted from the prosumer balance.
2. The transferred credits are applied to the recipient account/billing statement.
3. The successful transaction is recorded.
4. The transfer confirmation is displayed.

## Main Success Scenario

1. Prosumer Resident selects "Transfer Solar Credits".
2. System displays the available credit balance and transfer fields.
3. Prosumer enters the recipient account and transfer amount.
4. System validates the recipient and transfer amount.
5. System validates that the prosumer has sufficient available credits.
6. System deducts the transferred credits from the prosumer balance.
7. System applies the transferred credits to the recipient account/billing statement.
8. System records the transaction with source, destination, amount, and timestamp.
9. System displays a transfer confirmation.
10. Use case ends successfully.

## Alternate Flow

### AF-01 - Insufficient Credit Balance

**At Step 5:**

1. System determines that the requested amount exceeds the available credit balance.
2. System rejects the transfer.
3. System displays "Insufficient credit balance".
4. No credits are deducted.
5. No credits are applied to the recipient.
6. The transaction is not recorded as a successful transfer.
