# Integration Guide — Production Deployment

**How to integrate the Sneaker Fraud Intel system into GOAT's production stack**

---

## Architecture Overview

```
┌─────────────────┐
│  Seller Lists   │
│  New Item       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  Fraud Scoring  │─────▶│  Decision Engine │
│  API Service    │      │  (Block/Auth/OK) │
└────────┬────────┘      └────────┬─────────┘
         │                        │
         ▼                        ▼
┌─────────────────┐      ┌──────────────────┐
│  Feature Store  │      │  Authentication  │
│  (Historical)   │      │  Pipeline        │
└─────────────────┘      └──────────────────┘
```

---

## Phase 1: Data Pipeline Setup

### Step 1.1: Identify Data Sources

**Required tables/collections:**

```sql
-- Sellers table
SELECT 
  seller_id,
  created_at,
  location,
  verified_business,
  verified_social_media,
  total_sales,
  total_returns,
  avg_feedback_score
FROM sellers;

-- Transactions table
SELECT
  transaction_id,
  seller_id,
  item_id,
  sale_price,
  sale_date,
  return_initiated,
  negative_feedback
FROM transactions;

-- Listings table
SELECT
  listing_id,
  seller_id,
  item_sku,
  price,
  market_price,
  quantity,
  sizes_available,
  photo_urls,
  description,
  created_at
FROM listings;
```

### Step 1.2: Build Feature Engineering Pipeline

Create a service that transforms raw data into `SellerProfile` and `ListingSignals`:

