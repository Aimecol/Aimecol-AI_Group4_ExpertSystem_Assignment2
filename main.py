from app_factory import create_app
# from models import db, Crop
from flask import render_template, request, jsonify
from datetime import datetime
import json
import logging
from crop_database_setup import init_db as setup_db
# from sqlalchemy import and_
import sqlite3
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_application():
    """Create and initialize the application"""
    # Initialize the database first
    if not setup_db():
        logger.error("Failed to initialize SQLite database")
        return None
        
    # Create Flask app without creating tables
    app = create_app()
    
    return app

# Create the application
app = create_application()

if not app:
    raise RuntimeError("Failed to initialize application")

def validate_input(data):
    """Validate input parameters."""
    errors = []
    try:
        if not (0 <= float(data['temperature']) <= 50):
            errors.append("Temperature must be between 0°C and 50°C")
        if not (0 <= float(data['rainfall']) <= 5000):
            errors.append("Rainfall must be between 0mm and 5000mm")
        if not (0 <= float(data['humidity']) <= 100):
            errors.append("Humidity must be between 0% and 100%")
        if not (0 <= float(data['ph']) <= 14):
            errors.append("pH must be between 0 and 14")
    except ValueError:
        errors.append("All values must be numbers")
    
    if data['soil_type'] not in ['clay', 'loam', 'sandy']:
        errors.append("Invalid soil type")
    
    return errors

def get_current_season():
    """Determine current growing season based on month."""
    month = datetime.now().month
    if 6 <= month <= 10:
        return "Monsoon season"
    elif month <= 3 or month >= 11:
        return "Winter season"
    else:
        return "Summer season"

def calculate_crop_score(crop_info, conditions):
    """Calculate compatibility score for a crop under given conditions."""
    score = 0
    
    # Temperature compatibility
    temp = float(conditions['temperature'])
    if crop_info['temp_range'][0] <= temp <= crop_info['temp_range'][1]:
        score += 30
    
    # Rainfall compatibility
    rainfall = float(conditions['rainfall'])
    if crop_info['rainfall_range'][0] <= rainfall <= crop_info['rainfall_range'][1]:
        score += 25
    
    # Soil type compatibility
    if conditions['soil_type'] in crop_info['soil_types']:
        score += 20
    
    # pH compatibility
    ph = float(conditions['ph'])
    if crop_info['ph_range'][0] <= ph <= crop_info['ph_range'][1]:
        score += 15
    
    # Season compatibility
    if get_current_season() in crop_info['seasons']:
        score += 10
    
    return score

def recommend_crop(conditions):
    """Enhanced crop recommendation system with direct database filtering"""
    crop_scores = {}
    
    try:
        temp = float(conditions['temperature'])
        rainfall = float(conditions['rainfall'])
        soil_type = conditions['soil_type'].lower()
        
        # Connect to database using absolute path
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'crops.db'))
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Modified query to ensure we get all necessary fields
        cursor.execute('''
            SELECT 
                name, temp_min, temp_max, rain_min, rain_max,
                ph_min, ph_max, humidity_min, humidity_max,
                soil_types, seasons, nutrients,
                'Detailed information about ' || name as description,
                'Standard farming practices for ' || name as farming_practices,
                CASE 
                    WHEN rain_min > 1000 THEN 'High'
                    WHEN rain_min > 500 THEN 'Medium'
                    ELSE 'Low'
                END as water_needs,
                'Full Sun' as sunlight_needs
            FROM crops
            WHERE (? BETWEEN temp_min AND temp_max)
            AND (? BETWEEN rain_min AND rain_max)
            AND soil_types LIKE ?
        ''', (temp, rainfall, f"%{soil_type}%"))
        
        crops_data = cursor.fetchall()
        logger.info(f"Found {len(crops_data)} matching crops")
        
        current_season = get_current_season()
        
        for crop in crops_data:
            try:
                (name, t_min, t_max, r_min, r_max, p_min, p_max, 
                 h_min, h_max, soils, seasons, nutrients, desc, 
                 practices, water, sun) = crop
                
                crop_info = {
                    'temp_range': (float(t_min), float(t_max)),
                    'rainfall_range': (float(r_min), float(r_max)),
                    'ph_range': (float(p_min), float(p_max)),
                    'humidity_range': (float(h_min), float(h_max)),
                    'soil_types': [s.strip() for s in soils.split(',')],
                    'seasons': [s.strip() for s in seasons.split(',')],
                    'nutrients': json.loads(nutrients)
                }
                
                score = calculate_crop_score(crop_info, conditions)
                logger.info(f"Crop: {name}, Score: {score}")
                
                if score >= 60:  # Only recommend crops with good compatibility
                    crop_scores[name] = {
                        'score': score,
                        'details': {
                            'optimal_temp': f"{t_min}-{t_max}°C",
                            'optimal_rainfall': f"{r_min}-{r_max}mm",
                            'suitable_soil': soils,
                            'growing_season': seasons,
                            'nutrients_needed': crop_info['nutrients'],
                            'description': desc,
                            'farming_practices': practices,
                            'water_needs': water,
                            'sunlight_needs': sun
                        }
                    }
            except Exception as e:
                logger.error(f"Error processing crop {name}: {str(e)}")
                continue
        
        conn.close()
        sorted_scores = dict(sorted(crop_scores.items(), key=lambda x: x[1]['score'], reverse=True))
        logger.info(f"Returning {len(sorted_scores)} recommendations")
        return sorted_scores

    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        return {}

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main route handler."""
    # Get all soil types from database
    soil_types = []
    try:
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'crops.db'))
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM soil_types')
        soil_types = [soil[0].lower() for soil in cursor.fetchall()]
        conn.close()
    except sqlite3.Error as e:
        logger.error(f"Error fetching soil types: {e}")

    if request.method == 'POST':
        conditions = {
            'temperature': request.form['temperature'],
            'rainfall': request.form['rainfall'],
            'soil_type': request.form['soil_type'],
            'humidity': request.form.get('humidity', 70),
            'ph': request.form.get('ph', 6.5),
        }
        
        errors = validate_input(conditions)
        if errors:
            return render_template('index.html', errors=errors, soil_types=soil_types)
        
        recommendations = recommend_crop(conditions)
        logger.info(f"Rendering template with {len(recommendations)} recommendations")
        return render_template('index.html', 
                             recommendations=recommendations,
                             current_season=get_current_season(),
                             conditions=conditions,
                             soil_types=soil_types)
    
    return render_template('index.html', soil_types=soil_types)

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    """API endpoint for crop recommendations."""
    try:
        conditions = request.get_json()
        errors = validate_input(conditions)
        if errors:
            return jsonify({'errors': errors}), 400
        
        recommendations = recommend_crop(conditions)
        return jsonify({
            'recommendations': recommendations,
            'current_season': get_current_season()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
