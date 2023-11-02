from django.shortcuts import render
from django.utils.safestring import mark_safe
import requests
import folium
from .models import WeatherForecast
import re
from datetime import datetime



def landing(request):
    return render(request, 'forecast/landing.html')

def parse_forecast_details(detailed_forecast):
    # Regular expressions to find temperature, wind, and precipitation details
    temp_pattern = r"High near (\d+)|low around (\d+)"
    wind_pattern = r"(\d+ mph)"
    precipitation_pattern = r"Chance of precipitation is (\d+)%"
    rainfall_pattern = r"New rainfall amounts between (.+) possible"

    # Find all matches in the forecast string
    temp_matches = re.findall(temp_pattern, detailed_forecast)
    wind_match = re.search(wind_pattern, detailed_forecast)
    precipitation_match = re.search(precipitation_pattern, detailed_forecast)
    rainfall_match = re.search(rainfall_pattern, detailed_forecast)

    # Extract the temperature, wind, and precipitation details
    temperature_high = None
    temperature_low = None
    for high, low in temp_matches:
        if high:
            temperature_high = int(high)
        if low:
            temperature_low = int(low)

    wind = wind_match.group(0) if wind_match else None
    chance_of_precipitation = int(precipitation_match.group(1)) if precipitation_match else None
    precipitation_amount = rainfall_match.group(1) if rainfall_match else None

    return {
        "temperature_high": temperature_high,
        "temperature_low": temperature_low,
        "wind": wind,
        "chance_of_precipitation": chance_of_precipitation,
        "precipitation_amount": precipitation_amount
    }


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

    # Parse each period's forecast and save to the database
    for period in forecast_data:
        parsed_details = parse_forecast_details(period['detailedForecast'])
        precipitation_amount = parsed_details.get('precipitation_amount', 'Not provided')
        # Create a new WeatherForecast instance (or update existing entries)
        weather_forecast, created = WeatherForecast.objects.update_or_create(
            period_name=period['name'],
            defaults={
                'detailed_forecast': period['detailedForecast'],
                'temperature_high': parsed_details.get('temperature_high'),
                'temperature_low': parsed_details.get('temperature_low'),
                'wind': parsed_details.get('wind', 'Not provided'),
                'chance_of_precipitation': parsed_details.get('chance_of_precipitation'),
                'precipitation_amount': parsed_details.get('precipitation_amount'),
                # Assuming the period['startTime'] is in ISO format
                'forecast_date': datetime.fromisoformat(period['startTime']).date()
            }
        )

    # After saving the data to the database, you can decide what to do next.
    # For example, you might want to redirect to another page, or simply render a page with a success message.
    # Here, we'll just render the same page with a context that includes the forecast data.
    context = {
        "forecast_data": forecast_data,  # You can now retrieve this from the database if preferred
    }

    return render(request, 'forecast/forecast.html', context)