```python
# feature_engineering.py

from datetime import datetime, timedelta
from typing import Dict, List
from fraud_intel import SellerProfile, ListingSignals

class FeatureEngineer:
    """Transforms database records into fraud detection features"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def build_seller_profile(self, seller_id: str) -> SellerProfile:
        """Query database and construct SellerProfile"""
        
        # Query seller data
        seller = self.db.query(f"SELECT * FROM sellers WHERE id = '{seller_id}'")
        
        # Query transactions
        transactions = self.db.query(f"""
            SELECT * FROM transactions 
            WHERE seller_id = '{seller_id}'
            ORDER BY sale_date DESC
        """)
        
        # Calculate derived features
        account_age = (datetime.now() - seller['created_at']).days
        total_sales = len(transactions)
        
        high_value_count = sum(1 for t in transactions if t['sale_price'] > 500)
        avg_price = sum(t['sale_price'] for t in transactions) / max(total_sales, 1)
        
        returns = sum(1 for t in transactions if t['return_initiated'])
        return_rate = returns / max(total_sales, 1)
        
        negative_feedback = sum(1 for t in transactions if t['negative_feedback'])
        negative_feedback_pct = (negative_feedback / max(total_sales, 1)) * 100
        
        # Check for rapid listing activity
        recent_listings = self.db.query(f"""
            SELECT COUNT(*) as count
            FROM listings
            WHERE seller_id = '{seller_id}'
            AND created_at > NOW() - INTERVAL 1 DAY
        """)
        
        rapid_listing_count = recent_listings['count']
        
        # Geographic risk check
        counterfeit_regions = ["Putian", "Guangzhou", "Dongguan"]
        ships_from_risk_region = any(
            region in seller['location'] 
            for region in counterfeit_regions
        )
        
        return SellerProfile(
            seller_id=seller_id,
            account_age_days=account_age,
            total_sales=total_sales,
            categories_sold=self._get_seller_categories(seller_id),
            avg_price=avg_price,
            high_value_count=high_value_count,
            return_rate=return_rate,
            negative_feedback_pct=negative_feedback_pct,
            new_in_box_pct=self._calculate_nib_pct(transactions),
            rapid_listing_count=rapid_listing_count,
            location=seller['location'],
            ships_from_known_counterfeit_region=ships_from_risk_region,
            social_media_verified=seller['verified_social_media'],
            business_entity=seller['verified_business']
        )
    
    def build_listing_signals(self, seller_id: str, limit: int = 20) -> List[ListingSignals]:
        """Get recent listing signals for seller"""
        
        listings = self.db.query(f"""
            SELECT * FROM listings
            WHERE seller_id = '{seller_id}'
            ORDER BY created_at DESC
            LIMIT {limit}
        """)
        
        signals = []
        for listing in listings:
            # Calculate price vs market
            below_market_pct = 0.0
            if listing['market_price'] > 0:
                below_market_pct = (
                    (listing['market_price'] - listing['price']) / 
                    listing['market_price'] * 100
                )
            
            # Check for stock photo usage (simple heuristic)
            stock_photo_used = self._is_stock_photo(listing['photo_urls'])
            
            # Multiple sizes available
            multiple_sizes = len(listing['sizes_available']) > 1
            
            # New release check
            item_release_date = self._get_item_release_date(listing['item_sku'])
            days_since_release = (datetime.now() - item_release_date).days if item_release_date else 999
            new_release_immediate_stock = days_since_release < 7
            
            signals.append(ListingSignals(
                below_market_pct=max(below_market_pct, 0),
                stock_photo_used=stock_photo_used,
                description_copied=self._check_description_similarity(listing['description']),
                multiple_sizes_available=multiple_sizes,
                new_release_immediate_stock=new_release_immediate_stock,
                bulk_quantity=listing['quantity'],
                inconsistent_photos=self._check_photo_consistency(listing['photo_urls'])
            ))
        
        return signals
    
    def _get_seller_categories(self, seller_id: str) -> List[str]:
        """Get unique categories sold by seller"""
        result = self.db.query(f"""
            SELECT DISTINCT category
            FROM listings
            WHERE seller_id = '{seller_id}'
        """)
        return [r['category'] for r in result]
    
    def _calculate_nib_pct(self, transactions: List[Dict]) -> float:
        """Calculate percentage of NIB items"""
        nib_count = sum(1 for t in transactions if t['condition'] == 'new_in_box')
        return (nib_count / max(len(transactions), 1)) * 100
    
    def _is_stock_photo(self, photo_urls: List[str]) -> bool:
        """Simple check for stock photos (enhance with image analysis)"""
        # Placeholder: Could integrate with reverse image search
        # For now, check if photos match known brand URLs
        brand_domains = ['nike.com', 'adidas.com', 'newbalance.com']
        return any(domain in url for url in photo_urls for domain in brand_domains)
    
    def _check_description_similarity(self, description: str) -> bool:
        """Check if description is copied from other listings"""
        # Placeholder: Could integrate with text similarity search
        # For now, just check for template language
        template_phrases = [
            "100% authentic",
            "deadstock",
            "BNIB",
            "fast shipping",
            "trusted seller"
        ]
        matches = sum(1 for phrase in template_phrases if phrase.lower() in description.lower())
        return matches >= 3
    
    def _get_item_release_date(self, sku: str) -> datetime:
        """Get official release date for item"""
        result = self.db.query(f"SELECT release_date FROM items WHERE sku = '{sku}'")
        return result['release_date'] if result else None
    
    def _check_photo_consistency(self, photo_urls: List[str]) -> bool:
        """Check if photos have consistent quality/background"""
        # Placeholder: Could integrate with computer vision
        # For now, return False (assume consistent)
        return False
```

### Step 1.3: Create Feature Store

Cache computed features to avoid recalculation:

```python
# feature_store.py

import redis
import json
from datetime import timedelta

class FeatureStore:
    """Redis-backed cache for seller features"""
    
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis = redis.Redis(host=redis_host, port=redis_port)
        self.ttl = timedelta(hours=6)  # Refresh every 6 hours
    
    def get_seller_features(self, seller_id: str):
        """Get cached features or return None"""
        key = f"fraud:features:{seller_id}"
        data = self.redis.get(key)
        return json.loads(data) if data else None
    
    def set_seller_features(self, seller_id: str, profile_dict: dict, signals_dict: list):
        """Cache seller features"""
        key = f"fraud:features:{seller_id}"
        data = json.dumps({
            'profile': profile_dict,
            'signals': signals_dict,
            'cached_at': datetime.now().isoformat()
        })
        self.redis.setex(key, self.ttl, data)
    
    def invalidate(self, seller_id: str):
        """Clear cache for seller (call after new transaction)"""
        key = f"fraud:features:{seller_id}"
        self.redis.delete(key)
```

