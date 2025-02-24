# Smart Crop Recommendation System

A sophisticated web-based application that provides intelligent crop recommendations based on environmental conditions and soil characteristics.

## Features

- 🌱 Comprehensive crop database with 18+ crops
- 🌡️ Environmental factor analysis (temperature, rainfall, humidity)
- 🗺️ Soil type compatibility checking
- 📊 Detailed nutrient requirement analysis
- 🎯 Compatibility scoring system
- 📅 Seasonal growing recommendations
- 💻 Modern, responsive UI
- 🔍 Real-time input validation
- 🌐 RESTful API support

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3
- **Icons**: Font Awesome
- **API**: JSON REST API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Aimecol/AI_Group4_ExpertSystem_Assignment2.git
cd project-folder
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install flask
```

4. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
project-folder/
│
├── main.py              # Main Flask application
├── static/
│   └── style.css       # CSS styles
├── templates/
│   └── index.html      # HTML template
└── README.md           # Documentation
```

## Usage

1. Open the application in your web browser
2. Enter the following environmental parameters:
   - Temperature (°C)
   - Rainfall (mm)
   - Soil Type (Clay/Loam/Sandy)
   - pH Level (optional)
   - Humidity (optional)
3. Click "Get Recommendations"
4. View the recommended crops with their:
   - Compatibility score
   - Optimal growing conditions
   - Required nutrients
   - Suitable seasons

## API Usage

The system provides a REST API endpoint for programmatic access:

```bash
POST /api/recommend
Content-Type: application/json

{
    "temperature": 25,
    "rainfall": 1000,
    "soil_type": "loam",
    "ph": 6.5,
    "humidity": 70
}
```

Response:
```json
{
    "recommendations": {
        "Rice": {
            "score": 85,
            "details": {
                "optimal_temp": "20-35°C",
                "optimal_rainfall": "1000-2000mm",
                "suitable_soil": "clay, loam",
                "growing_season": "Kharif",
                "nutrients_needed": {
                    "nitrogen": "high",
                    "phosphorus": "medium",
                    "potassium": "medium"
                }
            }
        }
    },
    "current_season": "Kharif"
}
```

## Supported Crops

- Rice
- Wheat
- Maize
- Cotton
- Sugarcane
- Potato
- Tomato
- Groundnut
- Soybean
- Mustard
- Onion
- Garlic
- Peas
- Sunflower
- Jute
- Chickpea
- Turmeric
- Black Pepper

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Agricultural data sourced from various agricultural research institutions
- Weather data patterns from meteorological departments
- Soil composition guidelines from soil science research

## Support

For support, please open an issue in the GitHub repository or contact the development team.