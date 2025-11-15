# CogniSense Backend

**Digital Footprint Tracking & Analysis API** - MVP Phase 1

A FastAPI-based backend service that powers the CogniSense platform for tracking, analyzing, and providing insights into users' digital footprint and online content consumption patterns.

---

## 🚀 Features (Phase 1)

### Core Functionality
- **Content Ingestion API**: Receives text data from browser extension
- **ML-Powered Analysis**:
  - Sentiment Analysis (Positive/Negative/Neutral)
  - Content Categorization (Productivity/Social/Entertainment/News/etc.)
  - Emotion Detection (Joy, Anger, Sadness, Fear, etc.)
  - Emotional Balance Tracking
- **Time Tracking**: Store and aggregate browsing session data
- **User Categorization**: Custom site classifications

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | FastAPI | High-performance async web framework |
| **Server** | Uvicorn | ASGI server |
| **Database** | PostgreSQL | Relational database with JSONB support |
| **ORM** | SQLModel | Type-safe ORM with Pydantic integration |
| **ML Library** | Hugging Face Transformers | Pre-trained NLP models |
| **Authentication** | FastAPI-Users + JWT | User management and auth |
| **Validation** | Pydantic | Data validation and settings |
| **Testing** | Pytest | Unit and integration tests |
| **Dependency Mgmt** | Poetry | Python package management |
| **Containerization** | Docker Compose | Local development environment |

---

## 📁 Project Structure

```
cognisense-backend/
├── app/
│   ├── main.py                    # FastAPI app entry point
│   ├── core/                      # Core configuration
│   │   ├── config.py             # Pydantic settings
│   │   ├── security.py           # JWT & password hashing
│   │   └── logging.py            # Loguru configuration
│   ├── ml/                        # Machine Learning
│   │   ├── model_manager.py      # Singleton model loader
│   │   ├── sentiment_analyzer.py # Sentiment analysis
│   │   ├── zero_shot_classifier.py # Content categorization
│   │   └── emotion_detector.py   # Emotion detection
│   ├── api/v1/                    # API endpoints
│   │   ├── router.py             # Main router
│   │   ├── content.py            # Content analysis endpoints
│   │   ├── tracking.py           # Time tracking endpoints (TODO)
│   │   └── dashboard.py          # Dashboard stats (TODO)
│   ├── models/                    # SQLModel database models (TODO)
│   ├── schemas/                   # Pydantic request/response schemas (TODO)
│   └── services/                  # Business logic layer (TODO)
├── tests/                         # Test suite
├── docker-compose.yml            # Local dev environment
├── Dockerfile                     # Production container
├── pyproject.toml                # Poetry dependencies
└── .env.example                   # Environment variables template
```

---

## 🔧 Setup Instructions

### Prerequisites
- Python 3.12+
- Poetry (for dependency management)
- Docker & Docker Compose (optional, for containerized setup)

### 1. Clone Repository
```bash
git clone https://github.com/DhruvPokhriyal/cognisense-backend.git
cd cognisense-backend
```

### 2. Install Dependencies
```bash
poetry install
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

**Key environment variables:**
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret (generate with `openssl rand -hex 32`)
- `ALLOWED_ORIGINS`: CORS origins for browser extension

### 4. Start Database (Docker)
```bash
docker-compose up postgres -d
```

### 5. Run Migrations (TODO - when database models are ready)
```bash
alembic upgrade head
```

### 6. Start Development Server
```bash
poetry run uvicorn app.main:app --reload
```

Server will be available at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

---

## 🐳 Docker Setup (Alternative)

Run both API and PostgreSQL in containers:

```bash
docker-compose up --build
```

This starts:
- **API**: http://localhost:8000
- **PostgreSQL**: localhost:5432

---

## 🧪 Testing

Run tests with pytest:

```bash
poetry run pytest

# With coverage
poetry run pytest --cov=app --cov-report=html
```

---

## 📡 API Endpoints (Current)

### Health Check
```
GET /
GET /health
```

### Content Analysis (MVP Core)
```
POST /api/v1/content/analyze
```

**Request Body:**
```json
{
  "text": "Your webpage content here...",
  "url": "https://example.com",
  "analyze_sentiment": true,
  "analyze_category": true,
  "analyze_emotions": true
}
```

**Response:**
```json
{
  "text_length": 1234,
  "word_count": 200,
  "url": "https://example.com",
  "sentiment": {
    "label": "POSITIVE",
    "score": 0.9998
  },
  "category": {
    "primary": "Technology",
    "confidence": 0.95,
    "all_categories": [...]
  },
  "emotions": {
    "dominant": {"label": "joy", "score": 0.85},
    "all_emotions": [...],
    "balance": {
      "positive_score": 0.85,
      "negative_score": 0.15,
      "balance": 0.85,
      "is_balanced": false
    }
  }
}
```

---

## 🚧 TODO (Next Steps)

### Database & Models
- [ ] Create SQLModel database models (User, BrowsingSession, ContentSnapshot, etc.)
- [ ] Set up Alembic migrations
- [ ] Implement database session management

### Authentication
- [ ] Integrate FastAPI-Users
- [ ] Create auth endpoints (register, login, logout)
- [ ] Add JWT token authentication to protected routes

### API Endpoints
- [ ] Tracking endpoints (`POST /tracking`, time logging)
- [ ] Categories endpoints (user site classifications)
- [ ] Dashboard endpoints (daily/weekly stats)
- [ ] User profile endpoints

### Services Layer
- [ ] `content_service.py` - Content analysis orchestration
- [ ] `tracking_service.py` - Session tracking logic
- [ ] `aggregation_service.py` - Compute summaries
- [ ] `recommendation_service.py` - Generate suggestions

### Testing
- [ ] Unit tests for ML services
- [ ] Integration tests for API endpoints
- [ ] Test fixtures and mock data

### Deployment
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Deploy to Railway/Render
- [ ] Set up production database
- [ ] Configure production environment variables

---

## 📖 Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and test**
   ```bash
   poetry run pytest
   ```

3. **Format code with ruff**
   ```bash
   poetry run ruff check --fix .
   poetry run ruff format .
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: your feature description"
   git push origin feature/your-feature-name
   ```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📝 License

MIT License

---

## 👥 Authors

- **Dhruv Pokhriyal** - [GitHub](https://github.com/DhruvPokhriyal)

---

## 🙏 Acknowledgments

- Hugging Face for pre-trained models
- FastAPI framework
- SQLModel and Pydantic teams
