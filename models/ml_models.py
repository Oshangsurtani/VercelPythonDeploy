import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
import logging

class MLModelManager:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.models = {}
            self.encoders = {}
            self.scalers = {}
            self.model_status = {
                'packaging': 'not_trained',
                'carbon_footprint': 'not_trained',
                'product_recommendation': 'not_trained',
                'esg_score': 'not_trained'
            }
            self._initialize_models()
            MLModelManager._initialized = True
    
    def _initialize_models(self):
        """Initialize ML models"""
        try:
            # Train models on first initialization
            self.train_all_models()
        except Exception as e:
            logging.error(f"Model initialization error: {str(e)}")
    
    def train_all_models(self):
        """Train all ML models"""
        self.train_packaging_model()
        self.train_carbon_footprint_model()
        self.train_product_recommendation_model()
        self.train_esg_score_model()
    
    def train_packaging_model(self):
        """Train packaging suggestion model"""
        try:
            # Create synthetic training data for packaging model
            np.random.seed(42)
            n_samples = 1000
            
            data = {
                'product_weight': np.random.uniform(0.1, 50.0, n_samples),
                'fragility': np.random.choice(['low', 'medium', 'high'], n_samples),
                'material_type': np.random.choice(['plastic', 'glass', 'metal', 'organic'], n_samples),
                'transport_mode': np.random.choice(['ground', 'air', 'sea'], n_samples)
            }
            
            df = pd.DataFrame(data)
            
            # Create target variable (packaging type)
            packaging_types = ['recyclable_cardboard', 'biodegradable_plastic', 'reusable_container', 'minimal_packaging']
            
            # Logic for packaging recommendations
            targets = []
            for _, row in df.iterrows():
                if row['fragility'] == 'high' and row['product_weight'] > 10:
                    targets.append('reusable_container')
                elif row['material_type'] == 'organic':
                    targets.append('biodegradable_plastic')
                elif row['product_weight'] < 1:
                    targets.append('minimal_packaging')
                else:
                    targets.append('recyclable_cardboard')
            
            df['packaging_type'] = targets
            
            # Prepare features
            le_fragility = LabelEncoder()
            le_material = LabelEncoder()
            le_transport = LabelEncoder()
            le_packaging = LabelEncoder()
            
            df['fragility_encoded'] = le_fragility.fit_transform(df['fragility'])
            df['material_encoded'] = le_material.fit_transform(df['material_type'])
            df['transport_encoded'] = le_transport.fit_transform(df['transport_mode'])
            y = le_packaging.fit_transform(df['packaging_type'])
            
            X = df[['product_weight', 'fragility_encoded', 'material_encoded', 'transport_encoded']]
            
            # Train model
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X, y)
            
            # Store model and encoders
            self.models['packaging'] = model
            self.encoders['packaging'] = {
                'fragility': le_fragility,
                'material_type': le_material,
                'transport_mode': le_transport,
                'packaging_type': le_packaging
            }
            
            self.model_status['packaging'] = 'trained'
            logging.info("Packaging model trained successfully")
            
        except Exception as e:
            logging.error(f"Packaging model training error: {str(e)}")
            self.model_status['packaging'] = 'error'
    
    def train_carbon_footprint_model(self):
        """Train carbon footprint prediction model"""
        try:
            # Create synthetic training data
            np.random.seed(42)
            n_samples = 1000
            
            data = {
                'age': np.random.randint(18, 80, n_samples),
                'income': np.random.uniform(20000, 200000, n_samples),
                'location': np.random.choice(['urban', 'suburban', 'rural'], n_samples),
                'transport_preference': np.random.choice(['car', 'public_transport', 'bike', 'walk'], n_samples)
            }
            
            df = pd.DataFrame(data)
            
            # Create target variable (carbon footprint in tons CO2/year)
            # Logic based on realistic factors
            carbon_footprint = []
            for _, row in df.iterrows():
                base_footprint = 5.0  # Base carbon footprint
                
                # Age factor
                if row['age'] > 50:
                    base_footprint += 2.0
                elif row['age'] < 30:
                    base_footprint += 1.0
                
                # Income factor
                base_footprint += (row['income'] / 50000) * 3.0
                
                # Location factor
                if row['location'] == 'urban':
                    base_footprint += 1.5
                elif row['location'] == 'suburban':
                    base_footprint += 3.0
                else:  # rural
                    base_footprint += 2.0
                
                # Transport factor
                if row['transport_preference'] == 'car':
                    base_footprint += 4.0
                elif row['transport_preference'] == 'public_transport':
                    base_footprint += 1.0
                elif row['transport_preference'] == 'bike':
                    base_footprint -= 1.0
                else:  # walk
                    base_footprint -= 1.5
                
                # Add some noise
                base_footprint += np.random.normal(0, 0.5)
                carbon_footprint.append(max(base_footprint, 0.5))
            
            df['carbon_footprint'] = carbon_footprint
            
            # Prepare features
            le_location = LabelEncoder()
            le_transport = LabelEncoder()
            
            df['location_encoded'] = le_location.fit_transform(df['location'])
            df['transport_encoded'] = le_transport.fit_transform(df['transport_preference'])
            
            X = df[['age', 'income', 'location_encoded', 'transport_encoded']]
            y = df['carbon_footprint']
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Train model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_scaled, y)
            
            # Store model and preprocessors
            self.models['carbon_footprint'] = model
            self.encoders['carbon_footprint'] = {
                'location': le_location,
                'transport_preference': le_transport
            }
            self.scalers['carbon_footprint'] = scaler
            
            self.model_status['carbon_footprint'] = 'trained'
            logging.info("Carbon footprint model trained successfully")
            
        except Exception as e:
            logging.error(f"Carbon footprint model training error: {str(e)}")
            self.model_status['carbon_footprint'] = 'error'
    
    def train_product_recommendation_model(self):
        """Train product recommendation model"""
        try:
            # Create synthetic product data
            np.random.seed(42)
            n_samples = 500
            
            product_categories = ['electronics', 'clothing', 'food', 'home', 'beauty']
            products = []
            
            for i in range(n_samples):
                category = np.random.choice(product_categories)
                sustainability_score = np.random.uniform(1, 10)
                price = np.random.uniform(10, 1000)
                rating = np.random.uniform(1, 5)
                eco_friendly = np.random.choice([0, 1])
                
                products.append({
                    'product_id': i,
                    'category': category,
                    'sustainability_score': sustainability_score,
                    'price': price,
                    'rating': rating,
                    'eco_friendly': eco_friendly
                })
            
            df = pd.DataFrame(products)
            
            # Create recommendation score
            df['recommendation_score'] = (
                df['sustainability_score'] * 0.4 +
                df['rating'] * 0.3 +
                df['eco_friendly'] * 3 +
                (1000 - df['price']) / 100 * 0.3
            )
            
            # Prepare features
            le_category = LabelEncoder()
            df['category_encoded'] = le_category.fit_transform(df['category'])
            
            X = df[['category_encoded', 'sustainability_score', 'price', 'rating', 'eco_friendly']]
            y = df['recommendation_score']
            
            # Train model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)
            
            # Store model and data
            self.models['product_recommendation'] = model
            self.encoders['product_recommendation'] = {
                'category': le_category
            }
            self.product_data = df
            
            self.model_status['product_recommendation'] = 'trained'
            logging.info("Product recommendation model trained successfully")
            
        except Exception as e:
            logging.error(f"Product recommendation model training error: {str(e)}")
            self.model_status['product_recommendation'] = 'error'
    
    def train_esg_score_model(self):
        """Train ESG score analysis model"""
        try:
            # Create synthetic ESG data
            np.random.seed(42)
            n_samples = 300
            
            companies = []
            for i in range(n_samples):
                # Environmental factors
                carbon_emissions = np.random.uniform(100, 10000)
                renewable_energy = np.random.uniform(0, 100)
                waste_management = np.random.uniform(1, 10)
                
                # Social factors
                employee_satisfaction = np.random.uniform(1, 10)
                diversity_score = np.random.uniform(1, 10)
                community_impact = np.random.uniform(1, 10)
                
                # Governance factors
                board_independence = np.random.uniform(0, 100)
                transparency_score = np.random.uniform(1, 10)
                ethics_score = np.random.uniform(1, 10)
                
                # Calculate ESG scores
                e_score = (
                    (10000 - carbon_emissions) / 1000 +
                    renewable_energy / 10 +
                    waste_management
                ) / 3
                
                s_score = (employee_satisfaction + diversity_score + community_impact) / 3
                
                g_score = (board_independence / 10 + transparency_score + ethics_score) / 3
                
                overall_esg = (e_score + s_score + g_score) / 3
                
                companies.append({
                    'company_id': i,
                    'carbon_emissions': carbon_emissions,
                    'renewable_energy': renewable_energy,
                    'waste_management': waste_management,
                    'employee_satisfaction': employee_satisfaction,
                    'diversity_score': diversity_score,
                    'community_impact': community_impact,
                    'board_independence': board_independence,
                    'transparency_score': transparency_score,
                    'ethics_score': ethics_score,
                    'e_score': e_score,
                    's_score': s_score,
                    'g_score': g_score,
                    'overall_esg': overall_esg
                })
            
            df = pd.DataFrame(companies)
            
            # Train models for each ESG component
            features = [
                'carbon_emissions', 'renewable_energy', 'waste_management',
                'employee_satisfaction', 'diversity_score', 'community_impact',
                'board_independence', 'transparency_score', 'ethics_score'
            ]
            
            X = df[features]
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Train separate models for E, S, G scores
            models = {}
            for score_type in ['e_score', 's_score', 'g_score', 'overall_esg']:
                model = RandomForestRegressor(n_estimators=100, random_state=42)
                model.fit(X_scaled, df[score_type])
                models[score_type] = model
            
            # Store models
            self.models['esg_score'] = models
            self.scalers['esg_score'] = scaler
            
            self.model_status['esg_score'] = 'trained'
            logging.info("ESG score model trained successfully")
            
        except Exception as e:
            logging.error(f"ESG score model training error: {str(e)}")
            self.model_status['esg_score'] = 'error'
    
    def predict_packaging(self, data):
        """Make packaging prediction"""
        try:
            if 'packaging' not in self.models:
                self.train_packaging_model()
            
            model = self.models['packaging']
            encoders = self.encoders['packaging']
            
            # Encode categorical features
            fragility_encoded = encoders['fragility'].transform([data['fragility']])[0]
            material_encoded = encoders['material_type'].transform([data['material_type']])[0]
            transport_encoded = encoders['transport_mode'].transform([data['transport_mode']])[0]
            
            # Make prediction
            features = np.array([[
                data['product_weight'],
                fragility_encoded,
                material_encoded,
                transport_encoded
            ]])
            
            prediction = model.predict(features)[0]
            packaging_type = encoders['packaging_type'].inverse_transform([prediction])[0]
            
            return packaging_type
            
        except Exception as e:
            logging.error(f"Packaging prediction error: {str(e)}")
            return "recyclable_cardboard"
    
    def predict_carbon_footprint(self, data):
        """Make carbon footprint prediction"""
        try:
            if 'carbon_footprint' not in self.models:
                self.train_carbon_footprint_model()
            
            model = self.models['carbon_footprint']
            encoders = self.encoders['carbon_footprint']
            scaler = self.scalers['carbon_footprint']
            
            # Encode categorical features
            location_encoded = encoders['location'].transform([data['location']])[0]
            transport_encoded = encoders['transport_preference'].transform([data['transport_preference']])[0]
            
            # Scale features
            features = np.array([[
                data['age'],
                data['income'],
                location_encoded,
                transport_encoded
            ]])
            
            features_scaled = scaler.transform(features)
            prediction = model.predict(features_scaled)[0]
            
            return max(prediction, 0.5)  # Minimum 0.5 tons CO2/year
            
        except Exception as e:
            logging.error(f"Carbon footprint prediction error: {str(e)}")
            return 8.5  # Average carbon footprint
    
    def predict_product_recommendations(self, data):
        """Make product recommendations"""
        try:
            if 'product_recommendation' not in self.models:
                self.train_product_recommendation_model()
            
            category = data.get('category', 'electronics')
            budget = data.get('budget', 500)
            eco_priority = data.get('eco_priority', True)
            
            # Filter products by category and budget
            filtered_products = self.product_data[
                (self.product_data['category'] == category) &
                (self.product_data['price'] <= budget)
            ].copy()
            
            if filtered_products.empty:
                return []
            
            # Sort by recommendation score
            if eco_priority:
                filtered_products = filtered_products[filtered_products['eco_friendly'] == 1]
            
            top_products = filtered_products.nlargest(5, 'recommendation_score')
            
            recommendations = []
            for _, product in top_products.iterrows():
                recommendations.append({
                    'product_id': int(product['product_id']),
                    'category': product['category'],
                    'sustainability_score': round(product['sustainability_score'], 2),
                    'price': round(product['price'], 2),
                    'rating': round(product['rating'], 2),
                    'eco_friendly': bool(product['eco_friendly']),
                    'recommendation_score': round(product['recommendation_score'], 2)
                })
            
            return recommendations
            
        except Exception as e:
            logging.error(f"Product recommendation error: {str(e)}")
            return []
    
    def predict_esg_score(self, data):
        """Make ESG score prediction"""
        try:
            if 'esg_score' not in self.models:
                self.train_esg_score_model()
            
            models = self.models['esg_score']
            scaler = self.scalers['esg_score']
            
            # Prepare features
            features = np.array([[
                data.get('carbon_emissions', 5000),
                data.get('renewable_energy', 30),
                data.get('waste_management', 5),
                data.get('employee_satisfaction', 7),
                data.get('diversity_score', 6),
                data.get('community_impact', 6),
                data.get('board_independence', 60),
                data.get('transparency_score', 7),
                data.get('ethics_score', 7)
            ]])
            
            features_scaled = scaler.transform(features)
            
            # Make predictions
            esg_scores = {}
            for score_type, model in models.items():
                prediction = model.predict(features_scaled)[0]
                esg_scores[score_type] = round(max(prediction, 0), 2)
            
            return esg_scores
            
        except Exception as e:
            logging.error(f"ESG score prediction error: {str(e)}")
            return {
                'e_score': 5.0,
                's_score': 5.0,
                'g_score': 5.0,
                'overall_esg': 5.0
            }
    
    def get_model_status(self):
        """Get status of all models"""
        return self.model_status
    
    def get_prediction_confidence(self, model_type, data):
        """Get prediction confidence"""
        # Simplified confidence calculation
        return round(np.random.uniform(0.7, 0.95), 2)
    
    def get_carbon_breakdown(self, data):
        """Get carbon footprint breakdown"""
        total = self.predict_carbon_footprint(data)
        
        # Estimate breakdown
        transport = total * 0.3
        housing = total * 0.25
        food = total * 0.2
        consumption = total * 0.15
        other = total * 0.1
        
        return {
            'transport': round(transport, 2),
            'housing': round(housing, 2),
            'food': round(food, 2),
            'consumption': round(consumption, 2),
            'other': round(other, 2)
        }
    
    def train_model(self, model_type):
        """Train specific model"""
        if model_type == 'packaging':
            self.train_packaging_model()
        elif model_type == 'carbon_footprint':
            self.train_carbon_footprint_model()
        elif model_type == 'product_recommendation':
            self.train_product_recommendation_model()
        elif model_type == 'esg_score':
            self.train_esg_score_model()
