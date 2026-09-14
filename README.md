# SkillGap AI

An ML-powered personalized skill gap analysis and learning roadmap system for aspiring tech professionals.

## Project Structure

```
skillgap-ai/
├── data/processed/          # Taxonomy JSON + training CSV
├── ml/                      # ML pipeline (preprocessing, training, evaluation, engines)
│   └── model_artifacts/     # Trained .pkl files + benchmark JSON
├── backend/                 # FastAPI REST API
└── frontend/                # React (Vite) web application
```

## Model Performance

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Random Forest (deployed) | 90.6% | 92.7% | 90.4% | 91.5% |
| SVM | 91.2% | 91.3% | 93.2% | 92.2% |
| Naive Bayes | 80.2% | 82.7% | 81.8% | 82.2% |

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+

### 1. Backend Setup

```bash
cd skillgap-ai

# Install dependencies
pip install -r backend/requirements.txt

# (First time only) Generate training data and train the model
python -m ml.preprocessing
python -m ml.train_model

# Start the API server
uvicorn backend.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
cd frontend

npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

> The Vite dev server proxies `/api/*` requests to `http://localhost:8000` automatically.

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Health check |
| `/api/profile` | POST | Save student profile |
| `/api/skillgap` | POST | Get match % + ranked missing skills |
| `/api/roadmap` | POST | Get staged learning roadmap |
| `/api/roles` | GET | Browse all roles and their skills |
| `/api/roles/{role_name}` | GET | Get skills for a specific role |
| `/api/progress` | POST | Save skill completion progress |
| `/api/progress/{student_id}/{role}` | GET | Retrieve saved progress |

### Example Request

```bash
curl -X POST http://localhost:8000/api/skillgap \
  -H "Content-Type: application/json" \
  -d '{
    "current_skills": ["Python", "SQL", "Pandas"],
    "target_role": "Data Scientist",
    "projects": ["EDA Project"],
    "experience_level": "Intermediate"
  }'
```

## Covered Roles

- **Data Scientist** — Python, Statistics, ML, Deep Learning, NLP
- **Backend Developer** — REST APIs, SQL, Docker, CI/CD
- **ML Engineer** — ML Deployment, MLOps, Deep Learning
- **Frontend Developer** — React, TypeScript, State Management

## Deployment

### Backend (Render)

1. Create a new Web Service on [Render](https://render.com)
2. Set **Build Command**: `pip install -r backend/requirements.txt && python -m ml.train_model`
3. Set **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. Set **Root Directory** to the repo root

### Frontend (Vercel / Netlify)

1. Push the repo to GitHub
2. Import on [Vercel](https://vercel.com) or [Netlify](https://netlify.com)
3. Set **Root Directory**: `frontend`
4. Set **Build Command**: `npm run build`
5. Set **Output Directory**: `dist`
6. Add environment variable: `VITE_API_URL=https://your-render-backend-url.onrender.com`
7. Update `frontend/vite.config.js` proxy target to match your deployed backend URL

## ML Architecture

- **Dataset**: 2,500 synthetic rows across 4 roles, generated via weighted-skill-coverage rule
- **Feature Engineering**: MultiLabelBinarizer for skills, LabelEncoder for role/experience
- **Model**: Random Forest (200 trees, max_depth=15, class_weight=balanced)
- **Recommendation**: Pure rule-based — sorts missing skills by weight descending
- **Roadmap Sequencing**: Pure rule-based — groups by stage (Foundational → Intermediate → Applied)

## Development Notes

- No comments anywhere in the codebase — code is self-explanatory through naming
- Progress data is persisted in `backend/progress.db` (SQLite)
- Model artifacts are in `ml/model_artifacts/` — re-run `python -m ml.train_model` to retrain
