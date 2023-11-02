from django.db import models

# Create your models here.
class WeatherForecast(models.Model):
    period_name = models.CharField(max_length=100, help_text="Name of the forecast period, e.g., 'This Afternoon', 'Tonight'")
    detailed_forecast = models.TextField(help_text="Full text of the weather forecast")
    temperature_high = models.IntegerField(null=True, blank=True, help_text="High temperature for the period, if applicable")
    temperature_low = models.IntegerField(null=True, blank=True, help_text="Low temperature for the period, if applicable")
    wind = models.CharField(max_length=255, null=True, blank=True)
    chance_of_precipitation = models.IntegerField(null=True, blank=True, help_text="Chance of precipitation as a percentage")
    precipitation_amount = models.CharField(max_length=255, null=True, blank=True)
    forecast_date = models.DateField(help_text="The date for which the forecast applies")

    def __str__(self):
        return f"{self.period_name} ({self.forecast_date})"

    class Meta:
        verbose_name = "Weather Forecast"
        verbose_name_plural = "Weather Forecasts"
        ordering = ['forecast_date', 'period_name']
