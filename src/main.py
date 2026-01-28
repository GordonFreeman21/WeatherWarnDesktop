#!/usr/bin/env python3
"""
Weather Application - Main Entry Point
A CLI application to fetch and display weather information
"""

import sys
from typing import Optional
from .api_client import WeatherAPIClient, WeatherAPIError
from .weather_display import WeatherDisplay
from .config import config


class WeatherApp:
    """Main application class for the weather app"""
    
    def __init__(self):
        """Initialize the weather application"""
        self.api_client = WeatherAPIClient()
        self.display = WeatherDisplay()
        self.current_city = config.default_city
        self.temperature_unit = config.temperature_unit
        self.current_weather = None
        self.forecast_data = None
    
    def run(self):
        """Main application loop"""
        self.display.clear_screen()
        self.display.display_welcome()
        
        # Fetch initial weather for default city
        self.fetch_weather(self.current_city)
        
        # Main menu loop
        while True:
            self.display.display_menu()
            
            choice = self.display.get_input("Enter your choice (1-5):")
            
            if choice == '1':
                self.search_city()
            elif choice == '2':
                self.toggle_temperature_unit()
            elif choice == '3':
                self.refresh_weather()
            elif choice == '4':
                self.show_forecast()
            elif choice == '5':
                self.exit_app()
            else:
                self.display.show_error("Invalid choice. Please enter a number between 1 and 5.")
    
    def fetch_weather(self, city: str):
        """
        Fetch weather data for a given city
        
        Args:
            city: City name to fetch weather for
        """
        self.display.show_loading(f"Fetching weather for {city}...")
        
        try:
            # Determine API units based on current setting
            api_units = 'metric' if self.temperature_unit == 'celsius' else 'imperial'
            
            # Fetch current weather
            self.current_weather = self.api_client.get_current_weather(city, api_units)
            self.current_city = city
            
            # Display the weather
            self.display.clear_screen()
            self.display.display_current_weather(self.current_weather, self.temperature_unit)
            
        except WeatherAPIError as e:
            self.display.show_error(str(e))
        except Exception as e:
            self.display.show_error(f"Unexpected error: {str(e)}")
    
    def search_city(self):
        """Handle city search functionality"""
        city = self.display.get_input("Enter city name (e.g., London or London,UK):")
        
        # Validate input
        if not city or city.strip() == '':
            self.display.show_error("City name cannot be empty.")
            return
        
        self.fetch_weather(city.strip())
    
    def toggle_temperature_unit(self):
        """Toggle between Celsius and Fahrenheit"""
        if self.temperature_unit == 'celsius':
            self.temperature_unit = 'fahrenheit'
            unit_display = 'Fahrenheit (°F)'
        else:
            self.temperature_unit = 'celsius'
            unit_display = 'Celsius (°C)'
        
        self.display.console.print(f"\n[green]✓ Switched to {unit_display}[/green]")
        
        # Refresh weather with new unit
        if self.current_city:
            self.fetch_weather(self.current_city)
    
    def refresh_weather(self):
        """Refresh current weather data"""
        if not self.current_city:
            self.display.show_error("No city selected. Please search for a city first.")
            return
        
        self.fetch_weather(self.current_city)
    
    def show_forecast(self):
        """Fetch and display weather forecast"""
        if not self.current_city:
            self.display.show_error("No city selected. Please search for a city first.")
            return
        
        self.display.show_loading(f"Fetching forecast for {self.current_city}...")
        
        try:
            api_units = 'metric' if self.temperature_unit == 'celsius' else 'imperial'
            self.forecast_data = self.api_client.get_forecast(self.current_city, api_units, days=5)
            
            self.display.clear_screen()
            
            # Show current weather first
            if self.current_weather:
                self.display.display_current_weather(self.current_weather, self.temperature_unit)
            
            # Then show forecast
            self.display.display_forecast(self.forecast_data, self.temperature_unit)
            
        except WeatherAPIError as e:
            self.display.show_error(str(e))
        except Exception as e:
            self.display.show_error(f"Unexpected error: {str(e)}")
    
    def exit_app(self):
        """Exit the application gracefully"""
        self.display.console.print("\n[bold cyan]👋 Thank you for using Weather App! Stay safe![/bold cyan]\n")
        sys.exit(0)


def main():
    """Entry point for the application"""
    try:
        app = WeatherApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()