/**
 * Make.com Webhook Route
 *
 * Make.com calls POST /webhook/lead after it has:
 *   1. Received the address from upgrademybackyard.com
 *   2. Queried ATTOM Data for lot dimensions
 *   3. Fetched Google Street View and Satellite image URLs
 *
 * This endpoint caches the lead data and kicks off AI design generation.
 */

import { Router } from 'express';
import { createLead, updateLead } from '../services/leadService.js';
import { generateDesigns } from '../services/designEngine.js';

const router = Router();

/**
 * Validate the Make.com webhook secret sent in the Authorization header.
 */
function validateWebhookSecret(req) {
  const secret = process.env.WEBHOOK_SECRET;
  if (!secret) return true; // Skip auth if not configured (dev mode)
  const authHeader = req.headers['authorization'] ?? '';
  return authHeader === `Bearer ${secret}`;
}

/**
 * POST /webhook/lead
 *
 * Expected body from Make.com:
 * {
 *   "lead_id": "uuid",
 *   "address": "123 Main St, Austin, TX 78701",
 *   "email": "homeowner@example.com",
 *   "attom": {
 *     "lot_size_sqft": 8500,
 *     "lot_width_ft": 85,
 *     "lot_depth_ft": 100
 *   },
 *   "images": {
 *     "street_view_url": "https://maps.googleapis.com/maps/api/streetview?...",
 *     "satellite_url": "https://maps.googleapis.com/maps/api/staticmap?..."
 *   }
 * }
 */
router.post('/lead', async (req, res) => {
  if (!validateWebhookSecret(req)) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const { lead_id, address, email, attom, images } = req.body;

  // Validate required fields
  const missing = [];
  if (!lead_id) missing.push('lead_id');
  if (!address) missing.push('address');
  if (!attom?.lot_size_sqft) missing.push('attom.lot_size_sqft');
  if (!attom?.lot_width_ft) missing.push('attom.lot_width_ft');
  if (!attom?.lot_depth_ft) missing.push('attom.lot_depth_ft');
  if (!images?.street_view_url) missing.push('images.street_view_url');
  if (!images?.satellite_url) missing.push('images.satellite_url');

  if (missing.length > 0) {
    return res.status(400).json({ error: `Missing required fields: ${missing.join(', ')}` });
  }

  // Cache the lead immediately — store photo URLs + ATTOM dimensions
  const lead = createLead({ lead_id, address, email: email ?? '', attom, images });

  // Acknowledge Make.com right away so it doesn't time out
  res.status(202).json({
    success: true,
    lead_id,
    status: 'pending',
    message: 'Lead received. Design generation started.',
  });

  // Generate designs asynchronously (don't block the webhook response)
  setImmediate(async () => {
    try {
      updateLead(lead_id, { status: 'designing' });
      console.log(`[${lead_id}] Generating designs for: ${address}`);

      const designs = await generateDesigns(lead);

      updateLead(lead_id, { status: 'complete', designs });
      console.log(`[${lead_id}] Design generation complete. ${designs.length} designs created.`);
    } catch (err) {
      updateLead(lead_id, { status: 'error', error: err.message });
      console.error(`[${lead_id}] Design generation failed:`, err.message);
    }
  });
});

export default router;
