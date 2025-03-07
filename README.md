# WTOP - Terminal Weather Dashboard

WTOP is a beautiful, feature-rich terminal-based weather dashboard that displays current conditions and forecasts right in your terminal.

![WTOP screenshot](https://i.imgur.com/your-screenshot-here.png)

## Features

- 🌦️ **Current Conditions**: Temperature, "feels like" temperature, humidity, wind speed and direction
- 🔍 **System Stats**: Humidity, cloud cover, pressure, and visibility with visual gauges
- 🕐 **Hourly Forecast**: 12-hour forecast with temperature, conditions, wind, and precipitation
- 📅 **7-Day Forecast**: Weekly outlook with high/low temperatures and conditions
- 🌐 **Auto-Location**: Automatically detects your location using IP geolocation
- 💾 **Location Memory**: Saves your location for future use
- 🔄 **Live Updates**: Refreshes automatically every 5 seconds
- 🎯 **No API Key Required**: Uses the free Weather.gov API (US locations)
- 🎨 **Beautiful Display**: Rich color coding and Unicode symbols for better visualization

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Zazarothh/wtop.git
   cd wtop
   ```

2. Install dependencies:
   ```bash
   pip install requests
   ```

3. Run WTOP:
   ```bash
   python wtop_v1.0.py
   ```

## Usage

WTOP will automatically detect your location based on your IP address and display weather information. Your location is saved in `~/.wtop_config.json` for future use.

### Command Line Options

- `-h` or `--help`: Display help information

### Configuration

The configuration file is located at `~/.wtop_config.json` and contains:
- City name
- State code
- Latitude
- Longitude

## Mock Mode

By default, WTOP uses the Weather.gov API to fetch real weather data. For testing or development, you can enable mock mode by setting `MOCK_MODE = True` in the script.

## Terminal Support

WTOP uses Unicode box-drawing characters and ANSI color codes. For best results, use a terminal that supports these features, such as:
- iTerm2 (macOS)
- Windows Terminal (Windows)
- GNOME Terminal, Konsole, or Terminator (Linux)

## License

MIT

## Acknowledgments

- Weather data provided by [Weather.gov](https://www.weather.gov/)
- Location data provided by [ipinfo.io](https://ipinfo.io/)