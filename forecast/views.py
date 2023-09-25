from django.shortcuts import render
from django.utils.safestring import mark_safe
import requests
import folium

def landing(request):
    return render(request, 'forecast/landing.html')

def forecast(request):
    lat, lon = 18.4655, -66.1057

    headers = {
        "User-Agent": "HurricanePreparednessApp/1.2 lugo.emanuel@gmail.com"
    }
    metadata_url = f"https://api.weather.gov/points/{lat},{lon}"
    response = requests.get(metadata_url, headers=headers)
    forecast_url = response.json()['properties']['forecast']
    forecast_response = requests.get(forecast_url, headers=headers)
    forecast_data = forecast_response.json()['properties']['periods']

    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon], tooltip="Your Location").add_to(m)
    map_html = mark_safe(m._repr_html_())

    context = {
        "forecast_data": forecast_data,
        "map": map_html
    }

    return render(request, 'forecast.html', context)
