# LOVING UI Implementation Plan

## 1) Executive summary
This plan converts the LOVING HTML UI contract into a Salesforce build-control program without deploying metadata. It preserves FSL scheduling ownership and maps pre/post ServiceAppointment operations into staged Salesforce components.

## 2) Locked architecture
PO → Takeoff → WorkOrder/WOLI → ServiceAppointment → AssignedResource/ServiceCrew → Foreman Mobile via FSL → DQC arrival checklist (not loading) → QI/Closeout → Invoice handoff.

## 3) Build sequence
1. PO Pipeline  
2. Takeoff/BMG Gate  
3. WorkOrder Command Center  
4. Production Install Ticket  
5. Finished Job record type and ticket (staged)  
6. Customer Care / Warranty coverage fields  
7. Loading Ticket  
8. Inventory movement using ProductConsumed/ProductItem  
9. Foreman Mobile  
10. DQC Arrival Checklist  
11. QI / Closeout  
12. Invoice Handoff  
13. Aqua  
14. Dispatch  
15. WEX / Weather / Traffic overlays  
16. Admin / Go-Live Readiness

## 4) Object dependencies
- Core: WorkOrder, WorkOrderLineItem, ServiceAppointment, AssignedResource, ServiceCrew, Case, Account.
- Inventory baseline: ProductConsumed, ProductItem.
- Staged additions only after audit evidence.

## 5) Flow dependencies
- Takeoff submit flow.
- Appointment creation and assignment support flows (FSL-compatible).
- Arrival/DQC checklist flows.
- Cannot-complete escalation flow.
- QI/Closeout and invoice handoff flows.

## 6) LWC dependencies
- WorkOrder Command Center timeline/orchestration component.
- Optional WEX/weather/traffic advisory panel.
- Optional Aqua checklist wrapper where standard UI is insufficient.

## 7) FSL Mobile dependencies
- Foreman My Day card set.
- Mobile quick actions for In Route/Arrival/Closeout.
- DQC subsection in Arrival checklist only.

## 8) Permission dependencies
- Role-based permission sets for PO, Estimator, Dispatch, Foreman, QI, Warranty, Revenue, Admin.
- Field-level and action-level access required before UAT.

## 9) Testing plan
- Execute every test case in `audit/ui/HTML_UI_Action_Map_Normalized.csv`.
- Validate disabled states and prerequisite enforcement.
- Confirm no fake GPS/ETA/inventory/weather behavior.
- Run staging-only integration checks for FSL scheduling touchpoints.

## 10) Rollback plan
- Keep all changes in documentation and isolated scaffolding until approvals.
- For staged metadata in future: deactivate via change set rollback sequence in sandbox only.
- Preserve previous page assignments and quick actions snapshots before activation.

## 11) Stop conditions
- Missing required source artifacts.
- Unverified object/field prerequisites.
- Any proposed change violating locked architecture or non-negotiables.
- Any dependency requiring prohibited object creation without approval.

## 12) Morning checkpoint format
- Yesterday completed:
- Today planned:
- Current blockers:
- Salesforce verification needed:
- Risks introduced:
- Next decision request:

## 13) Source artifact dependency (blocking)
This scaffold is **not** final implementation guidance until the following source artifacts are present and mapped line-by-line:
- `LOVING_Everything_HTML_UI_v1.zip`
- `12_html_v1_sf_map.csv`
- `13_html_v1_action_map.csv`
- `14_v1_object_readiness.md`

Next required PR must:
1. Add or reference the source artifacts in-repo.
2. Replace `SOURCE_PACKAGE_MISSING` and placeholder mappings with real HTML-derived entries.
3. Replace `Needs Salesforce verification` where metadata evidence is obtained.
4. Keep changes docs-only unless explicitly approved for staged metadata scaffolding.

Do not proceed to deployable UI build from this scaffold alone.
