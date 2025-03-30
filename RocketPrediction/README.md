# Rocket Port Prediction System

A Django-based web application that predicts optimal spaceport locations for rocket launches based on various parameters including launch date, payload weight, and destination.

## Features

- User Authentication System
  - User registration and login
  - Secure password management
  - User profile management

- Mission Planning
  - Create and manage launch missions
  - Input parameters:
    - Launch date (future dates only)
    - Payload weight
    - Destination selection
    - Mission name
  - Real-time validation of inputs
  - Mission history tracking

- Spaceport Prediction
  - ML-based prediction system for optimal spaceport locations
  - Takes into account:
    - Launch date
    - Payload weight
    - Destination coordinates
  - Provides confidence scores for predictions

## Technical Stack

- **Backend**: Django 5.1.7
- **Database**: PostgreSQL 13
- **Frontend**: 
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap 5
- **ML Components**: 
  - scikit-learn
  - joblib
  - pandas

## Prerequisites

- Python 3.11
- PostgreSQL 13
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd RocketPrediction
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL:
```bash
# Login to PostgreSQL
psql -U postgres

# Create the database
CREATE DATABASE rocket_prediction;

# Exit psql
\q
```

5. Set up environment variables:
```bash
export DEBUG=1
export DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

8. Start the development server:
```bash
python manage.py runserver
```

The application will be available at http://localhost:8000

## Project Structure

```
RocketPrediction/
├── rocket_port_predictor/     # Main Django application
│   ├── templates/            # HTML templates
│   ├── static/              # Static files (CSS, JS, images)
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   └── urls.py              # URL routing
├── spaceport_project/       # Django project settings
└── requirements.txt        # Python dependencies
```

## API Endpoints

### Authentication
- `/login/` - User login
- `/register/` - User registration
- `/logout/` - User logout

### Mission Management
- `/` - Home page
- `/mission/create/` - Create new mission
- `/mission/<int:pk>/` - View mission details
- `/mission/<int:pk>/edit/` - Edit mission
- `/mission/<int:pk>/delete/` - Delete mission

## Development

### Database Management

- Create migrations:
```bash
python manage.py makemigrations
```

- Apply migrations:
```bash
python manage.py migrate
```

- Create superuser:
```bash
python manage.py createsuperuser
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the repository or contact the development team.

## Acknowledgments

- Django framework
- Bootstrap 5 for UI components
- scikit-learn for ML capabilities
- All contributors and maintainers 