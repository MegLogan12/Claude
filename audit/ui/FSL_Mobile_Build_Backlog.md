# FSL Mobile Build Backlog

DQC rule enforced:
- DQC is an arrival checklist section for supplier-delivered sod/mulch.
- DQC is not truck loading.
- DQC is not a standalone ticket.

| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Foreman My Day | Mobile home card | ServiceAppointment | Day sequence and priorities | SA list by assignee/date | Open next appointment | FSL mobile configuration | AssignedResource integrity | My Day order matches dispatch |
| Pre-shift vehicle checklist | Mobile flow | ServiceAppointment | Safety/compliance before departure | Checklist answers, odometer | Submit checklist | Screen flow (mobile) | Foreman permissions | Cannot start route before submit |
| Loaded checklist | Mobile flow | WorkOrder | Confirm materials loaded | Product list and quantities | Mark loaded | Screen flow | ProductItem availability | In Route blocked until loaded |
| In Route | Quick action | ServiceAppointment | Transition to route state | Timestamp, crew | Update SA status | Standard/FSL action | Pre-shift + loaded complete | Status updates to In Route |
| Arrival checklist | Mobile flow | ServiceAppointment | On-site arrival checks | Arrival time, site safety | Submit arrival | Screen flow | In Route status | Arrival checklist required for On Site |
| DQC on-site delivery check | Arrival subsection | ServiceAppointment | Supplier sod/mulch quality check | DQC yes/no + notes/photos | Save DQC section | Embedded flow section | Supplier-delivery flag | DQC section hidden when not applicable |
| Before photos | File action | ServiceAppointment | Capture pre-work proof | Image files + category | Upload and tag photos | Standard file upload + flow tagging | Camera/file access | Photos linked and categorized |
| Active job | Mobile card | WorkOrder/ServiceAppointment | Track job execution | Progress, blockers | Update progress | FSL card + flow | Arrival complete | Active job state visible |
| 2 PM Health Check | Timed flow action | WorkOrder | Mid-day operational signal | Health status, comments | Submit health check | Screen flow + schedule logic | Device local time handling | One health check per day enforced |
| Cannot-complete flag | Escalation flow | ServiceAppointment | Escalate blocked jobs | Blocker type, notes | Flag and create escalation case | Screen flow | Case routing config | Case created and SA flagged |
| FM review handoff | Handoff action | WorkOrder | Hand off for FM review | Review notes/proof links | Submit for review | Quick action + flow | Closeout prerequisites | FM queue receives item |
| Closeout | Mobile/desktop flow | WorkOrder | Complete QI and closeout | Final checklist + proof | Close work packet | Screen flow | QI completion | Closeout cannot submit with missing proof |
| End of day | Mobile flow | AssignedResource | End shift reconciliation | End mileage, unresolved items | Submit end-day report | Screen flow | Health check completed | End-of-day report saved |