---

## Phase 2: API Service

### Step 2.1: Build Fraud Scoring API

```python
# fraud_api.py

from flask import Flask, request, jsonify
from fraud_intel import FraudAnalyzer, SellerProfile, ListingSignals
from feature_engineering import FeatureEngineer
from feature_store import FeatureStore
from dataclasses import asdict

app = Flask(__name__)

# Initialize components
analyzer = FraudAnalyzer()
engineer = FeatureEngineer(db_connection)
store = FeatureStore()

@app.route('/api/v1/fraud/analyze', methods=['POST'])
def analyze_seller():
    """Analyze seller fraud risk"""
    
    data = request.json
    seller_id = data.get('seller_id')
    
    if not seller_id:
        return jsonify({'error': 'seller_id required'}), 400
    
    # Try to get from cache
    cached = store.get_seller_features(seller_id)
    
    if cached:
        profile = SellerProfile(**cached['profile'])
        signals = [ListingSignals(**s) for s in cached['signals']]
    else:
        # Compute features
        profile = engineer.build_seller_profile(seller_id)
        signals = engineer.build_listing_signals(seller_id)
        
        # Cache for next time
        store.set_seller_features(
            seller_id,
            asdict(profile),
            [asdict(s) for s in signals]
        )
    
    # Run fraud analysis
    score = analyzer.analyze_seller(profile, signals)
    
    # Log for monitoring
    log_fraud_analysis(score)
    
    return jsonify({
        'seller_id': seller_id,
        'score': score.overall_score,
        'risk_level': score.risk_level.value,
        'confidence': score.confidence,
        'recommended_action': score.recommended_action,
        'red_flags': score.red_flags,
        'green_flags': score.green_flags,
        'timestamp': score.timestamp
    })

@app.route('/api/v1/fraud/batch', methods=['POST'])
def batch_analyze():
    """Batch analyze multiple sellers"""
    
    data = request.json
    seller_ids = data.get('seller_ids', [])
    
    results = []
    for seller_id in seller_ids:
        try:
            # Reuse single-seller logic
            result = analyze_seller_internal(seller_id)
            results.append(result)
        except Exception as e:
            results.append({
                'seller_id': seller_id,
                'error': str(e)
            })
    
    return jsonify({'results': results})

@app.route('/api/v1/fraud/invalidate', methods=['POST'])
def invalidate_cache():
    """Invalidate cached features after new transaction"""
    
    data = request.json
    seller_id = data.get('seller_id')
    
    store.invalidate(seller_id)
    
    return jsonify({'status': 'invalidated'})

def analyze_seller_internal(seller_id: str):
    """Internal helper for batch processing"""
    # ... (same logic as analyze_seller endpoint)
    pass

def log_fraud_analysis(score):
    """Log analysis for monitoring/training"""
    # Write to analytics database
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Step 2.2: Deploy API Service

```yaml
# docker-compose.yml

version: '3.8'

services:
  fraud-api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/goat
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
  
  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=goat
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
```

```dockerfile
# Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fraud_intel.py .
COPY feature_engineering.py .
COPY feature_store.py .
COPY fraud_api.py .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "fraud_api:app"]
```

```
# requirements.txt

flask==3.0.0
gunicorn==21.2.0
redis==5.0.0
psycopg2-binary==2.9.9
```

---

## Phase 3: Decision Engine Integration

### Step 3.1: Modify Listing Acceptance Flow

```python
# listing_handler.py (GOAT backend)

from fraud_api_client import FraudAPIClient

fraud_client = FraudAPIClient('http://fraud-api:5000')

