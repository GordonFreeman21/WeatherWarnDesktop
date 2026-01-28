"""
API Client module for fetching weather data from OpenWeatherMap API
"""

import requests
from datetime import datetime
import pytz
from typing import Dict, Optional, List
from .config import config


class WeatherAPIError(Exception):
    """Custom exception for weather API errors"""
    pass


class WeatherAPIClient:
    """Client for interacting with OpenWeatherMap API"""
    
    def __init__(self):
        """Initialize the API client"""
        config.validate()
        self.api_key = config.api_key
        self.session = requests.Session()
        self.session.params = {'appid': self.api_key}
        
    def get_current_weather(self, city: str, units: str = 'metric') -> Dict:
        """
        Fetch current weather data for a city
        
        Args:
            city: City name (can include country code, e.g., "London,UK")
            units: Temperature units ('metric' for Celsius, 'imperial' for Fahrenheit)
            
        Returns:
            Dictionary containing weather data
            
        Raises:
            WeatherAPIError: If the API request fails
        """
        try:
            params = {
                'q': city,
                'units': units
            }
            
            response = self.session.get(
                config.current_weather_url,
                params=params,
                timeout=10
            )
            
            # Handle different error responses
            if response.status_code == 404:
                raise WeatherAPIError(f"City '{city}' not found. Please check the spelling.")
            elif response.status_code == 401:
                raise WeatherAPIError("Invalid API key. Please check your configuration.")
            elif response.status_code != 200:
                raise WeatherAPIError(f"API error: {response.status_code} - {response.text}")
            
            return self._process_current_weather(response.json())
            
        except requests.exceptions.Timeout:
            raise WeatherAPIError("Request timed out. Please check your internet connection.")
        except requests.exceptions.ConnectionError:
            raise WeatherAPIError("Connection error. Please check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise WeatherAPIError(f"Network error: {str(e)}")
    
    def get_forecast(self, city: str, units: str = 'metric', days: int = 5) -> List[Dict]:
        """
        Fetch weather forecast for a city
        
        Args:
            city: City name
            units: Temperature units ('metric' or 'imperial')
            days: Number of days for forecast (max 5 for free tier)
            
        Returns:
            List of dictionaries containing forecast data
            
        Raises:
            WeatherAPIError: If the API request fails
        """
        try:
            params = {
                'q': city,
                'units': units,
                'cnt': min(days * 8, 40)  # API returns data in 3-hour intervals
            }
            
            response = self.session.get(
                config.forecast_url,
                params=params,
                timeout=10
            )
            
            if response.status_code == 404:
                raise WeatherAPIError(f"City '{city}' not found for forecast.")
            elif response.status_code != 200:
                raise WeatherAPIError(f"Forecast API error: {response.status_code}")
            
            return self._process_forecast(response.json(), days)
            
        except requests.exceptions.RequestException as e:
            raise WeatherAPIError(f"Forecast fetch error: {str(e)}")
    
    def _process_current_weather(self, data: Dict) -> Dict:
        """
        Process and structure current weather data
        
        Args:
            data: Raw API response data
            
        Returns:
            Processed weather data dictionary
        """
        return {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': round(data['main']['temp'], 1),
            'feels_like': round(data['main']['feels_like'], 1),
            'temp_min': round(data['main']['temp_min'], 1),
            'temp_max': round(data['main']['temp_max'], 1),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': round(data['wind']['speed'], 1),
            'wind_direction': data['wind'].get('deg', 0),
            'description': data['weather'][0]['description'].title(),
            'main': data['weather'][0]['main'],
            'icon': data['weather'][0]['icon'],
            'clouds': data['clouds']['all'],
            'visibility': data.get('visibility', 0) / 1000,  # Convert to km
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise'], tz=pytz.UTC),
            'sunset': datetime.fromtimestamp(data['sys']['sunset'], tz=pytz.UTC),
            'timezone': data['timezone'],
            'timestamp': datetime.now(pytz.UTC)
        }
    
    def _process_forecast(self, data: Dict, days: int) -> List[Dict]:
        """
        Process forecast data and group by day
        
        Args:
            data: Raw forecast API response
            days: Number of days to include
            
        Returns:
            List of daily forecast dictionaries
        """
        daily_forecasts = []
        current_date = None
        day_data = []
        
        for item in data['list']:
            forecast_date = datetime.fromtimestamp(item['dt']).date()
            
            # Group forecasts by day
            if current_date != forecast_date:
                if day_data and len(daily_forecasts) < days:
                    daily_forecasts.append(self._aggregate_day_forecast(day_data))
                day_data = []
                current_date = forecast_date
            
            day_data.append(item)
        
        # Add the last day
        if day_data and len(daily_forecasts) < days:
            daily_forecasts.append(self._aggregate_day_forecast(day_data))
        
        return daily_forecasts[:days]
    
    def _aggregate_day_forecast(self, day_data: List[Dict]) -> Dict:
        """
        Aggregate 3-hour forecasts into a single day forecast
        
        Args:
            day_data: List of 3-hour forecast data points
            
        Returns:
            Aggregated daily forecast
        """
        temps = [item['main']['temp'] for item in day_data]
        
        # Find the most common weather condition
        conditions = [item['weather'][0]['main'] for item in day_data]
        main_condition = max(set(conditions), key=conditions.count)
        
        # Get description from the most common condition
        for item in day_data:
            if item['weather'][0]['main'] == main_condition:
                description = item['weather'][0]['description']
                icon = item['weather'][0]['icon']
                break
        
        return {
            'date': datetime.fromtimestamp(day_data[0]['dt']).date(),
            'temp_min': round(min(temps), 1),
            'temp_max': round(max(temps), 1),
            'temp_avg': round(sum(temps) / len(temps), 1),
            'description': description.title(),
            'main': main_condition,
            'icon': icon,
            'humidity': round(sum(item['main']['humidity'] for item in day_data) / len(day_data)),
            'wind_speed': round(sum(item['wind']['speed'] for item in day_data) / len(day_data), 1)
        }