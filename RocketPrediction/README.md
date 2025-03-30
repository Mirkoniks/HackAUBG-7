# Spaceport Location Predictor

A Django web application that predicts optimal spaceport locations for space missions using machine learning models.

## Features

- User authentication system
- Contact form for inquiries
- Mission input form with prediction capabilities
- Interactive map display of recommended spaceport locations
- Weather predictions for each recommended location

## Prerequisites

- Python 3.8 or higher
- Django 4.2 or higher
- PostgreSQL 13 or higher
- Required Python packages (see requirements.txt)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd spaceport-project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL:
```bash
# Login to PostgreSQL
psql -U postgres

# Create the database
CREATE DATABASE spaceport_db;

# Exit psql
\q
```

5. Create the models directory and add your ML models:
```bash
mkdir rocket_port_predictor/models
```

6. Add your ML model files to the `rocket_port_predictor/models/` directory:
- `launch_location_model.pkl`: Main model for predicting spaceport locations
- `weather_model_port1.pkl`: Weather prediction model for first spaceport
- `weather_model_port2.pkl`: Weather prediction model for second spaceport
- `weather_model_port3.pkl`: Weather prediction model for third spaceport

7. Apply database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

8. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

9. Run the development server:
```bash
python manage.py runserver
```

10. Visit http://127.0.0.1:8000/ in your web browser

## Database Configuration

The application uses PostgreSQL as its database. The default configuration in `settings.py` assumes:
- Database name: `spaceport_db`
- Username: `postgres`
- Password: `postgres`
- Host: `localhost`
- Port: `5432`

If your PostgreSQL setup is different, update these settings in `settings.py` accordingly.

## Project Structure

```
spaceport_project/
├── manage.py
├── requirements.txt
├── spaceport_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── rocket_port_predictor/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── models/
    │   ├── launch_location_model.pkl
    │   ├── weather_model_port1.pkl
    │   ├── weather_model_port2.pkl
    │   └── weather_model_port3.pkl
    ├── templates/
    │   └── rocket_port_predictor/
    │       ├── base.html
    │       ├── home.html
    │       ├── login.html
    │       ├── contact.html
    │       ├── thank_you.html
    │       ├── mission_form.html
    │       └── prediction_results.html
    ├── urls.py
    └── views.py
```

## Model Requirements

The ML models should be trained to provide the following outputs:

### Launch Location Model (`launch_location_model.pkl`)
- Input features: budget, launch date (month, day)
- Output: probability distribution over possible spaceport locations

### Weather Models (`weather_model_portX.pkl`)
- Input features: same as launch location model
- Output: [latitude, longitude, temperature, wind_speed, humidity, cloud_coverage]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 