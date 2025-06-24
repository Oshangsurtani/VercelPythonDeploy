import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    model_type = db.Column(db.String(50), nullable=False)
    input_data = db.Column(JSON, nullable=False)
    prediction_result = db.Column(JSON, nullable=False)
    confidence_score = db.Column(db.Float)
    processing_time = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    
    def to_dict(self):
        return {
            'id': self.id,
            'model_type': self.model_type,
            'input_data': self.input_data,
            'prediction_result': self.prediction_result,
            'confidence_score': self.confidence_score,
            'processing_time': self.processing_time,
            'created_at': self.created_at.isoformat(),
            'ip_address': self.ip_address
        }

class BatchProcessing(db.Model):
    __tablename__ = 'batch_processing'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    model_type = db.Column(db.String(50), nullable=False)
    total_rows = db.Column(db.Integer, nullable=False)
    successful_rows = db.Column(db.Integer, nullable=False)
    failed_rows = db.Column(db.Integer, nullable=False)
    processing_time = db.Column(db.Float, nullable=False)
    results_summary = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'model_type': self.model_type,
            'total_rows': self.total_rows,
            'successful_rows': self.successful_rows,
            'failed_rows': self.failed_rows,
            'success_rate': round((self.successful_rows / self.total_rows) * 100, 2) if self.total_rows > 0 else 0,
            'processing_time': self.processing_time,
            'results_summary': self.results_summary,
            'created_at': self.created_at.isoformat()
        }

class ModelPerformance(db.Model):
    __tablename__ = 'model_performance'
    
    id = db.Column(db.Integer, primary_key=True)
    model_type = db.Column(db.String(50), nullable=False)
    accuracy_score = db.Column(db.Float)
    training_time = db.Column(db.Float)
    last_trained = db.Column(db.DateTime, default=datetime.utcnow)
    version = db.Column(db.String(50), default='1.0.0')
    status = db.Column(db.String(20), default='trained')
    metrics = db.Column(JSON)
    
    def to_dict(self):
        return {
            'id': self.id,
            'model_type': self.model_type,
            'accuracy_score': self.accuracy_score,
            'training_time': self.training_time,
            'last_trained': self.last_trained.isoformat(),
            'version': self.version,
            'status': self.status,
            'metrics': self.metrics
        }

class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True, nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    predictions_count = db.Column(db.Integer, default=0)
    batch_uploads_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'predictions_count': self.predictions_count,
            'batch_uploads_count': self.batch_uploads_count,
            'created_at': self.created_at.isoformat(),
            'last_activity': self.last_activity.isoformat()
        }

class SystemStats(db.Model):
    __tablename__ = 'system_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    total_predictions = db.Column(db.Integer, default=0)
    total_batch_jobs = db.Column(db.Integer, default=0)
    total_users = db.Column(db.Integer, default=0)
    avg_processing_time = db.Column(db.Float, default=0.0)
    most_used_model = db.Column(db.String(50))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'total_predictions': self.total_predictions,
            'total_batch_jobs': self.total_batch_jobs,
            'total_users': self.total_users,
            'avg_processing_time': self.avg_processing_time,
            'most_used_model': self.most_used_model,
            'updated_at': self.updated_at.isoformat()
        }