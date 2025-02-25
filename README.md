# Smart Crop Recommendation System

An intelligent agricultural expert system that provides data-driven crop recommendations based on environmental conditions, soil characteristics, and seasonal factors.

## Features

- 🌱 SQLite-based crop database with detailed information
- 🌍 Comprehensive soil type analysis and recommendations
- 🌤️ Seasonal growing patterns integration
- 🌡️ Environmental condition analysis:
  - Temperature ranges
  - Rainfall requirements
  - Humidity levels
  - pH levels
- 🏗️ Advanced database architecture:
  - Crops database
  - Soil types database
  - Seasons database
- 📊 Sophisticated scoring algorithm
- 💻 Modern, responsive interface

## Technical Stack

- **Backend**: Python 3.x, Flask
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Dependencies**: See requirements.txt
- **Development**: Logging, Error Handling, Data Validation

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Aimecol/AI_Group4_ExpertSystem_Assignment2.git
cd project-folder
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install requirements:

```bash
pip install -r requirements.txt
```

4. Initialize the database:

```bash
python crop_database_setup.py
```

5. Run the application:

```bash
python main.py
```

The system will be available at `http://localhost:5000`

## Project Structure

```
project-folder/
│
├── main.py                 # Application entry point
├── app_factory.py         # Flask app configuration
├── models.py             # Database models
├── crop_database_setup.py # Database initialization
├── init_db.py
│
├── static/
│   └── style.css         # CSS styles
│
├── templates/
│   └── index.html        # Main template
│
├── crops.db              # SQLite database
├── requirements.txt      # Project dependencies
└── README.md            # Documentation
```

## Database Schema

### Crops Table

- Temperature ranges
- Rainfall requirements
- pH levels
- Humidity ranges
- Soil type compatibility
- Seasonal information
- Nutrient requirements

### Soil Types Table

- Physical characteristics
- Water retention
- Nutrient content
- Crop suitability
- Management practices

### Seasons Table

- Growing periods
- Weather patterns
- Suitable crops
- Farming activities

## Usage

1. Input environmental conditions:
   - Temperature (°C)
   - Rainfall (mm)
   - Select soil type
2. System will:
   - Filter compatible crops
   - Calculate matching scores
   - Provide detailed recommendations
   - Show growing tips

## Development

- Built with modular architecture
- Implements SQLite for data persistence
- Features comprehensive error handling
- Includes detailed logging
- Uses responsive design principles

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open Pull Request

## License

MIT License - see LICENSE file

## Acknowledgments

- Agricultural data from research institutions
- Soil science guidelines from agricultural departments
- Weather pattern data from meteorological institutes
