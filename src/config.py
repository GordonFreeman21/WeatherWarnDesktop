"""
Configuration module for Weather Application
Handles API keys and application settings
"""

import os
from dotenv import load_dotenv
from pathlib import Path

class Config:
    """Configuration class for managing app settings"""
    
    def __init__(self):
        # Load environment variables from .env file
        env_path = Path(__file__).resolve().parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)
        
        # API Configuration
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        # Default Settings
        self.default_city = os.getenv('DEFAULT_CITY', 'London')
        self.temperature_unit = os.getenv('TEMPERATURE_UNIT', 'celsius').lower()
        
        # API endpoints
        self.current_weather_url = f"{self.base_url}/weather"
        self.forecast_url = f"{self.base_url}/forecast"
        
    def validate(self):
        """Validate that required configuration is present"""
        if not self.api_key:
            raise ValueError(
                "API key not found. Please set OPENWEATHER_API_KEY in .env file"
            )
        return True

# Global config instance
config = Config()