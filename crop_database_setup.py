import sqlite3
import json
import logging
import os

logger = logging.getLogger(__name__)

def init_db():
    """Initialize all tables in crops database"""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crops.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create all tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS crops (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        temp_min REAL,
        temp_max REAL,
        rain_min REAL,
        rain_max REAL,
        ph_min REAL,
        ph_max REAL,
        humidity_min REAL,
        humidity_max REAL,
        seasons TEXT,
        soil_types TEXT,
        nutrients TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS soil_types (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        texture TEXT,
        drainage TEXT,
        water_retention TEXT,
        nutrient_retention TEXT,
        ph_min REAL,
        ph_max REAL,
        organic_matter TEXT,
        suitable_crops TEXT,
        management_practices TEXT,
        characteristics TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS seasons (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        start_month INTEGER,
        end_month INTEGER,
        characteristics TEXT,
        suitable_crops TEXT,
        rainfall_pattern TEXT,
        temperature_range TEXT,
        humidity_range TEXT,
        daylight_hours TEXT,
        wind_pattern TEXT,
        farming_activities TEXT
    )
    ''')
    
    # Insert soil type data
    soil_types_data = [
        (1, 'Clay', 'Fine-textured soil with high nutrient content', 'Fine', 'Poor', 
         'High', 'High', 6.0, 7.0, 'Medium', 
         'Rice,Wheat,Cotton', 
         'Requires good drainage management and careful tillage',
         json.dumps({
             "particle_size": "< 0.002mm",
             "cec": "High",
             "compaction_risk": "High",
             "erosion_risk": "Low",
             "temperature_capacity": "High"
         })),
        
        (2, 'Loam', 'Medium-textured soil with balanced properties', 'Medium', 'Good',
         'Medium', 'Medium', 6.0, 7.5, 'High',
         'Most crops',
         'Ideal for most farming practices, maintain organic matter',
         json.dumps({
             "particle_size": "0.002-0.05mm",
             "cec": "Medium",
             "compaction_risk": "Medium",
             "erosion_risk": "Medium",
             "temperature_capacity": "Medium"
         })),
        
        (3, 'Sandy', 'Coarse-textured soil with good drainage', 'Coarse', 'Excellent',
         'Low', 'Low', 5.5, 7.0, 'Low',
         'Groundnut,Potato,Carrot',
         'Requires frequent irrigation and fertilization',
         json.dumps({
             "particle_size": "0.05-2.0mm",
             "cec": "Low",
             "compaction_risk": "Low",
             "erosion_risk": "High",
             "temperature_capacity": "Low"
         }))
    ]
    
    for soil in soil_types_data:
        try:
            cursor.execute('''
            INSERT OR IGNORE INTO soil_types (
                id, name, description, texture, drainage,
                water_retention, nutrient_retention, ph_min, ph_max,
                organic_matter, suitable_crops, management_practices, characteristics
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', soil)
        except sqlite3.IntegrityError:
            logger.warning(f"Soil type '{soil[1]}' already exists, skipping...")

    # Insert season data
    seasons_data = [
        (1, 'Kharif', 6, 10, 
         'Monsoon season with high rainfall and humidity',
         'Rice,Cotton,Sugarcane,Maize,Groundnut,Soybean',
         'Heavy monsoon rainfall (750-1500mm)',
         '25-35°C',
         '65-90%',
         '12-13 hours',
         'Strong monsoon winds',
         json.dumps({
             "land_preparation": "May-June",
             "sowing": "June-July",
             "harvesting": "September-October",
             "key_activities": [
                 "Field leveling",
                 "Monsoon preparation",
                 "Drainage management",
                 "Pest control"
             ]
         })),
        
        (2, 'Rabi', 11, 3,
         'Winter season with moderate temperatures',
         'Wheat,Mustard,Peas,Potato,Chickpea',
         'Light winter rainfall (50-250mm)',
         '15-25°C',
         '40-60%',
         '10-11 hours',
         'Cool dry winds',
         json.dumps({
             "land_preparation": "October",
             "sowing": "November",
             "harvesting": "March-April",
             "key_activities": [
                 "Soil preparation",
                 "Irrigation planning",
                 "Frost protection",
                 "Nutrient management"
             ]
         })),
        
        (3, 'Zaid', 3, 6,
         'Summer season between Rabi and Kharif',
         'Vegetables,Fruits,Fodder crops',
         'Minimal rainfall (0-100mm)',
         '30-40°C',
         '30-40%',
         '13-14 hours',
         'Hot dry winds',
         json.dumps({
             "land_preparation": "February",
             "sowing": "March",
             "harvesting": "May-June",
             "key_activities": [
                 "Irrigation management",
                 "Heat protection",
                 "Soil moisture conservation",
                 "Short duration crop planning"
             ]
         }))
    ]
    
    for season in seasons_data:
        try:
            cursor.execute('''
            INSERT OR IGNORE INTO seasons (
                id, name, start_month, end_month,
                characteristics, suitable_crops,
                rainfall_pattern, temperature_range,
                humidity_range, daylight_hours,
                wind_pattern, farming_activities
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', season)
        except sqlite3.IntegrityError:
            logger.warning(f"Season '{season[1]}' already exists, skipping...")

    # Insert crop data
    crops_data = [
        (1, 'Rice', 20, 35, 1000, 2000, 5.5, 6.5, 60, 85, 'Kharif', 'clay,loam', json.dumps({"nitrogen": "high", "phosphorus": "medium", "potassium": "medium"})),
        (2, 'Wheat', 15, 25, 600, 1100, 6.0, 7.0, 50, 70, 'Rabi', 'loam,clay', json.dumps({"nitrogen": "medium", "phosphorus": "medium", "potassium": "low"})),
        (3, 'Maize', 20, 30, 500, 800, 5.5, 7.5, 50, 75, 'Kharif,Rabi', 'loam,sandy', json.dumps({"nitrogen": "high", "phosphorus": "medium", "potassium": "medium"})),
        (4, 'Cotton', 21, 37, 500, 1500, 5.5, 8.5, 60, 80, 'Kharif', 'loam,clay', json.dumps({"nitrogen": "high", "phosphorus": "medium", "potassium": "high"})),
        (5, 'Sugarcane', 20, 35, 1500, 2500, 6.0, 7.5, 70, 90, 'Kharif', 'loam', json.dumps({"nitrogen": "high", "phosphorus": "medium", "potassium": "high"})),
        (6, 'Potato', 15, 25, 500, 700, 5.0, 6.5, 50, 75, 'Rabi', 'loam,sandy', json.dumps({"nitrogen": "medium", "phosphorus": "high", "potassium": "high"})),
        (7, 'Tomato', 20, 27, 400, 600, 6.0, 7.0, 65, 85, 'Rabi,Zaid', 'loam,sandy', json.dumps({"nitrogen": "medium", "phosphorus": "high", "potassium": "medium"})),
        (8, 'Groundnut', 20, 30, 500, 1250, 6.0, 7.5, 50, 75, 'Kharif', 'sandy,loam', json.dumps({"nitrogen": "low", "phosphorus": "medium", "potassium": "medium"})),
        (9, 'Soybean', 20, 30, 600, 1000, 6.0, 7.5, 55, 85, 'Kharif', 'loam', json.dumps({"nitrogen": "low", "phosphorus": "high", "potassium": "medium"})),
        (10, 'Mustard', 10, 25, 400, 600, 6.0, 7.0, 40, 60, 'Rabi', 'loam,clay', json.dumps({"nitrogen": "medium", "phosphorus": "medium", "potassium": "low"})),
        (11, 'Onion', 13, 24, 350, 550, 6.0, 7.0, 60, 70, 'Rabi', 'loam,clay', json.dumps({"nitrogen": "medium", "phosphorus": "high", "potassium": "medium"})),
        (12, 'Garlic', 12, 24, 600, 700, 6.0, 7.0, 50, 65, 'Rabi', 'loam', json.dumps({"nitrogen": "medium", "phosphorus": "medium", "potassium": "high"})),
        (13, 'Peas', 16, 24, 600, 800, 6.0, 7.5, 60, 70, 'Rabi', 'loam,sandy', json.dumps({"nitrogen": "low", "phosphorus": "medium", "potassium": "medium"})),
        (14, 'Sunflower', 20, 30, 500, 750, 6.5, 7.5, 50, 75, 'Kharif,Rabi', 'loam,sandy', json.dumps({"nitrogen": "medium", "phosphorus": "high", "potassium": "medium"})),
        (15, 'Jute', 24, 35, 1500, 2500, 6.0, 7.5, 65, 90, 'Kharif', 'loam,clay', json.dumps({"nitrogen": "high", "phosphorus": "medium", "potassium": "medium"})),
        (16, 'Chickpea', 15, 25, 600, 1000, 6.0, 8.0, 40, 60, 'Rabi', 'sandy,loam', json.dumps({"nitrogen": "low", "phosphorus": "medium", "potassium": "medium"})),
        (17, 'Turmeric', 20, 30, 1500, 2000, 6.0, 7.5, 70, 90, 'Kharif', 'loam', json.dumps({"nitrogen": "high", "phosphorus": "medium", "potassium": "high"})),
        (18, 'Black Pepper', 20, 35, 2000, 3000, 5.5, 6.5, 65, 95, 'Kharif', 'loam', json.dumps({"nitrogen": "high", "phosphorus": "medium", "potassium": "high"}))
    ]
    
    for crop in crops_data:
        try:
            cursor.execute('''
            INSERT OR IGNORE INTO crops (id, name, temp_min, temp_max, rain_min, rain_max, 
                              ph_min, ph_max, humidity_min, humidity_max, 
                              seasons, soil_types, nutrients)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', crop)
        except sqlite3.IntegrityError:
            logger.warning(f"Crop '{crop[1]}' already exists, skipping...")
    
    conn.commit()
    conn.close()
    logger.info("All database tables initialized successfully")
    return True

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    init_db()
