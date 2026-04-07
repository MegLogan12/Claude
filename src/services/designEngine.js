/**
 * AI Design Engine
 *
 * Uses Claude's vision API to analyze the homeowner's actual house photo
 * (from Google Street View) and the aerial satellite view, combined with
 * ATTOM lot dimensions, to generate 3 realistic patio/landscape design options.
 */

import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const DESIGN_STYLES = [
  {
    id: 'modern',
    name: 'Modern Outdoor Living',
    description: 'Clean lines, concrete pavers, minimalist planters, string lights, and a pergola with shade sails.',
  },
  {
    id: 'natural',
    name: 'Natural Garden Retreat',
    description: 'Flagstone path, raised garden beds, native plants, a fire pit circle, and a cedar pergola.',
  },
  {
    id: 'family',
    name: 'Family Entertainment Hub',
    description: 'Large paver patio, built-in grill station, kids lawn area, shade structure, and bistro seating.',
  },
];

/**
 * Build the Claude prompt that analyzes the house images and generates
 * 3 design overlays scaled to the actual ATTOM lot dimensions.
 */
function buildSystemPrompt(attom) {
  const { lot_size_sqft, lot_width_ft, lot_depth_ft } = attom;
  return `You are an expert landscape architect and outdoor living designer for UpgradeMyBackyard.com.

You analyze real homeowner property photos and lot data to create personalized backyard design plans.

Property lot dimensions from ATTOM Data:
- Lot size: ${lot_size_sqft.toLocaleString()} sq ft
- Lot width: ${lot_width_ft} ft
- Lot depth: ${lot_depth_ft} ft

When generating designs:
1. Reference specific features visible in the photos (existing trees, fence lines, grade, driveway, etc.)
2. Scale all patio/feature dimensions to fit within the actual lot measurements
3. Recommend realistic project costs based on the space size
4. Be specific about materials, dimensions, and placement relative to the house
5. Output valid JSON only — no markdown, no prose outside the JSON structure`;
}

function buildUserPrompt(address, style) {
  return `Analyze the attached house photos for the property at: ${address}

Generate a detailed "${style.name}" backyard design.

Return a single JSON object with this exact structure:
{
  "style_id": "${style.id}",
  "style_name": "${style.name}",
  "headline": "One compelling sentence describing the design for this specific home",
  "description": "2-3 sentences describing the design using specific features visible in the photos",
  "features": [
    "Feature 1 with dimension (e.g., '16x20 ft stamped concrete patio')",
    "Feature 2 with dimension",
    "Feature 3 with dimension",
    "Feature 4 with dimension",
    "Feature 5 with dimension"
  ],
  "patio_sqft": <number — estimated patio square footage based on lot size>,
  "estimated_cost_low": <number — low end project cost in USD>,
  "estimated_cost_high": <number — high end project cost in USD>,
  "timeline_weeks": <number — estimated installation timeline>,
  "plant_recommendations": ["plant 1", "plant 2", "plant 3"],
  "property_notes": "Specific observations about this property from the photos that informed the design"
}`;
}

/**
 * Fetch a URL and return it as a base64-encoded string with media type.
 * This is needed because Claude's URL image support works best with
 * direct image URLs; we fetch and encode for reliability.
 */
async function fetchImageAsBase64(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch image from ${url}: ${response.status} ${response.statusText}`);
  }
  const contentType = response.headers.get('content-type') || 'image/jpeg';
  const mediaType = contentType.split(';')[0].trim();
  const buffer = await response.arrayBuffer();
  const base64 = Buffer.from(buffer).toString('base64');
  return { base64, mediaType };
}

/**
 * Generate one design option using Claude vision.
 */
async function generateDesign(address, attom, images, style) {
  const [streetView, satellite] = await Promise.all([
    fetchImageAsBase64(images.street_view_url),
    fetchImageAsBase64(images.satellite_url),
  ]);

  const stream = await client.messages.stream({
    model: 'claude-opus-4-6',
    max_tokens: 2048,
    thinking: { type: 'adaptive' },
    system: buildSystemPrompt(attom),
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'image',
            source: {
              type: 'base64',
              media_type: streetView.mediaType,
              data: streetView.base64,
            },
          },
          {
            type: 'image',
            source: {
              type: 'base64',
              media_type: satellite.mediaType,
              data: satellite.base64,
            },
          },
          {
            type: 'text',
            text: buildUserPrompt(address, style),
          },
        ],
      },
    ],
  });

  const message = await stream.finalMessage();

  const textBlock = message.content.find((b) => b.type === 'text');
  if (!textBlock) throw new Error('Claude returned no text content');

  try {
    return JSON.parse(textBlock.text);
  } catch {
    throw new Error(`Claude returned invalid JSON for style "${style.name}": ${textBlock.text.slice(0, 200)}`);
  }
}

/**
 * Generate all 3 design options in parallel.
 * @param {import('./leadService.js').Lead} lead
 * @returns {Promise<Array>} array of 3 design objects
 */
export async function generateDesigns(lead) {
  const { address, attom, images } = lead;

  const results = await Promise.allSettled(
    DESIGN_STYLES.map((style) => generateDesign(address, attom, images, style))
  );

  const designs = [];
  const errors = [];

  for (const [i, result] of results.entries()) {
    if (result.status === 'fulfilled') {
      designs.push(result.value);
    } else {
      errors.push(`${DESIGN_STYLES[i].name}: ${result.reason.message}`);
    }
  }

  if (designs.length === 0) {
    throw new Error(`All designs failed: ${errors.join('; ')}`);
  }

  return designs;
}
