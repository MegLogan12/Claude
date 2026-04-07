import 'dotenv/config';
import express from 'express';
import webhookRouter from './routes/webhook.js';
import designsRouter from './routes/designs.js';

const app = express();
const PORT = process.env.PORT ?? 3000;

app.use(express.json());

// Health check
app.get('/health', (_, res) => res.json({ status: 'ok' }));

// Step 2-3: Make.com posts lead + image URLs + ATTOM data here
app.use('/webhook', webhookRouter);

// Step 5: Frontend polls this to show homeowner their 3 designs
app.use('/designs', designsRouter);

app.listen(PORT, () => {
  console.log(`UpgradeMyBackyard design server running on port ${PORT}`);
  console.log(`  POST /webhook/lead  — Make.com webhook receiver`);
  console.log(`  GET  /designs/:id   — Fetch designs for a lead`);
});
