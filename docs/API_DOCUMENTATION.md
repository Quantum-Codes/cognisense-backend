# API Documentation

## CogniSense Backend API

### Overview
CogniSense Backend is a FastAPI service that provides comprehensive digital footprint tracking with ML-powered content analysis. The system tracks user activity, analyzes content sentiment and emotion, categorizes content, and powers a dashboard with insights and wellness metrics.

### Base URL
```
http://localhost:8000
```

### API Version
All endpoints are versioned under `/api/v1/`

### Authentication & Security
- Authentication is powered by Supabase. For authenticated endpoints (notably the Dashboard suite), pass a Supabase JWT using the HTTP Bearer scheme.
- Header: `Authorization: Bearer <SUPABASE_JWT>`
- Requests without a valid token will receive `401 Unauthorized`.
- Public endpoints (e.g., classification helpers) may not require authentication.

Notes about data isolation and privacy:
- User-specific data is isolated per user ID.
- See docs/schema.sql for tables. Key tables include `public.page_view_sessions`, `public.content_analysis`, `public.user_domain_categories`, and `public.user_domain_limits`.

---

## Core Features

### 🔍 **Content Analysis**
- Real-time sentiment analysis with 99%+ confidence
- Emotion detection across 7 emotional states
- Zero-shot content categorization with 54 detailed categories

### 📊 **Activity Tracking** 
- Browser extension integration for seamless data collection
- Engagement metrics (clicks, keypresses, time spent)
- Automatic ML analysis pipeline

### 🎯 **Category Management**
- 54 comprehensive content categories organized into 8 groups
- User-customizable site preferences
- Intelligent content classification

### 📈 **Enhanced Dashboard Analytics**
- Main Dashboard: Weekly activity summaries with trend analysis and improvement tracking
- Insights & Alerts: Notifications about usage patterns, limits, and progress
- Settings Management: Domain categorization and time limit configuration
- Health Scoring: Overall digital wellness metrics and recommendations
- Progress Tracking: Goal-based progress monitoring with actionable insights
- Emotional Analysis: Content consumption emotional balance tracking

### 🔐 **Authentication & Security**
- Supabase-powered user authentication
- JWT token-based secure API access
- User-specific data isolation and privacy

---

## Endpoints Reference (Swagger-verified)
The following endpoints were verified against the Swagger UI you provided. Groups reflect the tags visible in Swagger.

### Health Check

#### GET /api/v1/ping
Simple health check endpoint to verify API availability.

Request:
- No parameters required
- No authentication required

Response:
```json
{
  "message": "pong",
  "api_version": "v1"
}
```

Status Codes:
- 200: API is healthy and running

---

### Content Analysis

#### POST /api/v1/content/analyze
Analyzes provided content for sentiment, emotion, and categorization.

Request Body:
```json
{
  "text": "This is a sample text to analyze",
  "url": "https://example.com",
  "analyze_sentiment": true,
  "analyze_category": true,
  "analyze_emotions": true
}
```

Parameters:
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| text | string | Yes | - | Text content to analyze |
| url | string | No | null | Source URL of the content |
| analyze_sentiment | boolean | No | true | Enable sentiment analysis |
| analyze_category | boolean | No | true | Enable content categorization |
| analyze_emotions | boolean | No | true | Enable emotion detection |

Response:
```json
{
  "text_length": 33,
  "word_count": 7,
  "url": "https://example.com",
  "sentiment": { "label": "POSITIVE", "score": 0.9999 },
  "category": {
    "primary": "Programming",
    "confidence": 0.8234,
    "all_categories": [
      {"label": "Programming", "score": 0.8234},
      {"label": "Documentation", "score": 0.1123},
      {"label": "Learning", "score": 0.0643}
    ]
  },
  "emotions": {
    "dominant": {"label": "joy", "score": 0.9909},
    "all_emotions": [
      {"label": "joy", "score": 0.9909},
      {"label": "optimism", "score": 0.0046},
      {"label": "love", "score": 0.0023},
      {"label": "admiration", "score": 0.0011},
      {"label": "approval", "score": 0.0006}
    ],
    "balance": {
      "positive_score": 0.99,
      "negative_score": 0.01,
      "balance": 0.99,
      "is_balanced": false
    }
  }
}
```

#### POST /api/v1/content/analyze/batch
Analyze multiple text contents in a single request.

Request Body:
```json
{
  "texts": [
    "I love this new productivity app!",
    "Breaking news: Major tech announcement today",
    "Checking social media updates"
  ]
}
```

Parameters:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| texts | array[string] | Yes | Array of text strings to analyze |

Response:
- Returns an array of analysis results, one for each input text. Each result follows the same structure as the single analysis endpoint. Failed analyses will include an "error" field instead of analysis fields for that item.

