import Database from './db.js';
import chalk from 'chalk';
import { table } from 'table';

const db = new Database();

async function main() {
  try {
    await db.init();
    
    console.log(chalk.bold.cyan('\n🤖 Angel Dashboard CLI\n'));
    
    // Show summary
    const deals = await db.getAllDeals();
    
    console.log(chalk.yellow('Portfolio Summary:'));
    console.log(`  • Total Deals: ${deals.length}`);
    console.log(`  • Active: ${deals.filter(d => d.status === 'active').length}`);
    console.log(`  • Total Invested: $${deals.reduce((sum, d) => sum + (d.invested_amount || 0), 0).toLocaleString()}`);
    console.log(`  • Avg Ownership: ${(deals.length > 0 ? deals.reduce((sum, d) => sum + (d.ownership_percent || 0), 0) / deals.length : 0).toFixed(2)}%\n`);
    
    if (deals.length === 0) {
      console.log(chalk.gray('No deals yet. Run: node seed-data.js to add sample data.\n'));
    } else {
      // Build table
      const config = {
        singleLine: true,
        columnDefault: {
          width: 12,
          truncate: true
        }
      };
      
      const data = [
        ['Name', 'Stage', 'Valuation ($M)', 'Invested ($K)', 'Ownership %', 'Status'],
        ...deals.map(d => [
          d.name.substring(0, 12),
          d.stage || '-',
          d.valuation ? (d.valuation / 1000000).toFixed(1) : '-',
          d.invested_amount ? (d.invested_amount / 1000).toFixed(1) : '-',
          d.ownership_percent ? d.ownership_percent.toFixed(2) : '-',
          d.status
        ])
      ];
      
      console.log(chalk.blue('Current Deals:\n'));
      console.log(table(data, config));
      
      // Show opportunities
      let totalFollowOns = 0;
      for (const deal of deals) {
        const followOns = await db.getFollowOns(deal.id);
        totalFollowOns += followOns.length;
      }
      
      if (totalFollowOns > 0) {
        console.log(chalk.yellow(`\n📈 Follow-on Opportunities: ${totalFollowOns} available\n`));
      }
    }
    
    console.log(chalk.green('✅ Start the web interface with: npm start\n'));
    
  } catch (error) {
    console.error(chalk.red('Error:'), error.message);
  } finally {
    db.close();
  }
}

main();
