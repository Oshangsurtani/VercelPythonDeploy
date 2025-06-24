import pandas as pd
import numpy as np
from models.ml_models import MLModelManager
import logging

class DataProcessor:
    def __init__(self):
        self.ml_manager = MLModelManager()
    
    def process_batch(self, df, model_type):
        """Process batch data for predictions"""
        try:
            results = []
            
            if model_type == 'packaging':
                results = self._process_packaging_batch(df)
            elif model_type == 'carbon_footprint':
                results = self._process_carbon_batch(df)
            elif model_type == 'product_recommendation':
                results = self._process_product_batch(df)
            elif model_type == 'esg_score':
                results = self._process_esg_batch(df)
            else:
                raise ValueError(f"Unknown model type: {model_type}")
            
            return results
            
        except Exception as e:
            logging.error(f"Batch processing error: {str(e)}")
            return []
    
    def _process_packaging_batch(self, df):
        """Process packaging batch data"""
        results = []
        required_columns = ['product_weight', 'fragility', 'material_type', 'transport_mode']
        
        # Check if required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")
        
        for index, row in df.iterrows():
            try:
                data = {
                    'product_weight': float(row['product_weight']),
                    'fragility': str(row['fragility']),
                    'material_type': str(row['material_type']),
                    'transport_mode': str(row['transport_mode'])
                }
                
                prediction = self.ml_manager.predict_packaging(data)
                confidence = self.ml_manager.get_prediction_confidence('packaging', data)
                
                results.append({
                    'row_index': index,
                    'prediction': prediction,
                    'confidence': confidence,
                    'input_data': data
                })
                
            except Exception as e:
                logging.error(f"Error processing row {index}: {str(e)}")
                results.append({
                    'row_index': index,
                    'error': str(e),
                    'input_data': row.to_dict()
                })
        
        return results
    
    def _process_carbon_batch(self, df):
        """Process carbon footprint batch data"""
        results = []
        required_columns = ['age', 'income', 'location', 'transport_preference']
        
        # Check if required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")
        
        for index, row in df.iterrows():
            try:
                data = {
                    'age': int(row['age']),
                    'income': float(row['income']),
                    'location': str(row['location']),
                    'transport_preference': str(row['transport_preference'])
                }
                
                prediction = self.ml_manager.predict_carbon_footprint(data)
                breakdown = self.ml_manager.get_carbon_breakdown(data)
                
                results.append({
                    'row_index': index,
                    'prediction': prediction,
                    'breakdown': breakdown,
                    'unit': 'tons CO2/year',
                    'input_data': data
                })
                
            except Exception as e:
                logging.error(f"Error processing row {index}: {str(e)}")
                results.append({
                    'row_index': index,
                    'error': str(e),
                    'input_data': row.to_dict()
                })
        
        return results
    
    def _process_product_batch(self, df):
        """Process product recommendation batch data"""
        results = []
        required_columns = ['category', 'budget']
        
        # Check if required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")
        
        for index, row in df.iterrows():
            try:
                data = {
                    'category': str(row['category']),
                    'budget': float(row['budget']),
                    'eco_priority': row.get('eco_priority', True)
                }
                
                recommendations = self.ml_manager.predict_product_recommendations(data)
                
                results.append({
                    'row_index': index,
                    'recommendations': recommendations,
                    'count': len(recommendations),
                    'input_data': data
                })
                
            except Exception as e:
                logging.error(f"Error processing row {index}: {str(e)}")
                results.append({
                    'row_index': index,
                    'error': str(e),
                    'input_data': row.to_dict()
                })
        
        return results
    
    def _process_esg_batch(self, df):
        """Process ESG score batch data"""
        results = []
        required_columns = ['carbon_emissions', 'renewable_energy', 'waste_management']
        
        # Check if required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")
        
        for index, row in df.iterrows():
            try:
                data = {
                    'carbon_emissions': float(row['carbon_emissions']),
                    'renewable_energy': float(row['renewable_energy']),
                    'waste_management': float(row['waste_management']),
                    'employee_satisfaction': float(row.get('employee_satisfaction', 7)),
                    'diversity_score': float(row.get('diversity_score', 6)),
                    'community_impact': float(row.get('community_impact', 6)),
                    'board_independence': float(row.get('board_independence', 60)),
                    'transparency_score': float(row.get('transparency_score', 7)),
                    'ethics_score': float(row.get('ethics_score', 7))
                }
                
                esg_scores = self.ml_manager.predict_esg_score(data)
                
                results.append({
                    'row_index': index,
                    'esg_scores': esg_scores,
                    'input_data': data
                })
                
            except Exception as e:
                logging.error(f"Error processing row {index}: {str(e)}")
                results.append({
                    'row_index': index,
                    'error': str(e),
                    'input_data': row.to_dict()
                })
        
        return results
    
    def validate_csv_format(self, df, model_type):
        """Validate CSV format for specific model type"""
        required_columns = {
            'packaging': ['product_weight', 'fragility', 'material_type', 'transport_mode'],
            'carbon_footprint': ['age', 'income', 'location', 'transport_preference'],
            'product_recommendation': ['category', 'budget'],
            'esg_score': ['carbon_emissions', 'renewable_energy', 'waste_management']
        }
        
        if model_type not in required_columns:
            return False, f"Unknown model type: {model_type}"
        
        missing_columns = [col for col in required_columns[model_type] if col not in df.columns]
        if missing_columns:
            return False, f"Missing required columns: {missing_columns}"
        
        return True, "Valid format"
    
    def get_sample_csv_format(self, model_type):
        """Get sample CSV format for specific model type"""
        sample_data = {
            'packaging': {
                'product_weight': [1.5, 10.0, 0.5],
                'fragility': ['low', 'high', 'medium'],
                'material_type': ['plastic', 'glass', 'metal'],
                'transport_mode': ['ground', 'air', 'sea']
            },
            'carbon_footprint': {
                'age': [25, 45, 35],
                'income': [50000, 80000, 60000],
                'location': ['urban', 'suburban', 'rural'],
                'transport_preference': ['car', 'public_transport', 'bike']
            },
            'product_recommendation': {
                'category': ['electronics', 'clothing', 'home'],
                'budget': [500, 200, 1000],
                'eco_priority': [True, False, True]
            },
            'esg_score': {
                'carbon_emissions': [5000, 3000, 8000],
                'renewable_energy': [30, 60, 20],
                'waste_management': [5, 8, 3],
                'employee_satisfaction': [7, 8, 6],
                'diversity_score': [6, 9, 5],
                'community_impact': [6, 7, 4]
            }
        }
        
        if model_type in sample_data:
            return pd.DataFrame(sample_data[model_type])
        else:
            return pd.DataFrame()
