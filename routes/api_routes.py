from flask import Blueprint, request, jsonify
from models.ml_models import MLModelManager
from utils.data_processor import DataProcessor
import pandas as pd
import io
import logging

api_bp = Blueprint('api', __name__)
ml_manager = MLModelManager()
data_processor = DataProcessor()

@api_bp.route('/predict/packaging', methods=['POST'])
def predict_packaging():
    """API endpoint for packaging predictions"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        prediction = ml_manager.predict_packaging(data)
        confidence = ml_manager.get_prediction_confidence('packaging', data)
        
        return jsonify({
            'prediction': prediction,
            'confidence': confidence,
            'model_status': 'active'
        })
        
    except Exception as e:
        logging.error(f"Packaging prediction API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/predict/carbon-footprint', methods=['POST'])
def predict_carbon_footprint():
    """API endpoint for carbon footprint predictions"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        prediction = ml_manager.predict_carbon_footprint(data)
        breakdown = ml_manager.get_carbon_breakdown(data)
        
        return jsonify({
            'prediction': prediction,
            'breakdown': breakdown,
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
        
        return jsonify({
            'results': results,
            'processed_count': len(results),
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
