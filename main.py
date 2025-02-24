from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Crop database with detailed information
CROP_DATABASE = {
    'Rice': {
        'temp_range': (20, 35),
        'rainfall_range': (1000, 2000),
        'ph_range': (5.5, 6.5),
        'humidity_range': (60, 85),
        'seasons': ['Kharif'],
        'soil_types': ['clay', 'loam'],
        'nutrients': {
            'nitrogen': 'high',
            'phosphorus': 'medium',
            'potassium': 'medium'
        }
    },
    'Wheat': {
        'temp_range': (15, 25),
        'rainfall_range': (600, 1100),
        'ph_range': (6.0, 7.0),
        'humidity_range': (50, 70),
        'seasons': ['Rabi'],
        'soil_types': ['loam', 'clay'],
        'nutrients': {
            'nitrogen': 'medium',
            'phosphorus': 'medium',
            'potassium': 'low'
        }
    },
    'Maize': {
        'temp_range': (20, 30),
        'rainfall_range': (500, 800),
        'ph_range': (5.5, 7.5),
        'humidity_range': (50, 75),
        'seasons': ['Kharif', 'Rabi'],
        'soil_types': ['loam', 'sandy'],
        'nutrients': {
            'nitrogen': 'high',
            'phosphorus': 'medium',
            'potassium': 'medium'
        }
    },
    'Cotton': {
        'temp_range': (21, 37),
        'rainfall_range': (500, 1500),
        'ph_range': (5.5, 8.5),
        'humidity_range': (60, 80),
        'seasons': ['Kharif'],
        'soil_types': ['loam', 'clay'],
        'nutrients': {
            'nitrogen': 'high',
            'phosphorus': 'medium',
            'potassium': 'high'
        }
    },
    'Sugarcane': {
        'temp_range': (20, 35),
        'rainfall_range': (1500, 2500),
        'ph_range': (6.0, 7.5),
        'humidity_range': (70, 90),
        'seasons': ['Kharif'],
        'soil_types': ['loam'],
        'nutrients': {
            'nitrogen': 'high',
            'phosphorus': 'medium',
            'potassium': 'high'
        }
    },
    'Potato': {
        'temp_range': (15, 25),
        'rainfall_range': (500, 700),
        'ph_range': (5.0, 6.5),
        'humidity_range': (50, 75),
        'seasons': ['Rabi'],
        'soil_types': ['loam', 'sandy'],
        'nutrients': {
            'nitrogen': 'medium',
            'phosphorus': 'high',
            'potassium': 'high'
        }
    },
    'Tomato': {
        'temp_range': (20, 27),
        'rainfall_range': (400, 600),
        'ph_range': (6.0, 7.0),
        'humidity_range': (65, 85),
        'seasons': ['Rabi', 'Zaid'],
        'soil_types': ['loam', 'sandy'],
        'nutrients': {
            'nitrogen': 'medium',
            'phosphorus': 'high',
            'potassium': 'medium'
        }
    },
    'Groundnut': {
        'temp_range': (25, 35),
        'rainfall_range': (500, 1250),
        'ph_range': (6.0, 7.5),
        'humidity_range': (50, 75),
        'seasons': ['Kharif'],
        'soil_types': ['sandy', 'loam'],
        'nutrients': {
            'nitrogen': 'low',
            'phosphorus': 'medium',
            'potassium': 'medium'
        }
    },
    'Soybean': {
        'temp_range': (20, 30),
        'rainfall_range': (600, 1000),
        'ph_range': (6.0, 7.5),
        'humidity_range': (55, 85),
        'seasons': ['Kharif'],
        'soil_types': ['loam'],
        'nutrients': {
            'nitrogen': 'low',
            'phosphorus': 'high',
            'potassium': 'medium'
        }
    },
    'Mustard': {
        'temp_range': (10, 25),
        'rainfall_range': (400, 600),
        'ph_range': (6.0, 7.0),
        'humidity_range': (40, 60),
        'seasons': ['Rabi'],
        'soil_types': ['loam', 'clay'],
        'nutrients': {
            'nitrogen': 'medium',
            'phosphorus': 'medium',
            'potassium': 'low'
        }
    },
    'Onion': {
        'temp_range': (13, 24),
        'rainfall_range': (350, 550),
        'ph_range': (6.0, 7.0),
        'humidity_range': (60, 70),
        'seasons': ['Rabi'],
        'soil_types': ['loam', 'clay'],
        'nutrients': {
            'nitrogen': 'medium',
            'phosphorus': 'high',
            'potassium': 'high'
        }
    },
    'Garlic': {
        'temp_range': (12, 24),
        'rainfall_range': (600, 700),
        'ph_range': (6.0, 7.0),
        'humidity_range': (50, 65),
        'seasons': ['Rabi'],
        'soil_types': ['loam'],
        'nutrients': {
            'nitrogen': 'medium',
            'phosphorus': 'medium',
            'potassium': 'high'
        }
    },
    'Peas': {
        'temp_range': (16, 24),
        'rainfall_range': (600, 800),
        'ph_range': (6.0, 7.5),
        'humidity_range': (60, 70),
        'seasons': ['Rabi'],
        'soil_types': ['loam', 'sandy'],
        'nutrients': {
            'nitrogen': 'low',
            'phosphorus': 'medium',
            'potassium': 'medium'
        }
    },
    'Sunflower': {
        'temp_range': (20, 30),
        'rainfall_range': (500, 750),
        'ph_range': (6.5, 7.5),
        'humidity_range': (50, 75),
        'seasons': ['Kharif', 'Rabi'],
        'soil_types': ['loam', 'sandy'],
        'nutrients': {
            'nitrogen': 'medium',
            'phosphorus': 'high',
            'potassium': 'medium'
        }
    },
    'Jute': {
        'temp_range': (24, 35),
        'rainfall_range': (1500, 2500),
        'ph_range': (6.0, 7.5),
        'humidity_range': (65, 90),
        'seasons': ['Kharif'],
        'soil_types': ['loam', 'clay'],
        'nutrients': {
            'nitrogen': 'high',
            'phosphorus': 'medium',
            'potassium': 'medium'
        }
    },
    'Chickpea': {
        'temp_range': (15, 25),
        'rainfall_range': (600, 1000),
        'ph_range': (6.0, 8.0),
        'humidity_range': (40, 60),
        'seasons': ['Rabi'],
        'soil_types': ['sandy', 'loam'],
        'nutrients': {
            'nitrogen': 'low',
            'phosphorus': 'medium',
            'potassium': 'medium'
        }
    },
    'Turmeric': {
        'temp_range': (20, 30),
        'rainfall_range': (1500, 2000),
        'ph_range': (6.0, 7.5),
        'humidity_range': (70, 90),
        'seasons': ['Kharif'],
        'soil_types': ['loam'],
        'nutrients': {
            'nitrogen': 'high',
            'phosphorus': 'medium',
            'potassium': 'high'
        }
    },
    'Black Pepper': {
        'temp_range': (20, 35),
        'rainfall_range': (2000, 3000),
        'ph_range': (5.5, 6.5),
        'humidity_range': (65, 95),
        'seasons': ['Kharif'],
        'soil_types': ['loam'],
        'nutrients': {
            'nitrogen': 'high',
            'phosphorus': 'medium',
            'potassium': 'high'
        }
    }
}

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
        return "Kharif"  # Monsoon season
    elif month <= 3 or month >= 11:
        return "Rabi"    # Winter season
    else:
        return "Zaid"    # Summer season

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
    """Enhanced crop recommendation system."""
    crop_scores = {}
    
    for crop, info in CROP_DATABASE.items():
        score = calculate_crop_score(info, conditions)
        if score >= 60:  # Only recommend crops with good compatibility
            crop_scores[crop] = {
                'score': score,
                'details': {
                    'optimal_temp': f"{info['temp_range'][0]}-{info['temp_range'][1]}°C",
                    'optimal_rainfall': f"{info['rainfall_range'][0]}-{info['rainfall_range'][1]}mm",
                    'suitable_soil': ', '.join(info['soil_types']),
                    'growing_season': ', '.join(info['seasons']),
                    'nutrients_needed': info['nutrients']
                }
            }
    
    # Sort crops by score
    recommended_crops = dict(sorted(crop_scores.items(), 
                                  key=lambda x: x[1]['score'], 
                                  reverse=True))
    
    return recommended_crops

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        conditions = {
            'temperature': request.form['temperature'],
            'rainfall': request.form['rainfall'],
            'soil_type': request.form['soil_type'],
            'humidity': request.form.get('humidity', 70),  # default value
            'ph': request.form.get('ph', 6.5),            # default value
        }
        
        # Validate input
        errors = validate_input(conditions)
        if errors:
            return render_template('index.html', errors=errors)
        
        # Get recommendations
        recommendations = recommend_crop(conditions)
        return render_template('index.html', 
                             recommendations=recommendations,
                             current_season=get_current_season())
    
    return render_template('index.html')

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
