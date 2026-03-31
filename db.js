import sqlite3 from 'sqlite3';
import { promisify } from 'util';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const dbPath = path.join(__dirname, 'deals.db');

class Database {
  constructor() {
    this.db = new sqlite3.Database(dbPath);
    this.run = promisify(this.db.run.bind(this.db));
    this.get = promisify(this.db.get.bind(this.db));
    this.all = promisify(this.db.all.bind(this.db));
  }

  async init() {
    await this.run(`
      CREATE TABLE IF NOT EXISTS deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        stage TEXT,
        valuation REAL,
        invested_amount REAL,
        ownership_percent REAL,
        date_invested TEXT,
        status TEXT DEFAULT 'active',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);

    await this.run(`
      CREATE TABLE IF NOT EXISTS follow_ons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deal_id INTEGER NOT NULL,
        round_name TEXT,
        valuation REAL,
        date_opportunity TEXT,
        available_allocation REAL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(deal_id) REFERENCES deals(id)
      )
    `);

    await this.run(`
      CREATE TABLE IF NOT EXISTS exits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deal_id INTEGER NOT NULL,
        type TEXT,
        valuation REAL,
        proceeds REAL,
        roi_multiple REAL,
        exit_date TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(deal_id) REFERENCES deals(id)
      )
    `);
  }

  async addDeal(deal) {
    const result = await this.run(
      `INSERT INTO deals (name, stage, valuation, invested_amount, ownership_percent, date_invested, status, notes)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
      [deal.name, deal.stage, deal.valuation, deal.invested_amount, deal.ownership_percent, deal.date_invested, deal.status || 'active', deal.notes]
    );
    return result;
  }

  async getAllDeals() {
    return this.all(`SELECT * FROM deals ORDER BY date_invested DESC`);
  }

  async getDeal(id) {
    return this.get(`SELECT * FROM deals WHERE id = ?`, [id]);
  }

  async addFollowOn(followOn) {
    return this.run(
      `INSERT INTO follow_ons (deal_id, round_name, valuation, date_opportunity, available_allocation, notes)
       VALUES (?, ?, ?, ?, ?, ?)`,
      [followOn.deal_id, followOn.round_name, followOn.valuation, followOn.date_opportunity, followOn.available_allocation, followOn.notes]
    );
  }

  async getFollowOns(dealId) {
    return this.all(`SELECT * FROM follow_ons WHERE deal_id = ? ORDER BY date_opportunity DESC`, [dealId]);
  }

  async addExit(exit) {
    return this.run(
      `INSERT INTO exits (deal_id, type, valuation, proceeds, roi_multiple, exit_date, notes)
       VALUES (?, ?, ?, ?, ?, ?, ?)`,
      [exit.deal_id, exit.type, exit.valuation, exit.proceeds, exit.roi_multiple, exit.exit_date, exit.notes]
    );
  }

  async getExits(dealId) {
    return this.all(`SELECT * FROM exits WHERE deal_id = ? ORDER BY exit_date DESC`, [dealId]);
  }

  async updateDealStatus(id, status) {
    return this.run(`UPDATE deals SET status = ? WHERE id = ?`, [status, id]);
  }

  close() {
    this.db.close();
  }
}

export default Database;
