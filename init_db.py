import sqlite3
from models import db, Crop, SoilType, Season
from app_factory import create_app
import json
import logging
from crop_database_setup import init_db as setup_db  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_from_db():
    """Read crop data from SQLite database file"""
    # Initialize database
    if not setup_db():
        logger.error("Failed to initialize database")
        return {}
        
    conn = sqlite3.connect('crops.db')
    cursor = conn.cursor()
    
    try:
        # Query the database - schema creation is now handled in crop_database_setup.py
        cursor.execute('''
            SELECT name, 
                   temp_min, temp_max,
                   rain_min, rain_max,
                   ph_min, ph_max,
                   humidity_min, humidity_max,
                   seasons, soil_types, nutrients 
            FROM crops
        ''')
        crops_data = cursor.fetchall()
        
        if not crops_data:
            logger.warning("No crop data found in database!")
            return {}

        crop_dict = {}
        for crop in crops_data:
            try:
                (name, t_min, t_max, r_min, r_max, 
                 p_min, p_max, h_min, h_max,
                 seasons, soils, nutrients) = crop
                
                # Validate numeric ranges
                ranges = [(t_min, t_max), (r_min, r_max), 
                         (p_min, p_max), (h_min, h_max)]
                for min_val, max_val in ranges:
                    if min_val > max_val:
                        raise ValueError(f"Invalid range for {name}: min > max")

                crop_dict[name] = {
                    'temp_range': (float(t_min), float(t_max)),
                    'rainfall_range': (float(r_min), float(r_max)),
                    'ph_range': (float(p_min), float(p_max)),
                    'humidity_range': (float(h_min), float(h_max)),
                    'seasons': seasons.split(','),
                    'soil_types': soils.split(','),
                    'nutrients': json.loads(nutrients)
                }
                logger.info(f"Successfully loaded crop data for: {name}")

            except (ValueError, json.JSONDecodeError) as e:
                logger.error(f"Error processing crop {name}: {str(e)}")
                continue

        return crop_dict
    
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return {}
    finally:
        conn.close()

def init_soil_types():
    """Read soil types from SQLite database"""
    conn = sqlite3.connect('crops.db')  # Updated database name
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT name, description, texture, drainage,
                   water_retention, nutrient_retention,
                   ph_min, ph_max, organic_matter,
                   suitable_crops, management_practices
            FROM soil_types
        ''')
        soils_data = cursor.fetchall()
        
        if not soils_data:
            logger.warning("No soil types found in database!")
            return False
            
        for soil in soils_data:
            try:
                soil_data = {
                    'name': soil[0],
                    'description': soil[1],
                    'texture': soil[2],
                    'drainage': soil[3],
                    'water_retention': soil[4],
                    'nutrient_retention': soil[5],
                    'ph_range': f"{soil[6]}-{soil[7]}",
                    'organic_matter': soil[8],
                    'suitable_crops': soil[9],
                    'management_practices': soil[10]
                }
                soil_type = SoilType(**soil_data)
                db.session.add(soil_type)
                logger.info(f"Added soil type: {soil[0]}")
            except Exception as e:
                logger.error(f"Error adding soil type {soil[0]}: {str(e)}")
                continue
                
        return True
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return False
    finally:
        conn.close()

def init_seasons():
    """Read seasons from SQLite database"""
    conn = sqlite3.connect('crops.db')  # Updated database name
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT name, start_month, end_month, characteristics,
                   suitable_crops, rainfall_pattern, temperature_range,
                   farming_activities
            FROM seasons
        ''')
        seasons_data = cursor.fetchall()
        
        if not seasons_data:
            logger.warning("No seasons found in database!")
            return False
            
        for season in seasons_data:
            try:
                season_data = {
                    'name': season[0],
                    'start_month': season[1],
                    'end_month': season[2],
                    'characteristics': season[3],
                    'suitable_crops': season[4],
                    'rainfall_pattern': season[5],
                    'temperature_range': season[6]
                }
                activities = json.loads(season[7])
                season_data['farming_activities'] = ', '.join(activities['key_activities'])
                
                season_obj = Season(**season_data)
                db.session.add(season_obj)
                logger.info(f"Added season: {season[0]}")
            except Exception as e:
                logger.error(f"Error adding season {season[0]}: {str(e)}")
                continue
                
        return True
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return False
    finally:
        conn.close()

def init_crops():
    crop_data = init_from_db()
    if not crop_data:
        logger.error("Failed to initialize crops: No data available")
        return False

    for crop_name, data in crop_data.items():
        try:
            crop_data = {
                'name': crop_name,
                'scientific_name': 'Scientific name here',
                'description': f'Detailed description of {crop_name}',
                'temp_range': f"{data['temp_range'][0]}-{data['temp_range'][1]}",
                'rainfall_range': f"{data['rainfall_range'][0]}-{data['rainfall_range'][1]}",
                'ph_range': f"{data['ph_range'][0]}-{data['ph_range'][1]}",
                'humidity_range': f"{data['humidity_range'][0]}-{data['humidity_range'][1]}",
                'seasons': ','.join(data['seasons']),
                'growth_duration': 120,
                'planting_depth': 5.0,
                'soil_types': ','.join(data['soil_types']),
                'nutrients': json.dumps(data['nutrients']),
                'water_needs': 'Medium',
                'sunlight_needs': 'Full Sun',
                'pest_susceptibility': 'Common pests...',
                'disease_susceptibility': 'Common diseases...',
                'farming_practices': 'Recommended practices...',
                'yield_range': '2-3 tons/hectare',
                'market_value': 'High',
                'storage_life': '3-6 months'
            }
            crop = Crop(**crop_data)
            db.session.add(crop)
            logger.info(f"Added crop: {crop_name}")

        except Exception as e:
            logger.error(f"Error adding crop {crop_name}: {str(e)}")
            continue

    return True

def init_database():
    app = create_app()
    with app.app_context():
        try:
            db.create_all()
            if not (Crop.query.first() or SoilType.query.first() or Season.query.first()):
                init_soil_types()
                init_seasons()
                if init_crops():
                    db.session.commit()
                    logger.info("Database initialized successfully!")
                else:
                    logger.error("Failed to initialize database")
            else:
                logger.info("Database already contains data!")
        except Exception as e:
            logger.error(f"Database initialization error: {str(e)}")

if __name__ == '__main__':
    init_database()
