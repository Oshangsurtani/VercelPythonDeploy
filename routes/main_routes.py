from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.ml_models import MLModelManager
from utils.data_processor import DataProcessor
import logging

main_bp = Blueprint('main', __name__)
ml_manager = MLModelManager()
data_processor = DataProcessor()

@main_bp.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    """Analytics dashboard"""
    # Get model status
    model_status = ml_manager.get_model_status()
    return render_template('dashboard.html', model_status=model_status)

@main_bp.route('/batch-processing')
def batch_processing():
    """Batch processing page"""
    return render_template('batch_processing.html')

@main_bp.route('/packaging-prediction')
def packaging_prediction():
    """Packaging prediction form"""
    if request.method == 'POST':
        try:
            # Get form data
            product_weight = float(request.form.get('product_weight', 0))
            fragility = request.form.get('fragility', 'low')
            material_type = request.form.get('material_type', 'plastic')
            transport_mode = request.form.get('transport_mode', 'ground')
            
            # Make prediction
            prediction = ml_manager.predict_packaging({
                'product_weight': product_weight,
                'fragility': fragility,
                'material_type': material_type,
                'transport_mode': transport_mode
            })
            
            flash(f'Recommended packaging: {prediction}', 'success')
            
        except Exception as e:
            logging.error(f"Packaging prediction error: {str(e)}")
            flash('Error making prediction. Please try again.', 'error')
    
    return render_template('index.html')

@main_bp.route('/carbon-footprint')
def carbon_footprint():
    """Carbon footprint calculation"""
    if request.method == 'POST':
        try:
            # Get form data
            age = int(request.form.get('age', 25))
            income = float(request.form.get('income', 50000))
            location = request.form.get('location', 'urban')
            transport_preference = request.form.get('transport_preference', 'car')
            
            # Make prediction
            prediction = ml_manager.predict_carbon_footprint({
                'age': age,
                'income': income,
                'location': location,
                'transport_preference': transport_preference
            })
            
            flash(f'Estimated carbon footprint: {prediction:.2f} tons CO2/year', 'success')
            
        except Exception as e:
            logging.error(f"Carbon footprint prediction error: {str(e)}")
            flash('Error calculating carbon footprint. Please try again.', 'error')
    
    return render_template('index.html')
