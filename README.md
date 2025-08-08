# WTOP - Terminal Weather Dashboard

A beautiful, responsive terminal-based weather dashboard that displays real-time weather information with smooth automatic updates.

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## Features

- 🌡️ **Real-time Weather Data**: Current conditions from Weather.gov API (US locations)
- 📊 **Visual System Stats**: Humidity, cloud cover, pressure, and visibility with color-coded gauge bars
- 📅 **Hourly Forecast**: Next 12 hours with temperature, conditions, wind, and precipitation
- 🗓️ **7-Day Forecast**: Week-long weather outlook with weather emoji icons
- 🎨 **Color-Coded Display**: Temperature-based colors for intuitive reading
- 🔄 **Smooth Auto-Refresh**: Updates every 5 seconds without screen flicker
- 📐 **Responsive Design**: Automatically adapts to any terminal size
- 📍 **Auto-Location**: Detects your location via IP geolocation
- 💾 **Location Caching**: Saves location for instant subsequent launches
- 🚀 **Zero Configuration**: Works out of the box with automatic dependency installation

## Screenshots

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Current Conditions                      Current Time: 2024-01-01 12:00:00 │
│ Temperature: 72.5°F / 22.5°C                                              │
│ Feels Like: 71.0°F                                                        │
│ Condition: Partly Cloudy                                                  │
│ Wind: 8 mph NW ↖                                                          │
│ Sunrise: 06:45  Sunset: 18:23                                             │
│ System Stats:                                                             │
│ Humidity (65%)      [████████████        ]                                │
│ Cloud Cover (40%)   [████████            ]                                │
│ Pressure (1013 hPa) [████████████████    ]                                │
│ Visibility (10 km)  [████████████████████]                                │
└──────────────────────────────────────────────────────────────────────────┘
```

## Installation

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wtop.git
cd wtop
```

2. Run the dashboard:
```bash
python wtop.py
```

That's it! Dependencies will auto-install on first run.

### Manual Installation

If you prefer to install dependencies manually:
```bash
pip install -r requirements.txt
```

### Requirements

- Python 3.6 or higher
- Terminal with UTF-8 support
- Internet connection (for weather data)
- US location (Weather.gov API limitation)

## Usage

Simply run the script:
```bash
python wtop.py
```

The dashboard will:
1. Auto-detect your location (first run only)
2. Display current weather conditions
3. Show hourly and weekly forecasts
4. Smoothly refresh every 5 seconds

### Keyboard Controls

- `Ctrl+C`: Exit the dashboard gracefully

### Command Line Options

```bash
python wtop.py --help    # Show help and location information
```

## Configuration

Location is automatically saved after first run in `~/.wtop_config.json`:
```json
{
    "city": "San Diego",
    "state": "CA",
    "latitude": 32.7157,
    "longitude": -117.1611
}
```

To change location:
1. Delete the config file: `rm ~/.wtop_config.json`
2. Restart WTOP to auto-detect new location

## Terminal Compatibility

### Recommended Terminals

**Windows:**
- Windows Terminal (best experience)
- PowerShell 7+
- ConEmu

**macOS:**
- iTerm2 (recommended)
- Terminal.app
- Alacritty

**Linux:**
- GNOME Terminal
- Konsole
- Terminator
- Alacritty

### Terminal Settings

For optimal display:
- **Font**: Use a monospace font with Unicode support (e.g., Cascadia Code, Fira Code)
- **Encoding**: UTF-8
- **Width**: Works on any width (optimal: 100+ columns)
- **Colors**: 256-color or true color support

## Features in Detail

### Current Conditions
- Temperature in Fahrenheit and Celsius
- "Feels like" temperature
- Weather description
- Wind speed, direction with arrow indicators
- Sunrise and sunset times

### Visual Gauges
Color-coded progress bars for:
- Humidity (0-100%)
- Cloud cover (0-100%)
- Atmospheric pressure (normalized)
- Visibility (0-10km scale)

### Forecast Tables
**Hourly (12 hours):**
- Date and time
- Color-coded temperature
- Weather conditions
- Wind speed and direction
- Precipitation amount

**Weekly (7 days):**
- Day of week
- Weather emoji icons
- High/low temperatures
- Conditions summary
- Rain probability

## Troubleshooting

### Common Issues

**Garbled characters on Windows:**
- Use Windows Terminal or PowerShell 7+
- Ensure UTF-8 encoding is enabled
- Try: `chcp 65001` before running

**Location not detected:**
- Check internet connection
- Ensure you're in the US (API limitation)
- Manually edit `~/.wtop_config.json`

**API errors:**
- Weather.gov may be temporarily unavailable
- Rate limiting (wait a few minutes)
- Check internet connectivity

**Screen flicker:**
- Update to latest terminal version
- Ensure ANSI escape codes are supported
- Try a different terminal emulator

## Technical Details

- **Weather API**: Weather.gov (National Weather Service) - Free, no key required
- **Location API**: ipinfo.io - Free tier for geolocation
- **Refresh Rate**: 5 seconds (smooth cursor-based refresh)
- **Responsive**: Adapts to terminal width (30-300 columns)
- **Performance**: Minimal CPU usage (<1%)
- **Memory**: ~20MB Python process

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development

```bash
# Run with debug borders
python wtop.py --check-borders

# Watch for changes during development
# (implement your own watch solution)
```

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Weather data: [Weather.gov](https://www.weather.gov/) (National Weather Service)
- IP geolocation: [ipinfo.io](https://ipinfo.io/)
- Inspired by terminal tools like htop, bashtop, and wttr.in

## Author

Built with ❤️ for the terminal