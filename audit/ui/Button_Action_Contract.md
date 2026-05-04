# Button / Action Contract

All UI buttons/actions must map to a real Salesforce action. No placeholders.

## Allowed action outcomes
1. Open a real record.
2. Launch a real Flow.
3. Create a real record.
4. Update a real record.
5. Upload/categorize proof.
6. Move inventory via ProductConsumed/ProductItem.
7. Assign/schedule work via FSL.
8. Route/escalate an issue.
9. Show clear disabled state when prerequisites are unmet.

## Contract rules
- No fake buttons.
- No fake GPS, ETA, inventory, or weather automation.
- FSL remains scheduling owner for ServiceAppointment/AssignedResource/ServiceCrew.
- DQC is arrival checklist only, not loading, not standalone ticket.
- Coverage decision uses Case/WorkOrder fields; do not create `Coverage_Decision__c`.
- Inventory movement starts with `ProductConsumed` + `ProductItem`; do not create `Inventory_Movement__c`.
- `Inventory_Ticket__c` only after `Inventory_Count__c` audit and approval.

## Disabled-state minimum standard
Every button must include:
- Prerequisite check.
- Disabled reason text.
- Audit field updates when action succeeds.
