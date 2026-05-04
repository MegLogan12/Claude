# Salesforce Component Backlog

> Documentation-only backlog. No deployment/activation included.

## 1. PO Pipeline
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PO Intake Panel | Lightning Record Component | WorkOrder | Intake and validate PO | PO number, lot, account | Create/update WO | Dynamic forms + validation flow | Account/Lot mapping | Create PO and validate required fields |

## 2. Account / Community / Lot
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Lot Context Card | Related list/config | Account/WorkOrder | Show community and lot context | Community, lot phase | Open linked records | Standard related lists | Data model verification | Open lot from WO |

## 3. Work Order Command Center
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| Command Timeline | LWC | WorkOrder | Single-pane state across WO/FSL | WO status, SA status | Launch create SA/assign | LWC + screen flow | FSL objects available | Timeline reflects live SA status |

## 4. Production Install Ticket
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| Install Ticket Form | Record page section | WorkOrder | Manage production install completion | Install checklist | Update status/checks | Dynamic forms + flow | WO fields verified | Submit with required checks |

## 5. Finished Job Ticket
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| Finished Job Stage | Record type layout | WorkOrder | Stage finished job review | Finished_Job record type | Update staged fields | Record type + layout | Record type added staged | Transition to Finished_Job |

## 6. Warranty Ticket
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| Warranty Intake | Flow action | Case | Capture warranty case | Coverage fields on Case/WO | Create/rout case | Screen flow | Coverage fields exist | Create warranty case from WO |

## 7. Customer Care Process
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| Escalation Action | Quick action + flow | Case | Route care issues | Reason, severity | Escalate queue | Quick action + flow | Queue setup | Escalation task/owner set |

## 8. Aqua
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| Aqua Checklist | LWC/Flow | WorkOrder | Capture Aqua-specific checks | Aqua checklist fields | Submit checks | LWC wrapper + flow | Core WO baseline | Aqua submission persists |

## 9. Loading Ticket
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| Loading Confirmation | Mobile/desktop flow | WorkOrder | Confirm load complete before route | Load lines, timestamps | Mark loaded | Screen flow | Inventory objects | Cannot route until loaded |

## 10. Inventory / Scanner
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| Consumption Logger | Standard create action | ProductConsumed | Use FSL-native consumption | ProductItem, qty, WO link | Create ProductConsumed | Standard action + validation flow | ProductItem/Pricebook readiness | ProductConsumed created correctly |

## 11. DQC Arrival Checklist
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| DQC Section | Mobile checklist section | ServiceAppointment | Supplier sod/mulch arrival verification | Arrival quality checks | Save checklist section | Mobile flow section | Arrival state control | DQC visible only on arrival step |

## 12. QI / Closeout
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| Closeout Gate | Flow | WorkOrder | Enforce closeout criteria | QI score, proof docs | Close WO | Autolaunched + screen flow | Proof categories available | Fails if proof missing |

## 13. Foreman Mobile
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| My Day Console | FSL mobile config | ServiceAppointment | Guide foreman day steps | SA sequence, statuses | Start/arrive/complete | FSL mobile cards + flows | FSL mobile permissions | Steps visible in order |

## 14. Dispatch
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| Exception Board | Console list views | ServiceAppointment | Monitor exceptions | SA status exceptions | Reassign/escalate | List views + actions | FSL assignment enabled | Reassign from exception board |

## 15. WEX / Weather / Traffic
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| Overlay Insights | LWC integration panel | WorkOrder | Inform decisions with external data | API feeds | Display advisory only | LWC + integration service | API/security review | Overlay renders advisory badges |

## 16. Revenue / Invoice
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| Invoice Handoff Action | Quick action/flow | WorkOrder | Route complete jobs to invoice queue | Completion date, account | Create handoff task | Quick action + flow | Closeout complete state | Task created in invoice queue |

## 17. Admin / Go-Live Readiness
| Component | Type | Object | Purpose | Data Needed | Action Needed | Build Method | Dependency | Test Case |
| Readiness Dashboard | Report/dashboard | WorkOrder/Case/SA | Track readiness controls | Coverage, inventory, mobile, perms | Review and sign off | Reports + checklist doc | All prior streams | Dashboard reflects all gates |
