from loans import views
from django.urls import path

urlpatterns = [
    path('go/', views.scrape_data),
    path('clear/', views.clear_data),
    path('countries/', views.get_countries),
    path('sectors/', views.get_sectors),
    path('projects/', views.get_projects),
    path('loans/', views.get_loans),
]
