# OptiLaunch

An intelligent Django web app that simulates and predicts optimal space launch sites and weather conditions using Machine Learning.

Built as part of the HackAUBG 7 Hackathon, under the theme: "Space and Aerospace Innovation".

---

## Project Idea

Our mission is to make space exploration more accessible through predictive systems that help students, engineers, and startups simulate realistic rocket missions.

This proof-of-concept app predicts:
- The best launch site based on your custom rocket mission
- The forecasted weather for that site on your planned launch date

---

## AI Models Used

### 1. Launch Site Prediction (Classification)
- Dataset: [Kaggle - All Space Missions from 1957](https://www.kaggle.com/datasets/agirlcoding/all-space-missions-from-1957/data)
- Input Features:
  - Rocket name
  - Launch date (converted to year)
  - Cost of mission
  - Destination (e.g. Mars, Moon, LEO)
- Output: Best launch site and top 3 recommended locations

#### Why Random Forest?
We chose Random Forest because:
- Our dataset is structured/tabular and not deep enough for neural networks
- Random Forest gives strong performance with minimal tuning
- It achieved around 80% accuracy and handles categorical data well

We tested a neural network too, but the Random Forest model outperformed it in both accuracy and speed for our dataset size.

### 2. Weather Prediction (Regression)
- Dataset: [Kaggle - Global Weather Repository](https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository)
- Input Features:
  - City (closest large city to the spaceport)
  - Month (extracted from launch date)
- Output:
  - Forecasted average temperature
  - Forecasted wind speed

#### Why Random Forest Regressor?
- Handles nonlinear relationships
- Quick to train and accurate for historical weather patterns

Real aerospace companies use similar systems for launch planning, weather forecasting, and risk mitigation — this is a lightweight simulation of that process.

---

## Web App Features

- User inputs custom rocket details
- AI predicts launch location
- Map shows the top 3 predicted sites
- Click a pin to reveal:
  - Weather forecast
  - Launch success likelihood

---

## Tech Stack
- Backend: Django
- Frontend: Django templates + Leaflet.js (map)
- Database: PostgreSQL
- ML: Scikit-learn (Random Forest), Pandas, NumPy

---

## Repo Structure
```text
HackAUBG-7/
├── ml_models/                  # Trained models and notebooks
│   ├── FinalModelRandomForest.ipynb
│   ├── WeatherPrediction.ipynb
│   ├── *.pkl                   # Saved models and encoders
├── data/                       # Public datasets (or instructions)
├── app/                        # Django app
│   ├── views.py
│   ├── predictor.py            # Prediction logic
│   └── templates/
```

---

## Example Prediction

### Inputs
```python
rocket_name = "Falcon 9 Block 5"
launch_date = "2027-09-14"
cost = 40000000
destination = "Mars"
```

### Predicted Launch Site
LC-39A, Kennedy Space Center, Florida, USA

### Top 3 Launch Sites
- LC-39A: 32.2%
- SLC-41: 25.6%
- ELA-3: 18.3%

### Weather Prediction (Astana, September)
- Temperature: 16.06°C
- Wind: 19.12 km/h

---

## Team
- Developed by the RoboClub team from Technical University of Sofia
- Hackathon: HackAUBG 7

---

## Future Plans
- Add satellite trajectory optimization
- Integrate real-time weather APIs
- Allow full mission simulation for aerospace students

---

## License
Open-source for educational and demonstration purposes.

