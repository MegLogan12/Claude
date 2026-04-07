/**
 * BackyardDesignCallout
 *
 * Queueable Apex that POSTs a Salesforce Lead (with ATTOM lot dimensions
 * and Google image URLs) to the UpgradeMyBackyard design server.
 * The server generates 3 AI designs and writes them back as
 * Backyard_Design__c records.
 *
 * Prerequisites:
 *   1. Named Credential named "UpgradeMyBackyard" pointing to your server URL
 *      Setup → Security → Named Credentials → New
 *      Label: UpgradeMyBackyard
 *      Name:  UpgradeMyBackyard
 *      URL:   https://your-server.com   (no trailing slash)
 *      Auth:  Named Principal, Authentication Protocol: No Authentication
 *      (set the Bearer token via a custom header or use Password auth type)
 *
 *   2. Remote Site Setting (if not using Named Credentials)
 *      Setup → Security → Remote Site Settings → New
 *      Name: UpgradeMyBackyard
 *      URL:  https://your-server.com
 */
public class BackyardDesignCallout implements Queueable, Database.AllowsCallouts {

    private List<Id> leadIds;

    public BackyardDesignCallout(List<Id> leadIds) {
        this.leadIds = leadIds;
    }

    public void execute(QueueableContext ctx) {
        List<Lead> leads = [
            SELECT Id, FirstName, LastName, Street, City, State, PostalCode,
                   Email,
                   Lot_Size_Sqft__c, Lot_Width_Ft__c, Lot_Depth_Ft__c,
                   Street_View_URL__c, Satellite_URL__c,
                   Design_Status__c
            FROM Lead
            WHERE Id IN :leadIds
        ];

        for (Lead lead : leads) {
            callWebhook(lead);
        }
    }

    private void callWebhook(Lead lead) {
        // Build the JSON payload the design server expects
        Map<String, Object> attom = new Map<String, Object>{
            'lot_size_sqft' => lead.Lot_Size_Sqft__c,
            'lot_width_ft'  => lead.Lot_Width_Ft__c,
            'lot_depth_ft'  => lead.Lot_Depth_Ft__c
        };

        Map<String, Object> images = new Map<String, Object>{
            'street_view_url' => lead.Street_View_URL__c,
            'satellite_url'   => lead.Satellite_URL__c
        };

        Map<String, Object> payload = new Map<String, Object>{
            'sf_lead_id' => lead.Id,
            'address'    => buildAddress(lead),
            'email'      => lead.Email,
            'attom'      => attom,
            'images'     => images
        };

        HttpRequest req = new HttpRequest();
        // Uses Named Credential — swap for full URL + Remote Site if preferred:
        // req.setEndpoint('https://your-server.com/webhook/lead');
        req.setEndpoint('callout:UpgradeMyBackyard/webhook/lead');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        req.setHeader('Authorization', 'Bearer ' + getWebhookSecret());
        req.setBody(JSON.serialize(payload));
        req.setTimeout(30000); // 30 s — server responds 202 immediately

        HttpResponse res = new Http().send(req);

        if (res.getStatusCode() != 202) {
            // Log and fail gracefully — designs will show as Error in the Lead
            System.debug(LoggingLevel.ERROR,
                'BackyardDesignCallout: webhook failed for Lead ' + lead.Id +
                ' — HTTP ' + res.getStatusCode() + ' ' + res.getBody()
            );
        }
    }

    private String buildAddress(Lead lead) {
        List<String> parts = new List<String>();
        if (String.isNotBlank(lead.Street))     parts.add(lead.Street);
        if (String.isNotBlank(lead.City))       parts.add(lead.City);
        if (String.isNotBlank(lead.State))      parts.add(lead.State);
        if (String.isNotBlank(lead.PostalCode)) parts.add(lead.PostalCode);
        return String.join(parts, ', ');
    }

    /**
     * Store WEBHOOK_SECRET in a Custom Setting or Custom Metadata Type
     * rather than hardcoding it here.
     * Example using a Protected Custom Setting named "BackyardSettings__c"
     * with a Text field "Webhook_Secret__c":
     */
    private String getWebhookSecret() {
        // BackyardSettings__c settings = BackyardSettings__c.getOrgDefaults();
        // return settings.Webhook_Secret__c;
        return ''; // Replace with your secret retrieval
    }
}
