/**
 * Designs API Route
 *
 * Used by the upgrademybackyard.com frontend to fetch the 3 design options
 * for a given lead once generation is complete.
 */

import { Router } from 'express';
import { getLead, getAllLeads } from '../services/leadService.js';

const router = Router();

/**
 * GET /designs/:leadId
 *
 * Returns the lead data and all generated designs.
 * Poll this endpoint until status === 'complete'.
 *
 * Response:
 * {
 *   "lead_id": "...",
 *   "address": "...",
 *   "status": "complete",  // 'pending' | 'designing' | 'complete' | 'error'
 *   "images": { "street_view_url": "...", "satellite_url": "..." },
 *   "attom": { "lot_size_sqft": 8500, "lot_width_ft": 85, "lot_depth_ft": 100 },
 *   "designs": [
 *     {
 *       "style_id": "modern",
 *       "style_name": "Modern Outdoor Living",
 *       "headline": "...",
 *       "description": "...",
 *       "features": ["16x20 ft stamped concrete patio", ...],
 *       "patio_sqft": 320,
 *       "estimated_cost_low": 18000,
 *       "estimated_cost_high": 28000,
 *       "timeline_weeks": 3,
 *       "plant_recommendations": ["Agave", "Mexican Sage", "Lantana"],
 *       "property_notes": "..."
 *     },
 *     { ... },
 *     { ... }
 *   ]
 * }
 */
router.get('/:leadId', (req, res) => {
  const lead = getLead(req.params.leadId);

  if (!lead) {
    return res.status(404).json({ error: 'Lead not found' });
  }

  const { lead_id, address, email, attom, images, status, designs, error, created_at, updated_at } = lead;

  res.json({
    lead_id,
    address,
    email,
    attom,
    images,
    status,
    designs,
    ...(error ? { error } : {}),
    created_at,
    updated_at,
  });
});

/**
 * GET /designs
 * Returns all leads (admin/debug view).
 */
router.get('/', (req, res) => {
  const leads = getAllLeads().map(({ lead_id, address, email, status, designs, created_at }) => ({
    lead_id,
    address,
    email,
    status,
    design_count: designs.length,
    created_at,
  }));
  res.json({ leads });
});

export default router;
