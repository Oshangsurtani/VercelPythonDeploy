# Sustainability Analytics Platform

## Overview

This is a comprehensive sustainability analytics web application built with Flask that integrates four machine learning models for environmental impact analysis. The platform provides both individual predictions and batch processing capabilities through a modern web interface with interactive dashboards.

## System Architecture

The application follows a modular Flask architecture optimized for both local development (Replit) and serverless deployment (Vercel):

- **Backend Framework**: Flask with Blueprint-based route organization
- **ML Framework**: scikit-learn with custom model managers
- **Frontend**: Bootstrap 5 (dark theme) with Chart.js for visualizations
- **Development Environment**: Replit with Nix package management
- **Production Deployment**: Vercel serverless functions
- **Data Processing**: pandas and numpy for batch operations

## Key Components

### Machine Learning Models (`models/ml_models.py`)
- **MLModelManager**: Central orchestrator for all ML operations
- **Packaging Suggestion Model**: RandomForestClassifier for optimal packaging recommendations
- **Carbon Footprint Prediction**: RandomForestRegressor for environmental impact calculation
- **Product Recommendation Engine**: Content-based filtering with sustainability scoring
- **ESG Score Analysis**: Sentiment analysis with environmental scoring

### Route Management (`routes/`)
- **main_routes.py**: Web interface routes (dashboard, forms, batch processing)
- **api_routes.py**: RESTful API endpoints for model predictions
- Blueprint architecture for modular route organization

### Data Processing (`utils/data_processor.py`)
- **DataProcessor**: Handles batch CSV processing
- Model-specific data validation and preprocessing
- Error handling and logging for production reliability

### Frontend Components
- **Templates**: Jinja2 templates with Bootstrap components
- **Static Assets**: Custom CSS, JavaScript, and Chart.js configurations
- **Interactive Dashboard**: Real-time model status and prediction visualizations

## Data Flow

1. **Input Processing**: User data via web forms or CSV uploads
2. **Model Selection**: Route to appropriate ML model based on prediction type
3. **Feature Engineering**: Data preprocessing and encoding
4. **Prediction Generation**: ML model inference with confidence scoring
5. **Result Presentation**: JSON API responses or rendered HTML templates
6. **Batch Processing**: CSV file processing with downloadable results

## External Dependencies

### Core Dependencies
- **Flask**: Web framework with SQLAlchemy extension
- **scikit-learn**: Machine learning models and preprocessing
- **pandas/numpy**: Data manipulation and numerical operations
- **matplotlib/seaborn**: Data visualization backend
- **joblib**: Model serialization and caching

### Frontend Dependencies (CDN)
- **Bootstrap 5**: UI framework with dark theme
- **Chart.js**: Interactive data visualizations
- **Font Awesome**: Icon library

### System Dependencies (Nix)
- **PostgreSQL**: Database system (configured but not actively used)
- **cairo/freetype**: Graphics rendering for matplotlib
- **gunicorn**: WSGI server for production deployment

## Deployment Strategy

### Development (Replit)
- **Environment**: Python 3.11 with Nix package management
- **Server**: Gunicorn with hot reloading
- **Port Configuration**: 5000 with automatic port forwarding
- **Workflow**: Parallel startup for application and dependency installation

### Production (Vercel)
- **Runtime**: Serverless Python functions
- **Handler**: WSGI compatibility layer for Flask
- **Timeout**: 60 seconds for ML model operations
- **Environment**: SESSION_SECRET for Flask session management
- **Build**: Automatic deployment from GitHub integration

### Configuration Files
- **vercel.json**: Serverless function configuration
- **.replit**: Development environment specification
- **pyproject.toml**: Python project metadata and dependencies

## Changelog

- June 24, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.