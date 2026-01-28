# 🌤️ WeatherWarnDesktop

![WeatherWarn Banner](assets/banner.png)

A sleek, modern Command Line Interface (CLI) application for real-time weather updates and 5-day forecasts. Built with Python and the [Rich](https://github.com/Textualize/rich) library for a beautiful terminal experience.

## ✨ Features

-   **Real-time Weather:** Get current conditions for any city globally.
-   **5-Day Forecast:** Detailed daily forecasts to help you plan ahead.
-   **Beautiful UI:** Interactive and visually appealing terminal interface using `Rich`.
-   **Dual Units:** Seamlessly toggle between Celsius and Fahrenheit.
-   **OpenWeatherMap Integration:** Powered by reliable, high-accuracy weather data.

## 🚀 Getting Started

### Prerequisites

-   Python 3.8 or higher
-   An OpenWeatherMap API Key (Get one for free at [openweathermap.org](https://openweathermap.org/api))

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/gordonfreeman21/WeatherWarnDesktop.git
    cd WeatherWarnDesktop
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **Set up your environment variables:**
    Rename `.env.example` to `.env` and add your OpenWeatherMap API key:
    ```bash
    cp .env.example .env
    ```
    Edit `.env`:
    ```env
    OPENWEATHER_API_KEY=your_api_key_here
    DEFAULT_CITY=London
    TEMPERATURE_UNIT=celsius
    ```

## 🛠️ Usage

Run the application from the project root:

```bash
python3 -m src.main
```

### Interactive Menu

Once launched, use the following options:
-   `1`: Search for a city
-   `2`: Toggle between °C and °F
-   `3`: Refresh current weather
-   `4`: View 5-day forecast
-   `5`: Exit application

## 🏗️ Project Structure

```text
WeatherWarnDesktop/
├── assets/             # Images and banners
├── src/                # Source code
│   ├── api_client.py   # OpenWeatherMap API integration
│   ├── config.py       # Configuration and .env loading
│   ├── main.py         # Application entry point
│   └── weather_display.py # Rich-based UI logic
├── .env.example        # Template for environment variables
├── requirements.txt    # Project dependencies
└── README.md           # You are here!
```

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---
Built with ❤️ by [Gordon Freeman](https://github.com/gordonfreeman21)