Status Codes:
- 200: Batch analysis completed (individual items may have errors)
- 400: Invalid request data (empty array)

---

### Activity Tracking

#### POST /api/v1/tracking/ingest
Ingests activity data from browser extension with real-time ML analysis.

Request Body:
```json
{
  "user_id": "user123",
  "url": "https://github.com/example/repo",
  "title": "GitHub Repository",
  "text": "Python machine learning project with advanced algorithms",
  "start_ts": 1704067200.0,
  "end_ts": 1704067800.0,
  "duration_seconds": 600,
  "clicks": 15,
  "keypresses": 245,
  "engagement_score": 0.85
}
```

Response:
```json
{ "status": "ok", "ingested": 1 }
```

#### GET /api/v1/tracking/activity/{user_id}
Retrieves recent activity records for a user.

Query Parameters:
- limit (optional): Number of records to return (1-1000, default: 100)

Example:
```bash
curl "http://localhost:8000/api/v1/tracking/activity/user123?limit=50"
```

Response:
```json
{
  "user_id": "user123",
  "count": 50,
  "items": [
    {
      "user_id": "user123",
      "url": "https://github.com/example/repo",
      "title": "GitHub Repository",
      "text": "Python machine learning project with advanced algorithms",
      "duration_seconds": 600.0,
      "clicks": 15,
      "keypresses": 245,
      "sentiment": { "label": "POSITIVE", "confidence": 0.9999 },
      "classified_category": "Programming",
      "category_group": "Productive",
      "emotions": { "joy": 0.9909, "optimism": 0.0046 },
      "received_at": 1704067800.0
    }
  ]
}
```

#### DELETE /api/v1/tracking/activity/{user_id}
Clears all activity data for a user (useful for testing).

Response:
```json
{ "status": "ok", "removed": 25 }
```

---

### Category Management

#### GET /api/v1/categories/labels
Returns all 54 available content categories.

Response:
```json
{
  "categories": [
    "Programming", "Documentation", "Code Review", "Technical Writing",
    "Social Media", "Messaging", "Video Calls", "Forums",
    "Streaming", "Gaming", "Music", "Videos", "Reading",
    "News", "Research", "Learning", "Reference",
    "Shopping", "Finance", "Travel", "Health",
    "Email", "Calendar", "Notes", "Utilities",
    "Adult Content", "Gambling", "Excessive Gaming",
    "Uncategorized", "Personal", "Other"
  ],
  "total": 54
}
```

#### GET /api/v1/categories/groups
Returns categories organized by functional groups.

Response:
```json
{
  "groups": {
    "Productive": ["Programming", "Documentation", "Code Review", "Technical Writing", "Project Management", "Development Tools", "Design"],
    "Social": ["Social Media", "Messaging", "Video Calls", "Forums", "Dating", "Community"],
    "Entertainment": ["Streaming", "Gaming", "Music", "Videos", "Reading", "Sports", "Hobbies"],
    "Information": ["News", "Research", "Learning", "Reference", "Science", "Technology"],
    "Lifestyle": ["Shopping", "Finance", "Travel", "Health", "Food", "Fitness", "Fashion"],
    "Commerce": ["Business", "Marketing", "Sales", "E-commerce", "Banking", "Investment"],
    "Problematic": ["Adult Content", "Gambling", "Excessive Gaming", "Harmful Content"],
    "Other": ["Uncategorized", "Personal", "Utilities", "Email", "Calendar", "Notes"]
  }
}
```

#### GET /api/v1/categories/classify
Classifies text using zero-shot classification.

Query Parameters:
- text (required): Text to classify

Example:
```bash
curl "http://localhost:8000/api/v1/categories/classify?text=Building%20a%20React%20application"
```

Response:
```json
{ "labels": ["Programming", "Documentation", "Learning"], "scores": [0.8234, 0.1123, 0.0643] }
```

#### GET /api/v1/categories/classify/grouped
Classifies text and returns both specific category and broad group.

Query Parameters:
- text (required): Text to classify

Response:
```json
{
  "labels": ["Programming", "Documentation"],
  "scores": [0.8234, 0.1123],
  "category_group": "Productive",
  "top_category": "Programming",
  "confidence": 0.8234
}
```

#### POST /api/v1/categories/user/{user_id}/sites
Sets user preference for site categorization.

Request Body:
```json
{ "user_id": "user123", "site": "github.com", "category": "Programming" }
```

Response:
```json
{ "status": "ok", "site": "github.com", "category": "Programming" }
```

#### GET /api/v1/categories/user/{user_id}/sites
Retrieves user's site categorization preferences.

Response:
```json
{
  "user_id": "user123",
  "preferences": {
    "github.com": "Programming",
    "youtube.com": "Entertainment",
    "stackoverflow.com": "Learning"
  }
}
```

