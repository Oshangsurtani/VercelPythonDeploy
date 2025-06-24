from flask import Blueprint, jsonify, render_template, request
from models.database import db, Prediction, BatchProcessing, ModelPerformance, UserSession, SystemStats
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import logging

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/analytics')
def analytics_dashboard():
    """Extended analytics dashboard with database insights"""
    try:
        # Get recent predictions
        recent_predictions = Prediction.query.order_by(desc(Prediction.created_at)).limit(10).all()
        
        # Get model usage statistics
        model_usage = db.session.query(
            Prediction.model_type,
            func.count(Prediction.id).label('count')
        ).group_by(Prediction.model_type).all()
        
        # Get batch processing stats
        batch_stats = db.session.query(
            func.count(BatchProcessing.id).label('total_batches'),
            func.sum(BatchProcessing.total_rows).label('total_rows'),
            func.avg(BatchProcessing.processing_time).label('avg_time')
        ).first()
        
        return render_template('analytics_dashboard.html', 
                             recent_predictions=recent_predictions,
                             model_usage=model_usage,
                             batch_stats=batch_stats)
    except Exception as e:
        logging.error(f"Analytics dashboard error: {str(e)}")
        return render_template('analytics_dashboard.html', 
                             recent_predictions=[],
                             model_usage=[],
                             batch_stats=None)

@dashboard_bp.route('/api/stats')
def get_dashboard_stats():
    """API endpoint for dashboard statistics"""
    try:
        # Total predictions by model
        predictions_by_model = db.session.query(
            Prediction.model_type,
            func.count(Prediction.id).label('count')
        ).group_by(Prediction.model_type).all()
        
        # Daily predictions for the last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        daily_predictions = db.session.query(
            func.date(Prediction.created_at).label('date'),
            func.count(Prediction.id).label('count')
        ).filter(Prediction.created_at >= seven_days_ago)\
         .group_by(func.date(Prediction.created_at))\
         .order_by(func.date(Prediction.created_at)).all()
        
        # Average processing times by model
        processing_times = db.session.query(
            Prediction.model_type,
            func.avg(Prediction.processing_time).label('avg_time')
        ).group_by(Prediction.model_type).all()
        
        # Recent batch jobs
        recent_batches = BatchProcessing.query.order_by(desc(BatchProcessing.created_at)).limit(5).all()
        
        # Model performance metrics
        model_performance = ModelPerformance.query.all()
        
        stats = {
            'predictions_by_model': [{'model': p.model_type, 'count': p.count} for p in predictions_by_model],
            'daily_predictions': [{'date': str(d.date), 'count': d.count} for d in daily_predictions],
            'processing_times': [{'model': p.model_type, 'avg_time': round(p.avg_time or 0, 3)} for p in processing_times],
            'recent_batches': [batch.to_dict() for batch in recent_batches],
            'model_performance': [perf.to_dict() for perf in model_performance],
            'total_predictions': sum(p.count for p in predictions_by_model),
            'total_batch_jobs': BatchProcessing.query.count(),
            'active_sessions': UserSession.query.filter(
                UserSession.last_activity >= datetime.utcnow() - timedelta(hours=1)
            ).count()
        }
        
        return jsonify(stats)
        
    except Exception as e:
        logging.error(f"Dashboard stats API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/api/predictions/recent')
def get_recent_predictions():
    """Get recent predictions with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        model_type = request.args.get('model_type')
        
        query = Prediction.query
        
        if model_type:
            query = query.filter(Prediction.model_type == model_type)
        
        predictions = query.order_by(desc(Prediction.created_at))\
                          .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'predictions': [pred.to_dict() for pred in predictions.items],
            'total': predictions.total,
            'page': predictions.page,
            'pages': predictions.pages,
            'per_page': predictions.per_page,
            'has_next': predictions.has_next,
            'has_prev': predictions.has_prev
        })
        
    except Exception as e:
        logging.error(f"Recent predictions API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/api/performance/trends')
def get_performance_trends():
    """Get model performance trends over time"""
    try:
        # Performance trends for the last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        # Average confidence scores by day
        confidence_trends = db.session.query(
            func.date(Prediction.created_at).label('date'),
            Prediction.model_type,
            func.avg(Prediction.confidence_score).label('avg_confidence')
        ).filter(Prediction.created_at >= thirty_days_ago)\
         .filter(Prediction.confidence_score.is_not(None))\
         .group_by(func.date(Prediction.created_at), Prediction.model_type)\
         .order_by(func.date(Prediction.created_at)).all()
        
        # Processing time trends
        processing_trends = db.session.query(
            func.date(Prediction.created_at).label('date'),
            Prediction.model_type,
            func.avg(Prediction.processing_time).label('avg_processing_time')
        ).filter(Prediction.created_at >= thirty_days_ago)\
         .group_by(func.date(Prediction.created_at), Prediction.model_type)\
         .order_by(func.date(Prediction.created_at)).all()
        
        trends = {
            'confidence_trends': [
                {
                    'date': str(t.date),
                    'model_type': t.model_type,
                    'avg_confidence': round(t.avg_confidence or 0, 3)
                }
                for t in confidence_trends
            ],
            'processing_trends': [
                {
                    'date': str(t.date),
                    'model_type': t.model_type,
                    'avg_processing_time': round(t.avg_processing_time or 0, 3)
                }
                for t in processing_trends
            ]
        }
        
        return jsonify(trends)
        
    except Exception as e:
        logging.error(f"Performance trends API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/api/export/predictions')
def export_predictions():
    """Export predictions data as JSON"""
    try:
        days = request.args.get('days', 7, type=int)
        model_type = request.args.get('model_type')
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        query = Prediction.query.filter(Prediction.created_at >= start_date)
        
        if model_type:
            query = query.filter(Prediction.model_type == model_type)
        
        predictions = query.order_by(desc(Prediction.created_at)).all()
        
        export_data = {
            'export_date': datetime.utcnow().isoformat(),
            'filters': {
                'days': days,
                'model_type': model_type
            },
            'total_records': len(predictions),
            'predictions': [pred.to_dict() for pred in predictions]
        }
        
        return jsonify(export_data)
        
    except Exception as e:
        logging.error(f"Export predictions error: {str(e)}")
        return jsonify({'error': str(e)}), 500