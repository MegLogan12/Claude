/**
 * LeadBackyardDesignTrigger
 *
 * Fires after a Lead is inserted or updated.
 * Enqueues BackyardDesignCallout when:
 *   - The Lead has ATTOM lot dimensions (populated by Make.com)
 *   - The Street View AND Satellite image URLs just became non-blank
 *   - Design_Status__c is null or 'Pending' (hasn't been sent yet)
 *
 * Make.com flow:
 *   1. Homeowner submits address on upgrademybackyard.com
 *   2. Make.com creates the Salesforce Lead
 *   3. Make.com calls ATTOM API → updates Lot_Size/Width/Depth fields
 *   4. Make.com builds Google image URLs → updates Street_View_URL__c, Satellite_URL__c
 *   5. This trigger fires on that update → enqueues the callout
 *   6. Server generates designs → writes Backyard_Design__c records back
 */
trigger LeadBackyardDesignTrigger on Lead (after insert, after update) {

    List<Id> leadIds = new List<Id>();

    for (Lead lead : Trigger.new) {
        Lead old = (Trigger.isUpdate) ? Trigger.oldMap.get(lead.Id) : null;

        // Must have all lot dimensions from ATTOM
        Boolean hasAttom = lead.Lot_Size_Sqft__c != null
                        && lead.Lot_Width_Ft__c  != null
                        && lead.Lot_Depth_Ft__c  != null;

        // Must have both image URLs
        Boolean hasImages = String.isNotBlank(lead.Street_View_URL__c)
                         && String.isNotBlank(lead.Satellite_URL__c);

        // Only fire once — skip if already sent to the design server
        Boolean notStarted = lead.Design_Status__c == null
                          || lead.Design_Status__c == 'Pending';

        // On insert: fire if all data is already present
        // On update: fire only when Street_View_URL__c transitions from blank → populated
        //            (prevents re-firing if the Lead is updated for other reasons)
        Boolean shouldFire;
        if (Trigger.isInsert) {
            shouldFire = hasAttom && hasImages && notStarted;
        } else {
            Boolean imagesJustAdded = String.isBlank(old.Street_View_URL__c)
                                   && String.isNotBlank(lead.Street_View_URL__c);
            shouldFire = hasAttom && hasImages && notStarted && imagesJustAdded;
        }

        if (shouldFire) {
            leadIds.add(lead.Id);
        }
    }

    if (!leadIds.isEmpty()) {
        System.enqueueJob(new BackyardDesignCallout(leadIds));
    }
}