def process_new_listing(seller_id, listing_data):
    """Process new listing with fraud check"""
    
    # Call fraud scoring API
    fraud_result = fraud_client.analyze(seller_id)
    
    risk_level = fraud_result['risk_level']
    score = fraud_result['score']
    
    # Decision tree
    if risk_level == 'CRITICAL' and score > 85:
        return {
            'status': 'REJECTED',
            'reason': 'Unable to accept listing at this time',
            'internal_reason': 'High fraud risk',
            'score': score
        }
    
    elif risk_level in ['HIGH', 'CRITICAL']:
        # Accept but require enhanced authentication
        listing_id = create_listing(listing_data)
        
        # Flag for enhanced review
        flag_for_enhanced_auth(listing_id, fraud_result)
        
        return {
            'status': 'ACCEPTED',
            'listing_id': listing_id,
            'authentication_level': 'ENHANCED',
            'additional_requirements': [
                'Purchase receipt required',
                'Additional photos required',
                'Manual authenticator review'
            ]
        }
    
    else:
        # Standard flow
        listing_id = create_listing(listing_data)
        
        return {
            'status': 'ACCEPTED',
            'listing_id': listing_id,
            'authentication_level': 'STANDARD'
        }

def flag_for_enhanced_auth(listing_id, fraud_result):
    """Add listing to enhanced authentication queue"""
    
    db.execute("""
        INSERT INTO authentication_queue (
            listing_id,
            priority,
            fraud_score,
            red_flags,
            requires_manual_review
        ) VALUES (%s, %s, %s, %s, %s)
    """, [
        listing_id,
        'HIGH',
        fraud_result['score'],
        json.dumps(fraud_result['red_flags']),
        True
    ])
```

### Step 3.2: Authenticator Dashboard Updates

Show fraud scores to human authenticators:

```python
# authenticator_dashboard.py

def get_next_item_to_authenticate(authenticator_id):
    """Get next item with context"""
    
    item = db.query("""
        SELECT 
            a.listing_id,
            a.fraud_score,
            a.red_flags,
            l.seller_id,
            l.item_sku,
            s.location
        FROM authentication_queue a
        JOIN listings l ON a.listing_id = l.id
        JOIN sellers s ON l.seller_id = s.id
        WHERE a.status = 'PENDING'
        ORDER BY a.priority DESC, a.created_at ASC
        LIMIT 1
    """)
    
    return {
        'listing_id': item['listing_id'],
        'item_sku': item['item_sku'],
        'seller_location': item['location'],
        'fraud_context': {
            'score': item['fraud_score'],
            'risk_level': get_risk_level(item['fraud_score']),
            'red_flags': json.loads(item['red_flags']),
            'extra_attention_needed': item['fraud_score'] > 60
        }
    }
```

---

## Phase 4: Monitoring & Feedback Loop

### Step 4.1: Track Authentication Outcomes

```python
# feedback_loop.py

def record_authentication_result(listing_id, outcome):
    """Record authentication outcome for model training"""
    
    # outcome: 'AUTHENTIC', 'COUNTERFEIT', 'UNCERTAIN'
    
    # Get fraud score for this listing
    fraud_data = db.query("""
        SELECT fraud_score, red_flags
        FROM authentication_queue
        WHERE listing_id = %s
    """, [listing_id])
    
    # Log for training
    db.execute("""
        INSERT INTO fraud_training_data (
            listing_id,
            fraud_score,
            red_flags,
            actual_outcome,
            logged_at
        ) VALUES (%s, %s, %s, %s, NOW())
    """, [
        listing_id,
        fraud_data['fraud_score'],
        fraud_data['red_flags'],
        outcome
    ])
    
    # Update metrics
    update_model_metrics(fraud_data['fraud_score'], outcome)

def update_model_metrics(predicted_score, actual_outcome):
    """Track true/false positives for monitoring"""
    
    # High score = predicted fraud
    predicted_fraud = predicted_score > 60
    actual_fraud = actual_outcome == 'COUNTERFEIT'
    
    if predicted_fraud and actual_fraud:
        increment_metric('true_positive')
    elif predicted_fraud and not actual_fraud:
        increment_metric('false_positive')
    elif not predicted_fraud and actual_fraud:
        increment_metric('false_negative')
    else:
        increment_metric('true_negative')
