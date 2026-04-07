/**
 * Lead service — stores property leads with cached image URLs and ATTOM lot dimensions.
 * Uses an in-memory Map. Swap this for a database (Postgres, Firestore, etc.) as needed.
 */

const leads = new Map();

/**
 * @typedef {Object} AttomData
 * @property {number} lot_size_sqft
 * @property {number} lot_width_ft
 * @property {number} lot_depth_ft
 */

/**
 * @typedef {Object} LeadImages
 * @property {string} street_view_url  - Google Street View static image URL
 * @property {string} satellite_url    - Google Maps satellite image URL
 */

/**
 * @typedef {Object} Lead
 * @property {string} lead_id
 * @property {string} address
 * @property {string} email
 * @property {AttomData} attom
 * @property {LeadImages} images
 * @property {string} status  - 'pending' | 'designing' | 'complete' | 'error'
 * @property {Array} designs  - populated by the design engine
 * @property {Date} created_at
 * @property {Date} updated_at
 */

export function createLead({ lead_id, address, email, attom, images }) {
  const lead = {
    lead_id,
    address,
    email,
    attom,
    images,
    status: 'pending',
    designs: [],
    created_at: new Date(),
    updated_at: new Date(),
  };
  leads.set(lead_id, lead);
  return lead;
}

export function getLead(lead_id) {
  return leads.get(lead_id) ?? null;
}

export function updateLead(lead_id, updates) {
  const lead = leads.get(lead_id);
  if (!lead) return null;
  const updated = { ...lead, ...updates, updated_at: new Date() };
  leads.set(lead_id, updated);
  return updated;
}

export function getAllLeads() {
  return Array.from(leads.values());
}