#### POST /api/v1/user-domain-category/user_domain_category/save (Swagger)
Saves a user-defined domain categorization rule. This endpoint is visible under the "User Domain Category" tag in Swagger.

Request Body (example):
```json
{
  "user_id": "00000000-0000-0000-0000-000000000000",
  "domain_pattern": "twitter.com",
  "category": "Social Media",
  "priority": 1
}
```

Notes:
- Upserts a rule per unique (user_id, domain_pattern).
- `priority` (int, optional, default 1) can be used to select the best match when multiple patterns overlap.
- Backed by table `public.user_domain_categories`.

Response (example):
```json
{ "status": "ok", "user_id": "00000000-0000-0000-0000-000000000000", "domain_pattern": "twitter.com", "category": "Social Media", "priority": 1 }
```

---

### Dashboard Analytics (Authenticated)
These endpoints require a Supabase JWT in the Authorization header.

Common:
- Base path: `/api/v1`
- Auth: `Authorization: Bearer <SUPABASE_JWT>`
- Query param `timeRange`: `this_week` (default) | `last_week`

#### GET /api/v1/dashboard
Summary and weekly breakdown for the current user.

Request:
- Headers: `Authorization: Bearer <token>`
- Query params: `timeRange` (optional)

Response (200):
```json
{
  "user": { "id": "uuid", "displayName": "Jane Doe", "email": "jane@example.com" },
  "timeRange": "this_week",
  "metrics": [
    { "title": "Total Time", "value": 14040, "change_percent": 15.0, "trend": "up", "improvement_label": "slightly_better" },
    { "title": "Productive Time", "value": 7200, "change_percent": 10.0, "trend": "up", "improvement_label": "slightly_better" },
    { "title": "Social Time", "value": 1800, "change_percent": -8.0, "trend": "down", "improvement_label": "slight_worse" },
    { "title": "Entertainment Time", "value": 3000, "change_percent": 5.0, "trend": "up", "improvement_label": "slightly_better" }
  ],
  "weeklyData": [
    { "day": "Mon", "Productive": 150, "Social": 100, "Entertainment": 80 },
    { "day": "Tue", "Productive": 180, "Social": 120, "Entertainment": 100 },
    { "day": "Wed", "Productive": 200, "Social": 150, "Entertainment": 120 },
    { "day": "Thu", "Productive": 280, "Social": 180, "Entertainment": 200 },
    { "day": "Fri", "Productive": 150, "Social": 120, "Entertainment": 180 },
    { "day": "Sat", "Productive": 100, "Social": 180, "Entertainment": 250 },
    { "day": "Sun", "Productive": 80,  "Social": 150, "Entertainment": 240 }
  ]
}
```

Notes:
- metrics[].value is returned in seconds.
- weeklyData values represent minutes per day for charting.
- Category mapping uses user-defined patterns from `public.user_domain_categories`.

Curl:
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/dashboard?timeRange=this_week"
```

#### GET /api/v1/dashboard/insights
Insights including a summary score, alerts, weekly progress against simple goals, emotional balance, and content category distribution.

Request:
- Headers: `Authorization: Bearer <token>`
- Query params: `timeRange` (optional)

Response (200):
```json
{
  "timeRange": "this_week",
  "summary": {
    "overallHealthScore": 72,
    "productiveTimeRatio": 48,
    "weeklyImprovementPercent": 15
  },
  "alerts": [
    { "id": "alert_neg_content", "type": "warning", "title": "Negative Content Alert", "description": "Your negative content consumption increased by 8% this period. Consider diversifying your sources." },
    { "id": "alert_bubble", "type": "info", "title": "Content Bubble Detected", "description": "You've been in a tech content bubble. Try exploring other topics for a balanced perspective." },
    { "id": "alert_progress", "type": "success", "title": "Great Progress!", "description": "Great job! Your productive screen time increased by 15% compared to last period." }
  ],
  "weeklyProgress": [
    { "goalId": "reduce_social_media", "label": "Reduce Social Media Time", "progressPercent": 65 },
    { "goalId": "increase_productive_hours", "label": "Increase Productive Hours", "progressPercent": 80 },
    { "goalId": "diversify_content", "label": "Diversify Content Sources", "progressPercent": 45 }
  ],
  "emotionalBalance": {
    "balanceScore": 72,
    "segments": [
      { "type": "positive", "value": 45 },
      { "type": "neutral",  "value": 30 },
      { "type": "negative", "value": 15 },
      { "type": "biased",   "value": 10 }
    ]
  },
  "contentCategories": [
    { "category": "technology", "percentage": 35 },
    { "category": "entertainment", "percentage": 25 },
    { "category": "news", "percentage": 18 },
    { "category": "social", "percentage": 15 },
    { "category": "other", "percentage": 7 }
  ]
}
```

Notes:
- Emotional balance aggregates `happy`, `sad+angry`, `neutral` from `public.content_analysis` for the period.
- Alerts are heuristic and compare current vs previous equal-length period.

Curl:
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/dashboard/insights?timeRange=this_week"
```

