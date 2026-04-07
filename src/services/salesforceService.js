/**
 * Salesforce Service
 *
 * Handles all reads/writes to Salesforce using jsforce.
 * Authenticates with a Connected App via username/password + security token.
 *
 * Salesforce setup required:
 *   - Custom fields on Lead object (see README)
 *   - Custom object: Backyard_Design__c (see README)
 *   - Connected App with OAuth enabled
 */

import jsforce from 'jsforce';

let connection = null;

async function getConnection() {
  if (connection) return connection;

  connection = new jsforce.Connection({
    loginUrl: process.env.SF_LOGIN_URL ?? 'https://login.salesforce.com',
  });

  await connection.login(
    process.env.SF_USERNAME,
    // Salesforce requires password + security token concatenated
    `${process.env.SF_PASSWORD}${process.env.SF_SECURITY_TOKEN}`,
  );

  return connection;
}

/**
 * Read a Salesforce Lead by ID.
 * Returns the lead with our custom fields populated.
 */
export async function getSalesforceLead(leadId) {
  const conn = await getConnection();
  return conn.sobject('Lead').retrieve(leadId);
}

/**
 * Update a Lead's design status and image/ATTOM custom fields.
 * Called when Make.com fires the webhook with the SF Lead ID.
 */
export async function updateLeadStatus(leadId, { status, streetViewUrl, satelliteUrl, lotSizeSqft, lotWidthFt, lotDepthFt }) {
  const conn = await getConnection();

  const fields = { Design_Status__c: status };
  if (streetViewUrl !== undefined) fields.Street_View_URL__c = streetViewUrl;
  if (satelliteUrl !== undefined) fields.Satellite_URL__c = satelliteUrl;
  if (lotSizeSqft !== undefined) fields.Lot_Size_Sqft__c = lotSizeSqft;
  if (lotWidthFt !== undefined) fields.Lot_Width_Ft__c = lotWidthFt;
  if (lotDepthFt !== undefined) fields.Lot_Depth_Ft__c = lotDepthFt;

  return conn.sobject('Lead').update({ Id: leadId, ...fields });
}

/**
 * Create Backyard_Design__c records for each generated design.
 * Uses bulk insert to create all 3 in one API call.
 */
export async function createDesignRecords(leadId, designs) {
  const conn = await getConnection();

  const records = designs.map((d) => ({
    Lead__c: leadId,
    Style_Id__c: d.style_id,
    Style_Name__c: d.style_name,
    Headline__c: d.headline,
    Description__c: d.description,
    Features__c: Array.isArray(d.features) ? d.features.join('\n') : d.features,
    Patio_Sqft__c: d.patio_sqft,
    Estimated_Cost_Low__c: d.estimated_cost_low,
    Estimated_Cost_High__c: d.estimated_cost_high,
    Timeline_Weeks__c: d.timeline_weeks,
    Plant_Recommendations__c: Array.isArray(d.plant_recommendations)
      ? d.plant_recommendations.join(', ')
      : d.plant_recommendations,
    Property_Notes__c: d.property_notes,
  }));

  const results = await conn.sobject('Backyard_Design__c').create(records);

  // jsforce returns array for bulk, single object for single record
  const resultArray = Array.isArray(results) ? results : [results];
  const failed = resultArray.filter((r) => !r.success);
  if (failed.length > 0) {
    throw new Error(`Failed to create ${failed.length} design record(s): ${JSON.stringify(failed)}`);
  }

  return resultArray;
}

/**
 * Query all Backyard_Design__c records for a given Lead.
 */
export async function getDesignRecords(leadId) {
  const conn = await getConnection();
  return conn.query(
    `SELECT Id, Style_Id__c, Style_Name__c, Headline__c, Description__c,
            Features__c, Patio_Sqft__c, Estimated_Cost_Low__c,
            Estimated_Cost_High__c, Timeline_Weeks__c,
            Plant_Recommendations__c, Property_Notes__c, CreatedDate
     FROM Backyard_Design__c
     WHERE Lead__c = '${leadId}'
     ORDER BY CreatedDate ASC`,
  );
}