```

### Step 4.2: Monitoring Dashboard

```python
# monitoring.py

def get_fraud_metrics(time_period='24h'):
    """Get performance metrics"""
    
    metrics = db.query("""
        SELECT
            COUNT(*) as total_analyzed,
            SUM(CASE WHEN fraud_score > 80 THEN 1 ELSE 0 END) as critical_count,
            SUM(CASE WHEN fraud_score BETWEEN 60 AND 80 THEN 1 ELSE 0 END) as high_count,
            AVG(fraud_score) as avg_score,
            
            -- Outcome metrics (from authentication results)
            SUM(CASE WHEN actual_outcome = 'COUNTERFEIT' THEN 1 ELSE 0 END) as total_fakes,
            SUM(CASE WHEN fraud_score > 60 AND actual_outcome = 'COUNTERFEIT' THEN 1 ELSE 0 END) as caught_fakes,
            SUM(CASE WHEN fraud_score > 60 AND actual_outcome = 'AUTHENTIC' THEN 1 ELSE 0 END) as false_positives
        FROM fraud_training_data
        WHERE logged_at > NOW() - INTERVAL '1 day'
    """)
    
    recall = metrics['caught_fakes'] / max(metrics['total_fakes'], 1)
    precision = metrics['caught_fakes'] / max(metrics['caught_fakes'] + metrics['false_positives'], 1)
    
    return {
        'total_analyzed': metrics['total_analyzed'],
        'avg_score': round(metrics['avg_score'], 2),
        'critical_count': metrics['critical_count'],
        'high_count': metrics['high_count'],
        'recall': round(recall, 3),
        'precision': round(precision, 3),
        'f1_score': round(2 * (precision * recall) / (precision + recall), 3)
    }
```

---

## Phase 5: Model Improvement

### Step 5.1: Retrain with Historical Data

```python
# model_training.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def retrain_model():
    """Retrain fraud model with historical outcomes"""
    
    # Load training data
    data = pd.read_sql("""
        SELECT 
            fraud_score,
            seller_signals,
            listing_signals,
            CASE WHEN actual_outcome = 'COUNTERFEIT' THEN 1 ELSE 0 END as label
        FROM fraud_training_data
        WHERE actual_outcome IN ('AUTHENTIC', 'COUNTERFEIT')
    """, db_connection)
    
    # Feature engineering
    X = extract_features(data)
    y = data['label']
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)
    
    # Evaluate
    accuracy = model.score(X_test, y_test)
    
    # Save model
    joblib.dump(model, 'fraud_model_v2.pkl')
    
    return {'accuracy': accuracy}
```

---

## Performance Tuning

### Caching Strategy

- **Feature Store TTL:** 6 hours (balance freshness vs compute)
- **API Response Caching:** 5 minutes (for repeat requests)
- **Database Query Optimization:** Index on `seller_id`, `created_at`

### Scaling Considerations

- **API Service:** Horizontally scale with load balancer
- **Feature Store:** Redis cluster for high availability
- **Database:** Read replicas for heavy query load

### Latency Targets

- **P50:** <100ms
- **P95:** <250ms
- **P99:** <500ms

(Fraud scoring should not slow down listing acceptance)

---

## Security & Privacy

### Data Access Controls

- Fraud scores are **internal only** (never expose to sellers)
- API requires authentication token
- Audit logging for all fraud decisions

### Compliance

- **GDPR:** Allow sellers to request fraud data deletion
- **Transparency:** Provide appeals process for wrongly flagged sellers
- **Non-discrimination:** Regular audits to prevent bias

---

## Rollout Checklist

- [ ] Phase 1: Offline analysis on historical data
- [ ] Phase 2: Shadow mode (log scores, don't act)
- [ ] Phase 3: Pilot with 10% of traffic
- [ ] Phase 4: Full rollout with monitoring
- [ ] Phase 5: Feedback loop + model retraining

---

**Questions? Contact Jack for GOAT-specific integration details.**
