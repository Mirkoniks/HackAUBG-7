from django.urls import path
from . import views

app_name = 'rocket_port_predictor'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('thank-you/', views.ThankYouView.as_view(), name='thank_you'),
    path('mission/', views.MissionPredictionView.as_view(), name='mission_form'),
    path('results/', views.PredictionResultsView.as_view(), name='prediction_results'),
] 