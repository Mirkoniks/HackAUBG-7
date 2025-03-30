from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from .forms import ContactForm, MissionForm, UserRegistrationForm
import joblib
import os
import pandas as pd
from datetime import datetime
from .models import ContactMessage, MissionInput
import numpy as np

# Create your views here.

class HomeView(TemplateView):
    template_name = 'rocket_port_predictor/home.html'

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'rocket_port_predictor/register.html'
    success_url = reverse_lazy('rocket_port_predictor:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Account created successfully! Welcome to OptiLaunch.')
        return response

class CustomLoginView(LoginView):
    template_name = 'rocket_port_predictor/login.html'
    redirect_authenticated_user = True
    next_page = 'rocket_port_predictor:home'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Successfully logged in! Welcome back.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('rocket_port_predictor:home')

class ContactView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = 'rocket_port_predictor/contact.html'
    success_url = reverse_lazy('thank_you')

    def form_valid(self, form):
        messages.success(self.request, 'Thank you for your message! We will get back to you soon.')
        return super().form_valid(form)

class ThankYouView(TemplateView):
    template_name = 'rocket_port_predictor/thank_you.html'

class MissionPredictionView(LoginRequiredMixin, FormView):
    template_name = 'rocket_port_predictor/mission_form.html'
    form_class = MissionForm
    success_url = reverse_lazy('rocket_port_predictor:prediction_results')

    def get_seasonal_weather(self, city, month):
        # Define seasonal weather patterns for different regions
        weather_patterns = {
            'Cayenne': {  # Tropical climate
                'temp': {'winter': 26, 'spring': 27, 'summer': 28, 'fall': 27},
                'wind': {'winter': 15, 'spring': 12, 'summer': 10, 'fall': 12}
            },
            'Moscow': {  # Continental climate
                'temp': {'winter': -8, 'spring': 10, 'summer': 23, 'fall': 5},
                'wind': {'winter': 15, 'spring': 12, 'summer': 10, 'fall': 13}
            },
            'Orlando': {  # Subtropical climate
                'temp': {'winter': 15, 'spring': 23, 'summer': 28, 'fall': 20},
                'wind': {'winter': 12, 'spring': 15, 'summer': 10, 'fall': 12}
            },
            'Los Angeles': {  # Mediterranean climate
                'temp': {'winter': 18, 'spring': 20, 'summer': 24, 'fall': 22},
                'wind': {'winter': 10, 'spring': 12, 'summer': 8, 'fall': 10}
            },
            'Washington': {  # Humid subtropical climate
                'temp': {'winter': 3, 'spring': 15, 'summer': 26, 'fall': 14},
                'wind': {'winter': 15, 'spring': 14, 'summer': 10, 'fall': 12}
            },
            'Anchorage': {  # Subarctic climate
                'temp': {'winter': -5, 'spring': 5, 'summer': 18, 'fall': 5},
                'wind': {'winter': 20, 'spring': 15, 'summer': 12, 'fall': 18}
            },
            'Phoenix': {  # Desert climate
                'temp': {'winter': 15, 'spring': 25, 'summer': 35, 'fall': 25},
                'wind': {'winter': 8, 'spring': 12, 'summer': 10, 'fall': 8}
            },
            'London': {  # Maritime climate
                'temp': {'winter': 5, 'spring': 12, 'summer': 18, 'fall': 10},
                'wind': {'winter': 18, 'spring': 15, 'summer': 12, 'fall': 16}
            },
            'Stockholm': {  # Cold maritime climate
                'temp': {'winter': -3, 'spring': 8, 'summer': 20, 'fall': 7},
                'wind': {'winter': 20, 'spring': 15, 'summer': 12, 'fall': 18}
            }
        }
        
        # Get season based on month
        if month in [12, 1, 2]:
            season = 'winter'
        elif month in [3, 4, 5]:
            season = 'spring'
        elif month in [6, 7, 8]:
            season = 'summer'
        else:  # 9, 10, 11
            season = 'fall'
            
        city_weather = weather_patterns.get(city, weather_patterns['Orlando'])  # Default to Orlando if city not found
        return city_weather['temp'][season], city_weather['wind'][season]

    def form_valid(self, form):
        try:
            # Save the mission data with the current user
            mission = form.save(commit=False)
            mission.user = self.request.user
            mission.launch_status = 'Success'  # Set default launch status
            mission.save()
            
            # Load encoders
            models_dir = os.path.join('rocket_port_predictor', 'models')
            rocket_encoder = joblib.load(os.path.join(models_dir, 'le_rocket.pkl'))
            destination_encoder = joblib.load(os.path.join(models_dir, 'le_dest.pkl'))
            status_encoder = joblib.load(os.path.join(models_dir, 'le_status.pkl'))
            location_encoder = joblib.load(os.path.join(models_dir, 'le_location.pkl'))

            # Load the launch location prediction model
            launch_location_model = joblib.load(os.path.join(models_dir, 'launch_location_model.pkl'))
            
            # Format the launch date as YYYY-MM-DD
            formatted_date = mission.launch_date.strftime("%Y-%m-%d")
            launch_month = mission.launch_date.month
            
            # Create input data matching the notebook format
            input_data = {
                'rocket_name': mission.rocket_name,
                'launch_date': formatted_date,
                'cost': float(mission.cost_million),  # This should already be in millions
                'destination': mission.destination,
                'launch_status': 'Success'  # Always use Success as in the notebook
            }
            
            # Create DataFrame with the same structure as training data
            input_df = pd.DataFrame([input_data])
            
            # Print available classes for debugging
            print("Available rocket names:", rocket_encoder.classes_)
            print("Available destinations:", destination_encoder.classes_)
            print("Available status values:", status_encoder.classes_)
            print("Available locations:", location_encoder.classes_)
            print("Input data:", input_data)
            
            # Apply encoders and convert to Python int
            try:
                # Always use "Unknown" for rocket name encoding since we're allowing free text
                input_df['Rocket_enc'] = rocket_encoder.transform(['Unknown']).astype(int)
            except Exception as e:
                print(f"Error encoding rocket name: {e}")
                input_df['Rocket_enc'] = rocket_encoder.transform(['Unknown']).astype(int)
            
            try:
                input_df['Destination_enc'] = destination_encoder.transform([mission.destination]).astype(int)
            except Exception as e:
                print(f"Error encoding destination: {e}")
                input_df['Destination_enc'] = destination_encoder.transform(['Unknown']).astype(int)
            
            try:
                # Always use "Success" for status encoding as in the notebook
                input_df['Status_enc'] = status_encoder.transform(['Success']).astype(int)
            except Exception as e:
                print(f"Error encoding status: {e}")
                input_df['Status_enc'] = status_encoder.transform(['Success']).astype(int)

            # Extract year from launch date
            input_df['Year'] = pd.to_datetime(input_df['launch_date']).dt.year.astype(int)
            
            # Create final feature DataFrame with correct column names and data types
            # Ensure the order matches the training data exactly
            features_df = pd.DataFrame({
                'Rocket_enc': input_df['Rocket_enc'],
                'Year': input_df['Year'],
                'Cost': input_df['cost'].astype(float),
                'Status_enc': input_df['Status_enc'],
                'Destination_enc': input_df['Destination_enc']
            })
            
            # Print the final features for debugging
            print("Final features:", features_df)
            print("Feature types:", features_df.dtypes)
            
            # Get predictions using DataFrame directly to preserve feature names
            try:
                predictions = launch_location_model.predict_proba(features_df)[0]
                print("Raw predictions:", predictions)
            except Exception as e:
                print(f"Error during prediction: {e}")
                # If prediction fails, return default predictions
                predictions = np.array([0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
            
            # Get the indices of the top 3 predictions
            top_3_indices = predictions.argsort()[-3:][::-1]
            
            # Get the actual location names from the encoder
            location_names = location_encoder.inverse_transform(top_3_indices)
            print("Top 3 location names:", location_names)
            
            spaceports = []
            
            # Define spaceport names and their coordinates and nearest weather city
            spaceport_info = {
                'ELV-1 (SLV), Guiana Space Centre, French Guiana, France': {
                    'coordinates': [5.2367, -52.7697],
                    'weather_city': 'Cayenne'  # Nearest city in French Guiana
                },
                'Site 370/13, Yasny Cosmodrome, Russia': {
                    'coordinates': [51.2083, 59.8500],
                    'weather_city': 'Moscow'  # Major Russian city
                },
                'Site 43/3, Plesetsk Cosmodrome, Russia': {
                    'coordinates': [62.9271, 40.5777],
                    'weather_city': 'Moscow'  # Major Russian city
                },
                'LC-39A, Kennedy Space Center, Florida, USA': {
                    'coordinates': [28.5729, -80.6490],
                    'weather_city': 'Orlando'  # Nearest major city
                },
                'SLC-40, Cape Canaveral Space Force Station, Florida, USA': {
                    'coordinates': [28.4866, -80.5446],
                    'weather_city': 'Orlando'  # Nearest major city
                },
                'SLC-4E, Vandenberg Space Force Base, California, USA': {
                    'coordinates': [34.7420, -120.5724],
                    'weather_city': 'Los Angeles'  # Nearest major city
                },
                'LP-0A, Wallops Flight Facility, Virginia, USA': {
                    'coordinates': [37.9402, -75.4664],
                    'weather_city': 'Washington'  # Nearest major city
                },
                'LP-3B, Pacific Spaceport Complex, Alaska, USA': {
                    'coordinates': [57.4333, -152.3417],
                    'weather_city': 'Anchorage'  # Nearest major city
                },
                'Launch Site One, Spaceport America, New Mexico, USA': {
                    'coordinates': [32.9904, -106.9749],
                    'weather_city': 'Phoenix'  # Nearest major city
                },
                'Launch Complex, Mojave Air and Space Port, California, USA': {
                    'coordinates': [35.0594, -118.1517],
                    'weather_city': 'Los Angeles'  # Nearest major city
                },
                'Launch Complex, Spaceport Cornwall, Newquay, UK': {
                    'coordinates': [50.4404, -5.0007],
                    'weather_city': 'London'  # Major UK city
                },
                'Launch Complex, Esrange Space Center, Sweden': {
                    'coordinates': [67.8856, 21.0800],
                    'weather_city': 'Stockholm'  # Major Swedish city
                }
            }
            
            # Get top 3 spaceports with their probabilities and weather predictions
            for idx, location_name in zip(top_3_indices, location_names):
                location_name = str(location_name)  # Convert numpy string to Python string
                if location_name in spaceport_info:
                    spaceport = spaceport_info[location_name]
                    probability = float(predictions[idx]) * 100  # Convert to percentage
                    
                    # Get weather prediction based on seasonal patterns
                    weather_city = spaceport['weather_city']
                    temp, wind = self.get_seasonal_weather(weather_city, launch_month)
                    
                    spaceports.append({
                        'name': location_name,
                        'coordinates': spaceport['coordinates'],
                        'probability': round(probability, 2),
                        'weather': {
                            'temperature': temp,
                            'wind_speed': wind,
                            'city': weather_city
                        }
                    })
                else:
                    print(f"Warning: Location '{location_name}' not found in spaceport_info")
            
            # Store predictions in session for display
            print("Storing spaceports in session:", spaceports)
            self.request.session['spaceport_predictions'] = spaceports
            return super().form_valid(form)
            
        except Exception as e:
            print(f"Full error details: {str(e)}")
            messages.error(self.request, f"Error during prediction: {str(e)}")
            return self.form_invalid(form)

class PredictionResultsView(LoginRequiredMixin, TemplateView):
    template_name = 'rocket_port_predictor/prediction_results.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spaceports = self.request.session.get('spaceport_predictions', [])
        print("Debug - Spaceports from session:", spaceports)  # Debug output
        context['spaceports'] = spaceports
        return context
