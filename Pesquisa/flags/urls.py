from django.urls import path
from . import views

app_name = 'flags'

urlpatterns = [
    path('', views.examples, name='examples'),
    path('api/countries/', views.countries_api, name='countries_api'),
    path('country/<str:country_code>/', views.country_detail, name='country_detail'),
]