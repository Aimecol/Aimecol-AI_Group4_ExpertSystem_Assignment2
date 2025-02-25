from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    scientific_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    
    # Growing conditions
    temp_range = db.Column(db.String(50), nullable=False)
    rainfall_range = db.Column(db.String(50), nullable=False)
    ph_range = db.Column(db.String(50), nullable=False)
    humidity_range = db.Column(db.String(50), nullable=False)
    
    # Timing
    seasons = db.Column(db.String(50), nullable=False)
    growth_duration = db.Column(db.Integer)  # Days to harvest
    planting_depth = db.Column(db.Float)     # In centimeters
    
    # Soil requirements
    soil_types = db.Column(db.String(100), nullable=False)
    soil_drainage = db.Column(db.String(50))
    soil_fertility = db.Column(db.String(50))
    
    # Nutrient requirements
    nutrients = db.Column(db.String(200), nullable=False)
    water_needs = db.Column(db.String(50))
    sunlight_needs = db.Column(db.String(50))
    
    # Management
    pest_susceptibility = db.Column(db.Text)
    disease_susceptibility = db.Column(db.Text)
    farming_practices = db.Column(db.Text)
    
    # Economic factors
    yield_range = db.Column(db.String(50))
    market_value = db.Column(db.String(50))
    storage_life = db.Column(db.String(50))
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Crop {self.name}>'

class SoilType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    texture = db.Column(db.String(50))
    drainage = db.Column(db.String(50))
    water_retention = db.Column(db.String(50))
    nutrient_retention = db.Column(db.String(50))
    ph_range = db.Column(db.String(50))
    organic_matter = db.Column(db.String(50))
    suitable_crops = db.Column(db.Text)
    management_practices = db.Column(db.Text)

class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    start_month = db.Column(db.Integer)
    end_month = db.Column(db.Integer)
    characteristics = db.Column(db.Text)
    suitable_crops = db.Column(db.Text)
    rainfall_pattern = db.Column(db.String(100))
    temperature_range = db.Column(db.String(50))
