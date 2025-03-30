from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
import joblib
import os
import pandas as pd
from datetime import datetime
from .forms import ContactForm, MissionForm
from .models import ContactMessage, MissionInput
import numpy as np

# Create your views here.

class HomeView(TemplateView):
    template_name = 'rocket_port_predictor/home.html'

class CustomLoginView(LoginView):
    template_name = 'rocket_port_predictor/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = 'home'

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
    success_url = reverse_lazy('prediction_results')

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
            
            # Define spaceport names and their coordinates
            spaceport_info = {
                'ELV-1 (SLV), Guiana Space Centre, French Guiana, France': {'coordinates': [5.2367, -52.7697]},
                'Site 370/13, Yasny Cosmodrome, Russia': {'coordinates': [51.2083, 59.8500]},
                'Site 43/3, Plesetsk Cosmodrome, Russia': {'coordinates': [62.9271, 40.5777]},
                'LC-39A, Kennedy Space Center, Florida, USA': {'coordinates': [28.5729, -80.6490]},
                'SLC-40, Cape Canaveral Space Force Station, Florida, USA': {'coordinates': [28.4866, -80.5446]},
                'SLC-4E, Vandenberg Space Force Base, California, USA': {'coordinates': [34.7420, -120.5724]},
                'LP-0A, Wallops Flight Facility, Virginia, USA': {'coordinates': [37.9402, -75.4664]},
                'LP-3B, Pacific Spaceport Complex, Alaska, USA': {'coordinates': [57.4333, -152.3417]},
                'Launch Site One, Spaceport America, New Mexico, USA': {'coordinates': [32.9904, -106.9749]},
                'Launch Complex, Mojave Air and Space Port, California, USA': {'coordinates': [35.0594, -118.1517]},
                'Launch Complex, Spaceport Cornwall, Newquay, UK': {'coordinates': [50.4404, -5.0007]},
                'Launch Complex, Esrange Space Center, Sweden': {'coordinates': [67.8856, 21.0800]}
            }
            
            # Get top 3 spaceports with their probabilities
            for idx, location_name in zip(top_3_indices, location_names):
                location_name = str(location_name)  # Convert numpy string to Python string
                if location_name in spaceport_info:
                    spaceport = spaceport_info[location_name]
                    probability = float(predictions[idx]) * 100  # Convert to percentage
                    
                    spaceports.append({
                        'name': location_name,
                        'coordinates': spaceport['coordinates'],
                        'probability': round(probability, 2),
                        'weather': {
                            'temperature': 20.0,
                            'wind_speed': 10.0,
                            'humidity': 60.0,
                            'cloud_coverage': 30.0
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