#### GET /api/v1/dashboard/settings
Combined per-domain settings view showing category and daily limit (if any).

Sources:
- Distinct recent domains from `public.page_view_sessions`
- User patterns from `public.user_domain_categories`
- User limits from `public.user_domain_limits`

Response (200):
```json
{
  "websites": [
    { "name": "github.com",  "category": "Productivity",  "limit": 60 },
    { "name": "youtube.com", "category": null,            "limit": null },
    { "name": "twitter.com", "category": "Social Media", "limit": 30 }
  ]
}
```

Notes:
- `category` is derived from best substring match against `domain_pattern` (nullable).
- `limit` is allowed_minutes per day from `user_domain_limits` (nullable, integer minutes).

Curl:
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/dashboard/settings"
```

---

### Dashboard Summary (Deprecated)
This legacy endpoint appears under the "Dashboard Summary" tag in Swagger. Prefer the authenticated Dashboard endpoints above.

#### GET /api/v1/dashboard-summary/summary/{user_id} (Deprecated)
Provides aggregated activity summary with time-based filtering.

Query Parameters:
- period (optional): "daily" or "weekly" (default: "weekly")

---

## Machine Learning Models

The API uses state-of-the-art transformer models for real-time analysis:

### Sentiment Analysis
- Model: `distilbert-base-uncased-finetuned-sst-2-english`
- Capability: Binary sentiment classification (POSITIVE/NEGATIVE)
- Accuracy: 99%+ confidence on clear sentiment expressions
- Performance: Optimized for real-time processing

### Emotion Detection 
- Model: `j-hartmann/emotion-english-distilroberta-base`
- Emotions: joy, sadness, anger, fear, surprise, disgust, optimism, love, admiration, approval, excitement, caring
- Output: Probability distribution across all emotions
- Use Case: Detailed emotional state analysis of browsing content

### Content Categorization
- Model: `typeform/distilbert-base-uncased-mnli` (Zero-shot)
- Categories: 54 detailed categories across 8 functional groups
- Approach: Zero-shot classification for maximum flexibility
- Coverage: Programming, Social Media, Entertainment, Learning, Shopping, etc.

## Integration Examples

### Browser Extension Integration

```javascript
// Ingest activity with content analysis
async function trackActivity(activityData) {
  const response = await fetch('http://localhost:8000/api/v1/tracking/ingest', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: 'user123',
      url: window.location.href,
      title: document.title,
      text: extractPageText(),
      start_ts: Date.now() / 1000,
      duration_seconds: getSessionDuration(),
      clicks: getClickCount(),
      keypresses: getKeypressCount()
    })
  });
  return response.json();
}

// (Legacy) Get dashboard summary by user_id
async function getDashboard(userId, period = 'weekly') {
  const response = await fetch(
    `http://localhost:8000/api/v1/dashboard-summary/summary/${userId}?period=${period}`
  );
  return response.json();
}
```

### Python Client Example

```python
import requests

# Analyze content
def analyze_content(text, url, user_id):
    response = requests.post('http://localhost:8000/api/v1/content/analyze', json={
        'text': text,
        'url': url,
        'user_id': user_id
    })
    return response.json()

# Get available categories
def get_categories():
    response = requests.get('http://localhost:8000/api/v1/categories/labels')
    return response.json()['categories']

# Classify text
def classify_text(text):
    response = requests.get(
        'http://localhost:8000/api/v1/categories/classify', 
        params={'text': text}
    )
    return response.json()
```

## Error Responses

#### 400 Bad Request
```json
{ "detail": "user_id and url required" }
```

#### 422 Unprocessable Entity  
```json
{
  "detail": [
    { "loc": ["body", "text"], "msg": "field required", "type": "value_error.missing" }
  ]
}
```

#### 500 Internal Server Error
```json
{ "detail": "Classification failed: Model not loaded" }
```

## Performance & Deployment

### Model Loading
- Strategy: Lazy loading to optimize startup time
- Memory: Models load on first request to minimize resource usage
- Caching: Models remain in memory for subsequent requests

### Scalability Considerations
- Phase 1: In-memory storage for rapid prototyping
- Phase 2: Database integration planned for production scale
- Optimization: Model instances are shared across requests

### Rate Limiting
Currently no rate limiting is implemented, but will be added for production deployment.

### Authentication
Supabase-based authentication is used. Dashboard endpoints require a Bearer JWT from Supabase; other endpoints may be public depending on deployment configuration.