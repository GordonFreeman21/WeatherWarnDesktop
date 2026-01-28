"""
Display module for rendering weather information in the terminal
Uses Rich library for beautiful formatting
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich import box
from datetime import datetime
from typing import Dict, List


class WeatherDisplay:
    """Handler for displaying weather information in terminal"""
    
    # Weather condition to emoji/icon mapping
    WEATHER_ICONS = {
        'Clear': '☀️',
        'Clouds': '☁️',
        'Rain': '🌧️',
        'Drizzle': '🌦️',
        'Thunderstorm': '⛈️',
        'Snow': '❄️',
        'Mist': '🌫️',
        'Fog': '🌫️',
        'Haze': '🌫️',
        'Smoke': '💨',
        'Dust': '💨',
        'Sand': '💨',
        'Ash': '🌋',
        'Squall': '💨',
        'Tornado': '🌪️'
    }
    
    # Weather condition to color mapping
    WEATHER_COLORS = {
        'Clear': 'yellow',
        'Clouds': 'bright_white',
        'Rain': 'blue',
        'Drizzle': 'cyan',
        'Thunderstorm': 'magenta',
        'Snow': 'white',
        'Mist': 'bright_black',
        'Fog': 'bright_black',
        'Haze': 'bright_black'
    }
    
    def __init__(self):
        """Initialize the display with Rich console"""
        self.console = Console()
    
    def show_loading(self, message: str = "Fetching weather data..."):
        """
        Display a loading message
        
        Args:
            message: Loading message to display
        """
        self.console.print(f"\n[bold cyan]⏳ {message}[/bold cyan]")
    
    def show_error(self, error_message: str):
        """
        Display an error message
        
        Args:
            error_message: Error message to display
        """
        panel = Panel(
            f"[bold red]❌ {error_message}[/bold red]",
            border_style="red",
            box=box.ROUNDED
        )
        self.console.print("\n", panel)
    
    def display_current_weather(self, weather: Dict, unit: str = 'celsius'):
        """
        Display current weather information
        
        Args:
            weather: Weather data dictionary
            unit: Temperature unit ('celsius' or 'fahrenheit')
        """
        # Determine unit symbol
        unit_symbol = '°C' if unit == 'celsius' else '°F'
        
        # Get weather icon and color
        icon = self.WEATHER_ICONS.get(weather['main'], '🌡️')
        color = self.WEATHER_COLORS.get(weather['main'], 'white')
        
        # Create header
        header = Text()
        header.append(f"{icon} ", style=f"bold {color}")
        header.append(f"{weather['city']}, {weather['country']}", style="bold cyan")
        
        # Create main temperature display
        temp_display = Text()
        temp_display.append(f"{weather['temperature']}{unit_symbol}", style=f"bold {color} on black")
        
        # Build weather information table
        info_table = Table(show_header=False, box=None, padding=(0, 2))
        info_table.add_column(style="cyan", width=20)
        info_table.add_column(style="white")
        
        info_table.add_row("Weather:", weather['description'])
        info_table.add_row("Feels Like:", f"{weather['feels_like']}{unit_symbol}")
        info_table.add_row("Min/Max:", f"{weather['temp_min']}{unit_symbol} / {weather['temp_max']}{unit_symbol}")
        info_table.add_row("Humidity:", f"{weather['humidity']}%")
        info_table.add_row("Wind Speed:", f"{weather['wind_speed']} m/s")
        info_table.add_row("Pressure:", f"{weather['pressure']} hPa")
        info_table.add_row("Visibility:", f"{weather['visibility']:.1f} km")
        info_table.add_row("Clouds:", f"{weather['clouds']}%")
        
        # Format sunrise/sunset times
        sunrise = weather['sunrise'].strftime('%H:%M')
        sunset = weather['sunset'].strftime('%H:%M')
        info_table.add_row("Sunrise:", f"🌅 {sunrise}")
        info_table.add_row("Sunset:", f"🌇 {sunset}")
        
        # Last updated
        updated = weather['timestamp'].strftime('%Y-%m-%d %H:%M:%S UTC')
        info_table.add_row("Updated:", updated)
        
        # Create the main panel
        content = Text()
        content.append(f"\n{temp_display}\n\n", justify="center")
        
        panel = Panel(
            content,
            title=header,
            subtitle=f"[dim]{updated}[/dim]",
            border_style=color,
            box=box.DOUBLE
        )
        
        # Display everything
        self.console.print("\n")
        self.console.print(panel, justify="center")
        self.console.print(info_table)
    
    def display_forecast(self, forecast: List[Dict], unit: str = 'celsius'):
        """
        Display weather forecast
        
        Args:
            forecast: List of forecast data dictionaries
            unit: Temperature unit ('celsius' or 'fahrenheit')
        """
        unit_symbol = '°C' if unit == 'celsius' else '°F'
        
        # Create forecast table
        table = Table(
            title="[bold cyan]📅 Weather Forecast[/bold cyan]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("Date", style="cyan", width=12)
        table.add_column("Weather", width=15)
        table.add_column("High/Low", justify="center", width=15)
        table.add_column("Humidity", justify="center", width=10)
        table.add_column("Wind", justify="center", width=10)
        
        for day in forecast:
            icon = self.WEATHER_ICONS.get(day['main'], '🌡️')
            date_str = day['date'].strftime('%a, %b %d')
            
            table.add_row(
                date_str,
                f"{icon} {day['description']}",
                f"{day['temp_max']}{unit_symbol} / {day['temp_min']}{unit_symbol}",
                f"{day['humidity']}%",
                f"{day['wind_speed']} m/s"
            )
        
        self.console.print("\n", table)
    
    def display_welcome(self):
        """Display welcome banner"""
        welcome = Text()
        welcome.append("\n🌤️  ", style="bold yellow")
        welcome.append("Weather Application", style="bold cyan")
        welcome.append("  🌤️\n", style="bold yellow")
        
        panel = Panel(
            welcome,
            border_style="cyan",
            box=box.DOUBLE
        )
        
        self.console.print(panel)
    
    def display_menu(self):
        """Display main menu options"""
        menu = Table(show_header=False, box=None, padding=(0, 2))
        menu.add_column(style="cyan", width=30)
        
        menu.add_row("[1] Search for a city")
        menu.add_row("[2] Toggle temperature unit (°C/°F)")
        menu.add_row("[3] Refresh current weather")
        menu.add_row("[4] View forecast")
        menu.add_row("[5] Exit")
        
        self.console.print("\n")
        self.console.print(menu)
    
    def get_input(self, prompt: str) -> str:
        """
        Get user input with custom prompt
        
        Args:
            prompt: Prompt message
            
        Returns:
            User input string
        """
        return self.console.input(f"\n[bold green]{prompt}[/bold green] ")
    
    def clear_screen(self):
        """Clear the terminal screen"""
        self.console.clear()