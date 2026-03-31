import Database from './db.js';

const db = new Database();

async function seedData() {
  try {
    await db.init();
    
    // Sample deals
    const deals = [
      {
        name: 'TechFlow',
        stage: 'seed',
        valuation: 8000000,
        invested_amount: 100000,
        ownership_percent: 1.25,
        date_invested: '2024-03-15',
        notes: 'AI workflow automation, strong founding team'
      },
      {
        name: 'GreenScale',
        stage: 'series-a',
        valuation: 45000000,
        invested_amount: 500000,
        ownership_percent: 1.1,
        date_invested: '2023-11-20',
        notes: 'Sustainable supply chain, pharma focus'
      },
      {
        name: 'DataVault',
        stage: 'seed',
        valuation: 6000000,
        invested_amount: 75000,
        ownership_percent: 1.25,
        date_invested: '2024-01-10',
        notes: 'Privacy-first data analytics'
      },
      {
        name: 'CloudPulse',
        stage: 'series-b',
        valuation: 180000000,
        invested_amount: 1000000,
        ownership_percent: 0.55,
        date_invested: '2022-06-01',
        notes: 'Real-time monitoring platform'
      },
      {
        name: 'FinServe',
        stage: 'series-a',
        valuation: 32000000,
        invested_amount: 250000,
        ownership_percent: 0.78,
        date_invested: '2024-02-14',
        notes: 'Underbanked financial services'
      }
    ];
    
    // Add deals
    for (const deal of deals) {
      try {
        await db.addDeal(deal);
        console.log(`✓ Added ${deal.name}`);
      } catch (e) {
        console.log(`~ ${deal.name} already exists`);
      }
    }
    
    // Add some follow-ons
    try {
      await db.addFollowOn({
        deal_id: 1,
        round_name: 'Series A',
        valuation: 25000000,
        date_opportunity: '2024-09-01',
        available_allocation: 250000,
        notes: 'Oversubscribed round, lead investor is Sequoia'
      });
      console.log(`✓ Added follow-on for TechFlow`);
    } catch (e) {}
    
    try {
      await db.addFollowOn({
        deal_id: 2,
        round_name: 'Series B',
        valuation: 120000000,
        date_opportunity: '2024-10-15',
        available_allocation: 500000,
        notes: 'Looking to dilute minimally'
      });
      console.log(`✓ Added follow-on for GreenScale`);
    } catch (e) {}
    
    // Add an exit
    try {
      await db.addExit({
        deal_id: 4,
        type: 'acquisition',
        valuation: 280000000,
        proceeds: 2800000,
        roi_multiple: 2.8,
        exit_date: '2024-08-20',
        notes: 'Acquired by Oracle'
      });
      console.log(`✓ Added exit for CloudPulse`);
    } catch (e) {}
    
    console.log('\n✅ Seed data loaded!\n');
    
  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    db.close();
  }
}

seedData();
