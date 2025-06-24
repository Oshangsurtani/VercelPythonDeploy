from flask import Blueprint, request, jsonify
from models.ml_models import MLModelManager
from models.database import db, Prediction, BatchProcessing, ModelPerformance, UserSession
from utils.data_processor import DataProcessor
import pandas as pd
import io
import logging
import time
from datetime import datetime

api_bp = Blueprint('api', __name__)
ml_manager = MLModelManager()
data_processor = DataProcessor()

@api_bp.route('/predict/packaging', methods=['POST'])
def predict_packaging():
    """API endpoint for packaging predictions"""
    start_time = time.time()
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        prediction = ml_manager.predict_packaging(data)
        confidence = ml_manager.get_prediction_confidence('packaging', data)
        processing_time = time.time() - start_time
        
        # Store prediction in database
        try:
            prediction_record = Prediction(
                model_type='packaging',
                input_data=data,
                prediction_result={'prediction': prediction},
                confidence_score=confidence,
                processing_time=processing_time,
                ip_address=request.remote_addr
            )
            db.session.add(prediction_record)
            db.session.commit()
        except Exception as db_error:
            logging.error(f"Database error storing packaging prediction: {str(db_error)}")
            # Continue without failing the prediction
        
        return jsonify({
            'prediction': prediction,
            'confidence': confidence,
            'processing_time': round(processing_time, 3),
            'model_status': 'active'
        })
        
    except Exception as e:
        logging.error(f"Packaging prediction API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/predict/carbon-footprint', methods=['POST'])
def predict_carbon_footprint():
    """API endpoint for carbon footprint predictions"""
    start_time = time.time()
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        prediction = ml_manager.predict_carbon_footprint(data)
        breakdown = ml_manager.get_carbon_breakdown(data)
        processing_time = time.time() - start_time
        
        # Store prediction in database
        try:
            prediction_record = Prediction(
                model_type='carbon_footprint',
                input_data=data,
                prediction_result={'prediction': prediction, 'breakdown': breakdown},
                processing_time=processing_time,
                ip_address=request.remote_addr
            )
            db.session.add(prediction_record)
            db.session.commit()
        except Exception as db_error:
            logging.error(f"Database error storing carbon footprint prediction: {str(db_error)}")
        
        return jsonify({
            'prediction': prediction,
            'breakdown': breakdown,
            'processing_time': round(processing_time, 3),
            'unit': 'tons CO2/year',
            'model_status': 'active'
        })
        
    except Exception as e:
        logging.error(f"Carbon footprint prediction API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/predict/product-recommendation', methods=['POST'])
def predict_product_recommendation():
    """API endpoint for product recommendations"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        recommendations = ml_manager.predict_product_recommendations(data)
        
        return jsonify({
            'recommendations': recommendations,
            'model_status': 'active'
        })
        
    except Exception as e:
        logging.error(f"Product recommendation API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/predict/esg-score', methods=['POST'])
def predict_esg_score():
    """API endpoint for ESG score analysis"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        esg_scores = ml_manager.predict_esg_score(data)
        
        return jsonify({
            'esg_scores': esg_scores,
            'model_status': 'active'
        })
        
    except Exception as e:
        logging.error(f"ESG score prediction API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/batch-process', methods=['POST'])
def batch_process():
    """API endpoint for batch processing CSV files"""
    start_time = time.time()
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'File must be CSV format'}), 400
        
        # Read CSV file
        csv_data = file.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(csv_data))
        
        # Process batch data
        model_type = request.form.get('model_type', 'packaging')
        results = data_processor.process_batch(df, model_type)
        processing_time = time.time() - start_time
        
        # Calculate statistics
        successful_rows = len([r for r in results if 'error' not in r])
        failed_rows = len([r for r in results if 'error' in r])
        
        # Store batch processing record
        try:
            batch_record = BatchProcessing(
                filename=file.filename,
                model_type=model_type,
                total_rows=len(results),
                successful_rows=successful_rows,
                failed_rows=failed_rows,
                processing_time=processing_time,
                results_summary={
                    'success_rate': round((successful_rows / len(results)) * 100, 2) if results else 0,
                    'avg_processing_time_per_row': round(processing_time / len(results), 4) if results else 0
                },
                ip_address=request.remote_addr
            )
            db.session.add(batch_record)
            db.session.commit()
        except Exception as db_error:
            logging.error(f"Database error storing batch processing: {str(db_error)}")
        
        return jsonify({
            'results': results,
            'processed_count': len(results),
            'successful_count': successful_rows,
            'failed_count': failed_rows,
            'success_rate': round((successful_rows / len(results)) * 100, 2) if results else 0,
            'processing_time': round(processing_time, 3),
            'model_type': model_type
        })
        
    except Exception as e:
        logging.error(f"Batch processing API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/models/status', methods=['GET'])
def get_models_status():
    """API endpoint to get model training status"""
    try:
        status = ml_manager.get_model_status()
        return jsonify(status)
        
    except Exception as e:
        logging.error(f"Model status API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/models/train', methods=['POST'])
def train_models():
    """API endpoint to trigger model training"""
    try:
        model_type = request.get_json().get('model_type', 'all')
        
        if model_type == 'all':
            ml_manager.train_all_models()
        else:
            ml_manager.train_model(model_type)
        
        return jsonify({
            'message': f'Training initiated for {model_type} model(s)',
            'status': 'training'
        })
        
    except Exception as e:
        logging.error(f"Model training API error: {str(e)}")
        return jsonify({'error': str(e)}), 500
