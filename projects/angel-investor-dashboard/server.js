import express from 'express';
import bodyParser from 'body-parser';
import Database from './db.js';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
const db = new Database();

app.use(bodyParser.json());
app.use(express.static('public'));

// Initialize database
await db.init();

// ==================== API Routes ====================

// Get all deals
app.get('/api/deals', async (req, res) => {
  try {
    const deals = await db.getAllDeals();
    
    // Enrich with follow-ons and exits
    const enrichedDeals = await Promise.all(deals.map(async deal => {
      const followOns = await db.getFollowOns(deal.id);
      const exits = await db.getExits(deal.id);
      return { ...deal, followOns, exits };
    }));
    
    res.json(enrichedDeals);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get single deal
app.get('/api/deals/:id', async (req, res) => {
  try {
    const deal = await db.getDeal(req.params.id);
    if (!deal) return res.status(404).json({ error: 'Deal not found' });
    
    const followOns = await db.getFollowOns(deal.id);
    const exits = await db.getExits(deal.id);
    
    res.json({ ...deal, followOns, exits });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Add new deal
app.post('/api/deals', async (req, res) => {
  try {
    const { name, stage, valuation, invested_amount, ownership_percent, date_invested, notes } = req.body;
    
    if (!name || !invested_amount) {
      return res.status(400).json({ error: 'Name and invested_amount are required' });
    }
    
    await db.addDeal({
      name,
      stage: stage || 'seed',
      valuation: valuation || 0,
      invested_amount,
      ownership_percent: ownership_percent || 0,
      date_invested: date_invested || new Date().toISOString().split('T')[0],
      notes: notes || ''
    });
    
    res.json({ success: true, message: 'Deal added' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Add follow-on round
app.post('/api/deals/:dealId/follow-ons', async (req, res) => {
  try {
    const { round_name, valuation, date_opportunity, available_allocation, notes } = req.body;
    
    await db.addFollowOn({
      deal_id: req.params.dealId,
      round_name: round_name || 'Series A',
      valuation: valuation || 0,
      date_opportunity: date_opportunity || new Date().toISOString().split('T')[0],
      available_allocation: available_allocation || 0,
      notes: notes || ''
    });
    
    res.json({ success: true, message: 'Follow-on added' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Add exit
app.post('/api/deals/:dealId/exits', async (req, res) => {
  try {
    const { type, valuation, proceeds, roi_multiple, exit_date, notes } = req.body;
    
    await db.addExit({
      deal_id: req.params.dealId,
      type: type || 'acquisition',
      valuation: valuation || 0,
      proceeds: proceeds || 0,
      roi_multiple: roi_multiple || 0,
      exit_date: exit_date || new Date().toISOString().split('T')[0],
      notes: notes || ''
    });
    
    res.json({ success: true, message: 'Exit recorded' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get portfolio summary
app.get('/api/summary', async (req, res) => {
  try {
    const deals = await db.getAllDeals();
    
    const summary = {
      totalDeals: deals.length,
      activeDeals: deals.filter(d => d.status === 'active').length,
      totalInvested: deals.reduce((sum, d) => sum + (d.invested_amount || 0), 0),
      averageOwnership: deals.length > 0 ? deals.reduce((sum, d) => sum + (d.ownership_percent || 0), 0) / deals.length : 0,
      dealsByStage: {}
    };
    
    deals.forEach(deal => {
      const stage = deal.stage || 'unknown';
      summary.dealsByStage[stage] = (summary.dealsByStage[stage] || 0) + 1;
    });
    
    res.json(summary);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==================== Web Routes ====================

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`🚀 Angel Dashboard running at http://localhost:${PORT}`);
});
