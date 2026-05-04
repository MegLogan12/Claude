# Object / Field Gap Register

| Area | Object / Field | Exists? | Needed For | Current Gap | Recommendation | Create Now? | Approval Needed? |
| ---- | -------------- | ------- | ---------- | ----------- | -------------- | ----------- | ---------------- |
| Coverage Decision | Case coverage fields | Needs Salesforce verification | Warranty routing | Field inventory unavailable in repo | Verify existing Case fields before any create | No | Yes |
| Coverage Decision | WorkOrder coverage fields | Needs Salesforce verification | Install/warranty decisioning | Field inventory unavailable in repo | Reuse WO fields; do not create Coverage_Decision__c | No | Yes |
| Inventory Movement | ProductConsumed | Needs Salesforce verification | Consumption logging | Metadata not visible in repo | Confirm FSL package/object availability | No | Yes |
| Inventory Movement | ProductItem | Needs Salesforce verification | On-hand/loaded inventory references | Metadata not visible in repo | Confirm ProductItem permissions/layouts | No | Yes |
| Inventory Ticket | Inventory_Count__c | Needs Salesforce verification | Decision whether Inventory_Ticket__c needed | Object/field not found in repo | Audit org metadata before recommending ticket object | No | Yes |
| Finished Job | WorkOrder.RecordType = Finished_Job | Needs Salesforce verification | Finished job staged flow | Record type not present in repo snapshot | Add staged record type only after metadata audit | Staged only | Yes |
| DQC | ServiceAppointment DQC fields | Needs Salesforce verification | Arrival checklist section | DQC fields not visible in repo | Add checklist fields on SA/WO as needed, not new ticket object | No | Yes |
| Invoice Handoff | WorkOrder invoice handoff fields | Needs Salesforce verification | Revenue handoff | Handoff fields unknown | Verify existing fields before create | No | Yes |
