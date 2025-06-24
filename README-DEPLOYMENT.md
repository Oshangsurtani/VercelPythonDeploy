# Sustainability Analytics Platform - Vercel Deployment

## Quick Deployment Steps

1. **Upload to GitHub**
   - Create new repository: `sustainability-analytics-platform`
   - Upload all project files

2. **Deploy to Vercel**
   - Connect GitHub repository to Vercel
   - Vercel will auto-detect Python application
   - Set environment variable: `SESSION_SECRET` (any random string)

3. **Configuration Files**
   - `vercel.json`: Serverless function configuration
   - `api/index.py`: Vercel entry point
   - `requirements-vercel.txt`: Production dependencies
   - `.vercelignore`: Deployment exclusions

## Features Included
- 4 ML Models: Packaging, Carbon Footprint, Product Recommendations, ESG Analysis
- Interactive Dashboard with Chart.js visualizations
- Batch CSV processing
- Bootstrap dark theme responsive design
- 60-second timeout for ML operations

## File Structure for Deployment
```
├── api/
│   └── index.py          # Vercel entry point
├── models/               # ML model implementations
├── routes/               # Flask blueprints
├── static/               # CSS, JS, assets
├── templates/            # HTML templates
├── utils/                # Data processing
├── app.py               # Main Flask application
├── vercel.json          # Vercel configuration
├── requirements-vercel.txt  # Production dependencies
└── .vercelignore        # Deployment exclusions
```

## Environment Variables Required
- `SESSION_SECRET`: Random string for Flask sessions

## Testing Endpoints
- `/health` - Health check
- `/` - Main dashboard
- `/api/models/status` - Model status
- `/api/predict/*` - ML predictions