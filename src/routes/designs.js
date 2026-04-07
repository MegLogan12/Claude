/**
 * Designs API Route
 *
 * GET /designs/:sfLeadId  — returns lead status + 3 generated designs.
 * Checks local cache first; falls back to Salesforce query.
 * Poll until status === 'complete'.
 */

import { Router } from 'express';
import { getLead, getAllLeads } from '../services/leadService.js';
import { getSalesforceLead, getDesignRecords } from '../services/salesforceService.js';

const router = Router();

/**
 * Normalize a Salesforce Backyard_Design__c record to the same shape
 * that the design engine returns.
 */
function normalizeDesignRecord(record) {
  return {
    style_id: record.Style_Id__c,
    style_name: record.Style_Name__c,
    headline: record.Headline__c,
    description: record.Description__c,
    features: record.Features__c ? record.Features__c.split('\n') : [],
    patio_sqft: record.Patio_Sqft__c,
    estimated_cost_low: record.Estimated_Cost_Low__c,
    estimated_cost_high: record.Estimated_Cost_High__c,
    timeline_weeks: record.Timeline_Weeks__c,
    plant_recommendations: record.Plant_Recommendations__c
      ? record.Plant_Recommendations__c.split(', ')
      : [],
    property_notes: record.Property_Notes__c,
  };
}

/**
 * GET /designs/:sfLeadId
 *
 * Returns:
 * {
 *   "sf_lead_id": "00Q...",
 *   "address": "...",
 *   "status": "Complete",
 *   "images": { "street_view_url": "...", "satellite_url": "..." },
 *   "attom": { ... },
 *   "designs": [ { style_id, style_name, headline, features, costs, ... }, ... ]
 * }
 */
router.get('/:sfLeadId', async (req, res) => {
  const { sfLeadId } = req.params;

  // Fast path: return from local cache if available
  const cached = getLead(sfLeadId);
  if (cached && cached.status === 'complete') {
    const { lead_id, address, email, attom, images, status, designs, created_at, updated_at } = cached;
    return res.json({ sf_lead_id: lead_id, address, email, attom, images, status, designs, created_at, updated_at });
  }

  if (cached && cached.status !== 'complete') {
    const { lead_id, address, email, attom, images, status, designs, error, created_at, updated_at } = cached;
    return res.json({
      sf_lead_id: lead_id, address, email, attom, images, status, designs,
      ...(error ? { error } : {}),
      created_at, updated_at,
    });
  }

  // Fallback: read directly from Salesforce (e.g., after a server restart)
  try {
    const [sfLead, designsResult] = await Promise.all([
      getSalesforceLead(sfLeadId),
      getDesignRecords(sfLeadId),
    ]);

    const designs = (designsResult.records ?? []).map(normalizeDesignRecord);

    res.json({
      sf_lead_id: sfLeadId,
      address: sfLead.Street ? `${sfLead.Street}, ${sfLead.City}, ${sfLead.State} ${sfLead.PostalCode}` : null,
      email: sfLead.Email,
      attom: {
        lot_size_sqft: sfLead.Lot_Size_Sqft__c,
        lot_width_ft: sfLead.Lot_Width_Ft__c,
        lot_depth_ft: sfLead.Lot_Depth_Ft__c,
      },
      images: {
        street_view_url: sfLead.Street_View_URL__c,
        satellite_url: sfLead.Satellite_URL__c,
      },
      status: (sfLead.Design_Status__c ?? 'Pending').toLowerCase(),
      designs,
    });
  } catch (err) {
    res.status(404).json({ error: `Lead not found: ${err.message}` });
  }
});

/**
 * GET /designs
 * Returns all leads from local cache (admin/debug).
 */
router.get('/', (req, res) => {
  const leads = getAllLeads().map(({ lead_id, address, email, status, designs, created_at }) => ({
    sf_lead_id: lead_id,
    address,
    email,
    status,
    design_count: designs.length,
    created_at,
  }));
  res.json({ leads });
});

export default router;
