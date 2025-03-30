from django.urls import path
from . import views

app_name = 'rocket_port_predictor'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('thank-you/', views.ThankYouView.as_view(), name='thank_you'),
    path('mission-form/', views.MissionPredictionView.as_view(), name='mission_form'),
    path('prediction-results/', views.PredictionResultsView.as_view(), name='prediction_results'),
] 