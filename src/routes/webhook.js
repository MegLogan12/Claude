/**
 * Make.com Webhook Route
 *
 * Make.com scenario flow:
 *   1. Homeowner submits address on upgrademybackyard.com
 *   2. Make.com creates a Salesforce Lead (or finds existing one)
 *   3. Make.com calls ATTOM API → updates Lead custom fields
 *   4. Make.com builds Google Street View + Satellite URLs → updates Lead
 *   5. Make.com POSTs to this endpoint with the Salesforce Lead ID + all data
 *
 * This endpoint kicks off Claude design generation, then writes the
 * 3 Backyard_Design__c records back to Salesforce when done.
 */

import { Router } from 'express';
import { createLead, updateLead } from '../services/leadService.js';
import { generateDesigns } from '../services/designEngine.js';
import {
  updateLeadStatus,
  createDesignRecords,
} from '../services/salesforceService.js';

const router = Router();

function validateWebhookSecret(req) {
  const secret = process.env.WEBHOOK_SECRET;
  if (!secret) return true;
  const authHeader = req.headers['authorization'] ?? '';
  return authHeader === `Bearer ${secret}`;
}

/**
 * POST /webhook/lead
 *
 * Make.com sends the Salesforce Lead ID plus all enriched data.
 * Body shape:
 * {
 *   "sf_lead_id": "00Q...",         ← Salesforce Lead record ID
 *   "address": "123 Main St, ...",
 *   "email": "homeowner@example.com",
 *   "attom": {
 *     "lot_size_sqft": 8500,
 *     "lot_width_ft": 85,
 *     "lot_depth_ft": 100
 *   },
 *   "images": {
 *     "street_view_url": "https://maps.googleapis.com/...",
 *     "satellite_url": "https://maps.googleapis.com/..."
 *   }
 * }
 */
router.post('/lead', async (req, res) => {
  if (!validateWebhookSecret(req)) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const { sf_lead_id, address, email, attom, images } = req.body;

  const missing = [];
  if (!sf_lead_id) missing.push('sf_lead_id');
  if (!address) missing.push('address');
  if (!attom?.lot_size_sqft) missing.push('attom.lot_size_sqft');
  if (!attom?.lot_width_ft) missing.push('attom.lot_width_ft');
  if (!attom?.lot_depth_ft) missing.push('attom.lot_depth_ft');
  if (!images?.street_view_url) missing.push('images.street_view_url');
  if (!images?.satellite_url) missing.push('images.satellite_url');

  if (missing.length > 0) {
    return res.status(400).json({ error: `Missing required fields: ${missing.join(', ')}` });
  }

  // Cache locally for fast polling; use Salesforce Lead ID as the key
  const lead = createLead({
    lead_id: sf_lead_id,
    address,
    email: email ?? '',
    attom,
    images,
  });

  res.status(202).json({
    success: true,
    sf_lead_id,
    status: 'pending',
    message: 'Lead received. Design generation started.',
  });

  setImmediate(async () => {
    try {
      updateLead(sf_lead_id, { status: 'designing' });

      // Reflect status in Salesforce immediately
      await updateLeadStatus(sf_lead_id, {
        status: 'Designing',
        streetViewUrl: images.street_view_url,
        satelliteUrl: images.satellite_url,
        lotSizeSqft: attom.lot_size_sqft,
        lotWidthFt: attom.lot_width_ft,
        lotDepthFt: attom.lot_depth_ft,
      });

      console.log(`[${sf_lead_id}] Generating designs for: ${address}`);
      const designs = await generateDesigns(lead);

      // Write all 3 designs to Salesforce as Backyard_Design__c records
      await createDesignRecords(sf_lead_id, designs);

      // Mark the Lead complete in Salesforce
      await updateLeadStatus(sf_lead_id, { status: 'Complete' });

      updateLead(sf_lead_id, { status: 'complete', designs });
      console.log(`[${sf_lead_id}] ${designs.length} designs written to Salesforce.`);
    } catch (err) {
      await updateLeadStatus(sf_lead_id, { status: 'Error' }).catch(() => {});
      updateLead(sf_lead_id, { status: 'error', error: err.message });
      console.error(`[${sf_lead_id}] Failed:`, err.message);
    }
  });
});

export default router;
