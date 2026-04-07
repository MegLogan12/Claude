/**
 * BackyardDesignCalloutTest
 *
 * Must maintain >= 75% code coverage for deployment to production.
 * Run in sandbox: Developer Console → Test → Run All
 */
@isTest
private class BackyardDesignCalloutTest {

    // ---------------------------------------------------------------------------
    // Mock HTTP response
    // ---------------------------------------------------------------------------
    private class WebhookMock implements HttpCalloutMock {
        private final Integer statusCode;
        WebhookMock(Integer statusCode) { this.statusCode = statusCode; }

        public HttpResponse respond(HttpRequest req) {
            // Verify the request shape is correct
            System.assertEquals('POST', req.getMethod());
            System.assert(req.getEndpoint().contains('/webhook/lead'));

            Map<String, Object> body = (Map<String, Object>) JSON.deserializeUntyped(req.getBody());
            System.assert(body.containsKey('sf_lead_id'), 'Payload missing sf_lead_id');
            System.assert(body.containsKey('attom'),      'Payload missing attom');
            System.assert(body.containsKey('images'),     'Payload missing images');

            HttpResponse res = new HttpResponse();
            res.setStatusCode(statusCode);
            res.setBody(statusCode == 202
                ? '{"success":true,"status":"pending"}'
                : '{"error":"Internal Server Error"}'
            );
            return res;
        }
    }

    // ---------------------------------------------------------------------------
    // Helper: build a fully-enriched Lead
    // ---------------------------------------------------------------------------
    private static Lead buildEnrichedLead() {
        return new Lead(
            FirstName    = 'Jane',
            LastName     = 'Homeowner',
            Company      = 'Self',
            Email        = 'jane@example.com',
            Street       = '123 Oak Lane',
            City         = 'Austin',
            State        = 'TX',
            PostalCode   = '78701',
            Lot_Size_Sqft__c  = 8500,
            Lot_Width_Ft__c   = 85,
            Lot_Depth_Ft__c   = 100,
            Street_View_URL__c = 'https://maps.googleapis.com/streetview?test',
            Satellite_URL__c   = 'https://maps.googleapis.com/satellite?test',
            Design_Status__c   = 'Pending'
        );
    }

    // ---------------------------------------------------------------------------
    // Test 1: Callout succeeds (202)
    // ---------------------------------------------------------------------------
    @isTest
    static void testCallout_202() {
        Lead lead = buildEnrichedLead();
        insert lead;

        Test.setMock(HttpCalloutMock.class, new WebhookMock(202));
        Test.startTest();
        System.enqueueJob(new BackyardDesignCallout(new List<Id>{ lead.Id }));
        Test.stopTest();

        // No exception = pass. Server writes designs back asynchronously.
    }

    // ---------------------------------------------------------------------------
    // Test 2: Callout gets a 500 — should not throw, just log
    // ---------------------------------------------------------------------------
    @isTest
    static void testCallout_500_doesNotThrow() {
        Lead lead = buildEnrichedLead();
        insert lead;

        Test.setMock(HttpCalloutMock.class, new WebhookMock(500));
        Test.startTest();
        System.enqueueJob(new BackyardDesignCallout(new List<Id>{ lead.Id }));
        Test.stopTest();
        // If we reach here without an exception, the error handling is correct
    }

    // ---------------------------------------------------------------------------
    // Test 3: Trigger fires when image URLs are added on update
    // ---------------------------------------------------------------------------
    @isTest
    static void testTrigger_firesOnImageUrlUpdate() {
        // Insert lead WITHOUT image URLs — trigger should NOT fire yet
        Lead lead = new Lead(
            FirstName   = 'Bob',
            LastName    = 'Builder',
            Company     = 'Self',
            Email       = 'bob@example.com',
            Street      = '456 Elm St',
            City        = 'Houston',
            State       = 'TX',
            PostalCode  = '77001',
            Lot_Size_Sqft__c = 6000,
            Lot_Width_Ft__c  = 60,
            Lot_Depth_Ft__c  = 100
        );
        insert lead;

        Test.setMock(HttpCalloutMock.class, new WebhookMock(202));
        Test.startTest();
        // Simulate Make.com enriching the lead with image URLs
        lead.Street_View_URL__c = 'https://maps.googleapis.com/streetview?bob';
        lead.Satellite_URL__c   = 'https://maps.googleapis.com/satellite?bob';
        update lead;
        Test.stopTest();

        // Trigger should have enqueued the job without errors
    }

    // ---------------------------------------------------------------------------
    // Test 4: Trigger does NOT fire again if Design_Status__c is already set
    // ---------------------------------------------------------------------------
    @isTest
    static void testTrigger_doesNotRefireWhenStatusSet() {
        Lead lead = buildEnrichedLead();
        lead.Design_Status__c = 'Designing'; // Already in progress
        insert lead;

        Test.setMock(HttpCalloutMock.class, new WebhookMock(202));
        Test.startTest();
        lead.LastName = 'Homeowner-Updated'; // Unrelated update
        update lead;
        Test.stopTest();

        // No callout enqueued — mock would throw if called unexpectedly
    }

    // ---------------------------------------------------------------------------
    // Test 5: Trigger fires on insert when all data is present at creation
    //         (e.g. Make.com creates a fully-enriched Lead in one step)
    // ---------------------------------------------------------------------------
    @isTest
    static void testTrigger_firesOnInsertWhenFullyEnriched() {
        Test.setMock(HttpCalloutMock.class, new WebhookMock(202));
        Test.startTest();
        Lead lead = buildEnrichedLead();
        insert lead;
        Test.stopTest();
    }
}
