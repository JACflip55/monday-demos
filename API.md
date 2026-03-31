# API Documentation

## Base URL
```
http://localhost:3000
```

## Endpoints

### Portfolio Summary
**GET** `/api/summary`

Returns high-level portfolio metrics.

**Response:**
```json
{
  "totalDeals": 5,
  "activeDeals": 4,
  "totalInvested": 1825000,
  "averageOwnership": 0.98,
  "dealsByStage": {
    "seed": 2,
    "series-a": 2,
    "series-b": 1
  }
}
```

---

### List All Deals
**GET** `/api/deals`

Returns all deals with enriched data (follow-ons and exits).

**Response:**
```json
[
  {
    "id": 1,
    "name": "TechFlow",
    "stage": "seed",
    "valuation": 8000000,
    "invested_amount": 100000,
    "ownership_percent": 1.25,
    "date_invested": "2024-03-15",
    "status": "active",
    "notes": "AI workflow automation, strong founding team",
    "followOns": [
      {
        "id": 1,
        "deal_id": 1,
        "round_name": "Series A",
        "valuation": 25000000,
        "date_opportunity": "2024-09-01",
        "available_allocation": 250000,
        "notes": "Oversubscribed round, lead investor is Sequoia"
      }
    ],
    "exits": []
  }
]
```

---

### Get Single Deal
**GET** `/api/deals/:id`

Returns details for a specific deal including follow-ons and exits.

**Parameters:**
- `id` (path) - Deal ID

**Response:**
```json
{
  "id": 1,
  "name": "TechFlow",
  "stage": "seed",
  "valuation": 8000000,
  "invested_amount": 100000,
  "ownership_percent": 1.25,
  "date_invested": "2024-03-15",
  "status": "active",
  "notes": "AI workflow automation, strong founding team",
  "followOns": [],
  "exits": []
}
```

---

### Add New Deal
**POST** `/api/deals`

Create a new angel investment.

**Request Body:**
```json
{
  "name": "OpenAI",
  "stage": "series-a",
  "valuation": 80000000,
  "invested_amount": 250000,
  "ownership_percent": 0.31,
  "date_invested": "2024-03-01",
  "notes": "GPT research, Ilya + Sam leading"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Deal added"
}
```

**Required Fields:**
- `name` - Company name (must be unique)
- `invested_amount` - Amount invested in dollars

**Optional Fields:**
- `stage` - Default: "seed"
- `valuation` - Post-money valuation
- `ownership_percent` - Ownership stake
- `date_invested` - Default: today
- `notes` - Free-form notes

---

### Add Follow-On Round
**POST** `/api/deals/:dealId/follow-ons`

Log a follow-on investment opportunity.

**Parameters:**
- `dealId` (path) - Parent deal ID

**Request Body:**
```json
{
  "round_name": "Series B",
  "valuation": 250000000,
  "date_opportunity": "2024-09-15",
  "available_allocation": 500000,
  "notes": "Lead: a16z, looking for strong LPs"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Follow-on added"
}
```

---

### Record an Exit
**POST** `/api/deals/:dealId/exits`

Log the sale or exit of an investment.

**Parameters:**
- `dealId` (path) - Parent deal ID

**Request Body:**
```json
{
  "type": "acquisition",
  "valuation": 500000000,
  "proceeds": 1550000,
  "roi_multiple": 6.2,
  "exit_date": "2024-12-01",
  "notes": "Acquired by Google"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Exit recorded"
}
```

**Exit Types:**
- `acquisition` - Bought by another company
- `ipo` - Initial Public Offering
- `liquidation` - Company shut down
- `secondary` - Sold your shares to another investor

---

## Example Workflows

### Workflow 1: Log a New Investment

```bash
# 1. Add the deal
curl -X POST http://localhost:3000/api/deals \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Anthropic",
    "stage": "series-c",
    "valuation": 5000000000,
    "invested_amount": 1000000,
    "ownership_percent": 0.02,
    "date_invested": "2024-01-15",
    "notes": "Leading AI safety research"
  }'

# 2. Check portfolio summary
curl http://localhost:3000/api/summary

# 3. View all deals
curl http://localhost:3000/api/deals
```

### Workflow 2: Track Follow-On Investment

```bash
# 1. Identify the deal ID (from list endpoint)
# Assuming ID = 3

# 2. Add follow-on opportunity
curl -X POST http://localhost:3000/api/deals/3/follow-ons \
  -H "Content-Type: application/json" \
  -d '{
    "round_name": "Series D",
    "valuation": 10000000000,
    "date_opportunity": "2024-06-01",
    "available_allocation": 2000000,
    "notes": "Series D at 2x Series C valuation"
  }'

# 3. Get updated deal with follow-on
curl http://localhost:3000/api/deals/3
```

### Workflow 3: Record an Exit (Success)

```bash
# Record when one of your deals exits

curl -X POST http://localhost:3000/api/deals/1/exits \
  -H "Content-Type: application/json" \
  -d '{
    "type": "acquisition",
    "valuation": 350000000,
    "proceeds": 2800000,
    "roi_multiple": 28,
    "exit_date": "2024-11-20",
    "notes": "Acquired by Meta for $350M"
  }'
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad request (missing required field)
- `404` - Resource not found
- `500` - Server error

**Error Response:**
```json
{
  "error": "Deal with name 'TechFlow' already exists"
}
```

---

## Performance Notes

- All responses are JSON
- No pagination implemented yet (suitable for <500 deals)
- Database queries are indexed on `deal_id` for fast follow-on/exit lookups
- Should add pagination if dealing with >1000 records

---

## Future API Extensions

- `PATCH /api/deals/:id` - Update deal details
- `DELETE /api/deals/:id` - Remove a deal
- `GET /api/deals/stage/:stage` - Filter by stage
- `GET /api/deals/search?q=name` - Search deals
- `GET /api/performance` - ROI analytics
- `GET /api/export/csv` - Export portfolio data
