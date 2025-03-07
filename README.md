# WTOP - Terminal Weather Dashboard

WTOP is a beautiful, feature-rich terminal-based weather dashboard that displays current conditions and forecasts right in your terminal.

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
- 📦 **Auto-Dependency Installation**: Automatically installs required dependencies

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Zazarothh/wtop.git
   cd wtop
   ```

2. Run WTOP:
   ```bash
   python wtop.py
   ```

### Dependencies

WTOP has minimal dependencies and will automatically install what it needs:

- **requests**: For API communication - automatically installed if missing
  
The auto-installation uses pip and requires Python's standard library. No manual installation of packages is required.

## Usage

WTOP will automatically detect your location based on your IP address and display weather information. Your location is saved in `~/.wtop_config.json` for future use.

### Command Line Options

- `-h` or `--help`: Display help information and usage
- `--check-borders`: Validate border alignment (for development/debugging)

### Configuration

The configuration file is located at `~/.wtop_config.json` and contains:
- City name
- State code
- Latitude
- Longitude

## Mock Mode and API Usage

WTOP can operate in two modes:

- **Live Mode** (default): Uses the Weather.gov API to fetch real-time weather data
  - No API key required as Weather.gov is a free public service
  - Optimized for US locations with accurate data
  
- **Mock Mode**: Uses built-in sample data for testing and development
  - Enable by setting `MOCK_MODE = True` in the script
  - Great for testing or when internet access is limited
  - Shows realistic data patterns with temperature variations

## Terminal Support

WTOP uses Unicode box-drawing characters and ANSI color codes for its beautiful display. For best results, use a modern terminal that supports these features:

- **Windows**: 
  - Windows Terminal (recommended)
  - PowerShell with modern font
  
- **macOS**:
  - iTerm2 (recommended)
  - Terminal.app
  
- **Linux**:
  - GNOME Terminal
  - Konsole
  - Terminator
  - Alacritty

For optimal display, ensure your terminal:
- Uses a monospace font that includes Unicode box-drawing characters
- Has ANSI color support enabled
- Is set to a width of at least 130 characters

## License

MIT

## Acknowledgments

- **Data Sources**:
  - Weather data provided by [Weather.gov](https://www.weather.gov/)
  - Location data provided by [ipinfo.io](https://ipinfo.io/)
  
- **Libraries**:
  - [requests](https://requests.readthedocs.io/) - For API communication
  
- **Inspiration**:
  - Terminal-based applications like `htop` and `wttr.in`
  - Modern CLI design patterns and Unicode art