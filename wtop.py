#!/usr/bin/env python3
import time
import datetime
import os
import sys
import json
import pathlib
from math import cos, sin, radians

# Auto-install requests if not available
try:
    import requests
except ImportError:
    print("Installing required package: requests")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    except Exception as e:
        print(f"Error installing requests: {e}")
        print("Please manually install the requests package with: pip install requests")
        sys.exit(1)

# Weather.gov API doesn't require an API key
UNITS = "imperial"  # imperial for F, metric for C

# Config file path
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".wtop_config.json")

# Set to False to use real API data
MOCK_MODE = False

# Load location data from config file or geolocate if not found
def load_location():
    # Check if config file exists
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return (
                    config.get('city', 'San Diego'), 
                    config.get('state', 'CA'),
                    config.get('latitude', 32.7153),
                    config.get('longitude', -117.1573)
                )
        except Exception as e:
            print(f"Error loading config: {e}")
    
    # If config doesn't exist or is invalid, geolocate the user
    return geolocate_user()

# Geolocate the user based on their IP address
def geolocate_user():
    if MOCK_MODE:
        # Default location coordinates for San Diego
        return "San Diego", "CA", 32.7153, -117.1573
    
    try:
        # Use a free IP geolocation API
        response = requests.get('https://ipinfo.io/json')
        if response.status_code == 200:
            data = response.json()
            location = data.get('city', 'San Diego')
            state = data.get('region', 'CA')
            
            # Get coordinates if available
            coords = data.get('loc', '32.7153,-117.1573').split(',')
            latitude = float(coords[0])
            longitude = float(coords[1])
            
            # Save location to config file
            save_location(location, state, latitude, longitude)
            return location, state, latitude, longitude
        else:
            # Fallback to default location if API fails
            return "San Diego", "CA", 32.7153, -117.1573
    except Exception as e:
        print(f"Error during geolocation: {e}")
        return "San Diego", "CA", 32.7153, -117.1573

# Save location to config file
def save_location(city, state, latitude, longitude):
    try:
        config = {
            'city': city, 
            'state': state,
            'latitude': latitude,
            'longitude': longitude
        }
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Error saving location: {e}")

# Get user location (city, state, and coordinates)
CITY, STATE, LATITUDE, LONGITUDE = load_location()

# Calculate accurate sunrise and sunset times based on location coordinates
def calculate_sun_times():
    import math
    
    # Use coordinates from geolocation
    lat = LATITUDE
    lon = LONGITUDE
    
    # Get current date
    now = datetime.datetime.now()
    
    # In real mode, we could use a proper astronomical library or API
    # For demo purposes, we're using a simplified calculation
    
    # Get day of year (1-366)
    day_of_year = now.timetuple().tm_yday
    
    # Calculate simplified sunrise based on location and season
    # These are simplified approximations adjusted for latitude
    
    # Base times (useful approximations for continental USA)
    base_sunrise_hour = 6.5  # 6:30 AM average
    base_sunset_hour = 19.5  # 7:30 PM average
    
    # Adjust for season (day of year)
    # Northern hemisphere: earlier sunrise in summer, later in winter
    season_adjustment = math.sin((day_of_year - 80) * (2 * math.pi / 365)) * 1.5
    
    # Adjust for latitude (further from equator = more seasonal variation)
    latitude_factor = abs(lat) / 90  # normalized to 0-1
    latitude_adjustment = latitude_factor * 2 * season_adjustment
    
    # Adjust for longitude within timezone
    # Each timezone is roughly 15 degrees wide
    timezone_center = round(lon / 15) * 15
    longitude_adjustment = (lon - timezone_center) / 15  # hours
    
    # Calculate the final times with all adjustments
    sunrise_hour = base_sunrise_hour - season_adjustment - longitude_adjustment
    sunset_hour = base_sunset_hour + season_adjustment - longitude_adjustment
    
    # Convert to hours and minutes
    sunrise_hour_int = int(sunrise_hour)
    sunrise_minute = int((sunrise_hour - sunrise_hour_int) * 60)
    sunset_hour_int = int(sunset_hour)
    sunset_minute = int((sunset_hour - sunset_hour_int) * 60)
    
    # Ensure values are in valid ranges
    sunrise_hour_int = max(0, min(23, sunrise_hour_int))
    sunrise_minute = max(0, min(59, sunrise_minute))
    sunset_hour_int = max(0, min(23, sunset_hour_int))
    sunset_minute = max(0, min(59, sunset_minute))
    
    # Create datetime objects for sunrise and sunset
    sunrise_time = datetime.datetime(now.year, now.month, now.day, sunrise_hour_int, sunrise_minute)
    sunset_time = datetime.datetime(now.year, now.month, now.day, sunset_hour_int, sunset_minute)
    
    # Convert to timestamps
    sunrise_timestamp = int(sunrise_time.timestamp())
    sunset_timestamp = int(sunset_time.timestamp())
    
    return sunrise_timestamp, sunset_timestamp

# Get sunrise and sunset times
SUNRISE_TIME, SUNSET_TIME = calculate_sun_times()

# Sample weather data for testing
MOCK_WEATHER_DATA = {
    "coord": {"lon": -117.1573, "lat": 32.7153},
    "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
    "base": "stations",
    "main": {
        "temp": 72.5,
        "feels_like": 71.8,
        "temp_min": 65.3,
        "temp_max": 77.2,
        "pressure": 1012,
        "humidity": 60
    },
    "visibility": 10000,
    "wind": {"speed": 8.5, "deg": 270},
    "clouds": {"all": 5},
    "dt": 1614978000,
    "sys": {
        "type": 1,
        "id": 5545,
        "country": "US",
        "sunrise": SUNRISE_TIME,
        "sunset": SUNSET_TIME
    },
    "timezone": -28800,
    "id": 5391811,
    "name": "San Diego",
    "cod": 200
}

# Sample forecast data for testing
MOCK_FORECAST_DATA = {
    "list": [
        {
            "dt_txt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "main": {"temp": 72.5, "humidity": 60},
            "weather": [{"description": "clear sky"}],
            "clouds": {"all": 5},
            "wind": {"speed": 8.5, "deg": 270}
        }
    ] * 8  # Replicate the forecast entry 8 times
}

# Create varied forecasts for more realistic data
MOCK_FORECAST_DATA["list"] = []
temps = [68, 70, 71, 72, 73, 74, 75, 74, 73, 72, 71, 69]  # Temperatures by hour for 12 hours
weather_conditions = [
    {"description": "clear sky", "icon": "01d"},
    {"description": "few clouds", "icon": "02d"},
    {"description": "scattered clouds", "icon": "03d"},
    {"description": "partly cloudy", "icon": "04d"}
]

# Create hourly forecasts with varied data for the next 12 hours
for i in range(12):
    hours_ahead = i  # One forecast per hour
    # Get current time for each refresh
    current_datetime = datetime.datetime.now()
    new_time = current_datetime + datetime.timedelta(hours=hours_ahead)
    temp = temps[i]
    weather_idx = min(3, i % 4)
    
    # Create more variation in the forecast
    forecast = {
        "dt_txt": new_time.strftime("%Y-%m-%d %H:%M:%S"),
        "main": {
            "temp": temp,
            "feels_like": temp - 1.5,
            "humidity": 60 + (i * 2 if i < 6 else (12 - i) * 2)
        },
        "weather": [weather_conditions[weather_idx]],
        "clouds": {"all": 5 + (i * 7) % 30},
        "wind": {"speed": 7 + (i % 3), "deg": (i * 30) % 360},
    }
    
    # Add precipitation for some forecasts
    if i in [3, 7, 10]:
        forecast["rain"] = {"1h": 0.2 * (i % 3 + 1)}
    
    MOCK_FORECAST_DATA["list"].append(forecast)

# Terminal color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"
    WHITE = "\033[37m"
    
# Box drawing characters and static borders for perfect alignment
class Box:
    # Fixed width for all boxes (main console width)
    DEFAULT_WIDTH = 130
    
    # Box characters
    HORIZONTAL = "─"
    VERTICAL = "│"
    TOP_LEFT = "┌"
    TOP_RIGHT = "┐"
    BOTTOM_LEFT = "└"
    BOTTOM_RIGHT = "┘"
    LEFT_T = "├"
    RIGHT_T = "┤"
    TOP_T = "┬"
    BOTTOM_T = "┴"
    CROSS = "┼"
    
    # ===== MAIN BOX BORDERS =====
    # These are exactly DEFAULT_WIDTH characters wide
    SINGLE_TOP = "┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐"
    SINGLE_BOTTOM = "└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘"
    SINGLE_DIVIDER = "├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤"
    
    # ===== FORECAST TABLE BORDERS =====
    # For the split top-level forecast display (hourly | daily)
    # These are exactly DEFAULT_WIDTH characters wide with the split at the right position
    FORECAST_TOP = "┌────────────────────────────────────────────────────────────────────────────────────┬─────────────────────────────────────────┐"
    FORECAST_BOTTOM = "└────────────────────────────────────────────────────────────────────────────────────┴─────────────────────────────────────────┘"
    FORECAST_DIVIDER = "├────────────────────────────────────────────────────────────────────────────────────┬─────────────────────────────────────────┤"
    
    # Fixed column widths for the forecast table
    LEFT_COLUMN_WIDTH = 84  # Width between │ and │ (not including borders)
    RIGHT_COLUMN_WIDTH = 41  # Width between │ and │ (not including borders)
    
    # Fixed constants for padding calculations
    EMPTY_LEFT_COLUMN = "│                                                                                    "
    EMPTY_RIGHT_COLUMN = "                                         │"
    
# For calculating color escape sequence lengths
def strip_color_codes(text):
    """Remove ANSI color codes from a string for accurate length calculation."""
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def draw_hourly_forecast_table(forecasts, box_width):
    """Draw the hourly forecast table with perfect alignment.
    
    Args:
        forecasts: List of forecast data
        box_width: Width of the box to fit the table into
    
    Returns:
        List of lines making up the table
    """
    lines = []
    
    # Header
    header = f"{Colors.BOLD}Hourly Forecast (Next 12 Hours){Colors.RESET}"
    lines.append(draw_box_line(header, box_width))
    
    # Fixed table structure - calculate exact widths for consistent display
    date_width = 6   # Date column width
    time_width = 6   # Time column width
    temp_width = 8   # Temperature column width
    cond_width = 15  # Weather condition column width
    wind_width = 12  # Wind information column width
    precip_width = 5 # Precipitation column width - adjusted for better alignment
    
    # Calculate total table width including internal separators
    table_width = date_width + 1 + time_width + 1 + temp_width + 1 + cond_width + 1 + wind_width + 1 + precip_width
    
    # Calculate needed left margin to center the table
    left_margin = 2  # We want at least 2 spaces from the left border
    
    # Make sure the table will fit inside the box with proper margins
    available_width = box_width - 2  # Total available width inside the box
    
    # Header row with column titles, with consistent left margin
    table_header = f"{' ' * left_margin}{'Date':^{date_width}}│{'Time':^{time_width}}│{'Temp °F':^{temp_width}}│{'Condition':^{cond_width}}│{'Wind':^{wind_width}}│{'Rain':^{precip_width}}"
    
    # Make a proper separator line matching the header columns exactly
    separator = f"{' ' * left_margin}{'─' * date_width}┼{'─' * time_width}┼{'─' * temp_width}┼{'─' * cond_width}┼{'─' * wind_width}┼{'─' * precip_width}"
    
    # Add header and separator to output
    lines.append(draw_box_line(table_header, box_width))
    lines.append(draw_box_line(separator, box_width))
    
    # Process each forecast for the next 12 hours
    for forecast in forecasts[:12]:
        # Extract data
        dt_txt = forecast.get("dt_txt", "")
        date = dt_txt.split(" ")[0].split("-")[2] + "/" + dt_txt.split(" ")[0].split("-")[1]  # Display as DD/MM
        time = dt_txt.split(" ")[1][:5]  # HH:MM
        
        temp = forecast.get("main", {}).get("temp", 0)
        weather = forecast.get("weather", [{}])[0].get("description", "").capitalize()
        if len(weather) > cond_width - 2:
            weather = weather[:cond_width - 5] + "..."
            
        wind_speed = forecast.get("wind", {}).get("speed", 0)
        wind_deg = forecast.get("wind", {}).get("deg", 0)
        wind_dir = get_wind_direction_name(wind_deg)
        wind_arrow = get_wind_direction_arrow(wind_deg)
        
        # Handle 1h precipitation (instead of 3h)
        precip = forecast.get("rain", {}).get("1h", 0) + forecast.get("snow", {}).get("1h", 0)
        # Fallback to 3h data if 1h is not available
        if precip == 0:
            precip = (forecast.get("rain", {}).get("3h", 0) + forecast.get("snow", {}).get("3h", 0)) / 3
        
        # Color coding based on values
        temp_color = Colors.BLUE
        if temp > 85:
            temp_color = Colors.RED
        elif temp > 75:
            temp_color = Colors.YELLOW
        elif temp > 65:
            temp_color = Colors.GREEN
            
        precip_color = Colors.RESET
        if precip > 0.5:
            precip_color = Colors.BLUE
        elif precip > 0.1:
            precip_color = Colors.CYAN
        
        # Create the row - careful with spacing in fixed-width columns
        date_col = f"{date:^{date_width}}"
        time_col = f"{time:^{time_width}}"
        temp_col = f"{temp_color}{temp:^{temp_width}.1f}{Colors.RESET}"
        cond_col = f"{weather:^{cond_width}}"
        wind_col = f"{wind_speed:^4.1f}mph {wind_arrow} {wind_dir:3}"
        # Make precipitation more compact by using less width
        precip_col = f"{precip_color}{precip:^4.1f}{Colors.RESET}"
        
        # Build the complete row with perfect spacing and consistent left margin
        row = f"{' ' * left_margin}{date_col}│{time_col}│{temp_col}│{cond_col}│{wind_col}│{precip_col}"
        lines.append(draw_box_line(row, box_width))
    
    return lines

# Simplified box drawing functions that rely on static borders

def draw_box_line(content, box_type="single"):
    """Draw a line of content in a box with perfect alignment.
    
    Args:
        content: The content to display inside the box line
        box_type: Type of box ('single' or 'forecast')
    
    Returns:
        Perfectly aligned box line with exact width
    """
    content_no_color = strip_color_codes(content)
    
    if box_type == "single":
        # Basic single-column box
        inner_width = Box.DEFAULT_WIDTH - 2  # Width without the borders
        content_width = len(content_no_color)
        padding = inner_width - content_width
        
        if padding < 0:
            # Content is too wide, truncate it
            truncated_length = inner_width - 3  # Allow for "..."
            return f"{Box.VERTICAL}{content[:truncated_length]}...{Box.VERTICAL}"
        
        # Build the final line with exact width
        return f"{Box.VERTICAL}{content}{' ' * padding}{Box.VERTICAL}"
        
    elif box_type == "forecast":
        # Split forecast box with two columns
        if "|" in content:
            # Content contains a column separator
            left_content, right_content = content.split("|", 1)
            
            left_content_no_color = strip_color_codes(left_content)
            right_content_no_color = strip_color_codes(right_content)
            
            # Calculate padding for each column
            left_padding = Box.LEFT_COLUMN_WIDTH - len(left_content_no_color)
            right_padding = Box.RIGHT_COLUMN_WIDTH - len(right_content_no_color)
            
            if left_padding < 0:
                left_content = left_content[:Box.LEFT_COLUMN_WIDTH - 3] + "..."
                left_padding = 0
                
            if right_padding < 0:
                right_content = right_content[:Box.RIGHT_COLUMN_WIDTH - 3] + "..."
                right_padding = 0
            
            # Build the line with exact column widths
            return f"{Box.VERTICAL}{left_content}{' ' * left_padding}{Box.VERTICAL}{right_content}{' ' * right_padding}{Box.VERTICAL}"
        else:
            # Single content centered across both columns
            inner_width = Box.DEFAULT_WIDTH - 2  # Width without the borders
            content_width = len(content_no_color)
            padding = inner_width - content_width
            
            if padding < 0:
                # Content is too wide, truncate it
                truncated_length = inner_width - 3  # Allow for "..."
                return f"{Box.VERTICAL}{content[:truncated_length]}...{Box.VERTICAL}"
            
            # Calculate centering
            left_padding = padding // 2
            right_padding = padding - left_padding
            
            # Build the centered line
            return f"{Box.VERTICAL}{' ' * left_padding}{content}{' ' * right_padding}{Box.VERTICAL}"

def draw_forecast_line(left_content="", right_content=""):
    """Draw a line in the forecast box with content in both columns.
    
    Args:
        left_content: Content for the left column
        right_content: Content for the right column
        
    Returns:
        Formatted line with proper borders and padding
    """
    left_no_color = strip_color_codes(left_content)
    right_no_color = strip_color_codes(right_content)
    
    # Calculate padding for each column
    left_padding = Box.LEFT_COLUMN_WIDTH - len(left_no_color)
    right_padding = Box.RIGHT_COLUMN_WIDTH - len(right_no_color)
    
    if left_padding < 0:
        left_content = left_content[:Box.LEFT_COLUMN_WIDTH - 3] + "..."
        left_padding = 0
        
    if right_padding < 0:
        right_content = right_content[:Box.RIGHT_COLUMN_WIDTH - 3] + "..."
        right_padding = 0
    
    # Build the line with exact column widths
    return f"{Box.VERTICAL}{left_content}{' ' * left_padding}{Box.VERTICAL}{right_content}{' ' * right_padding}{Box.VERTICAL}"


def get_weather_data():
    if MOCK_MODE:
        return MOCK_WEATHER_DATA
    else:
        try:
            # Weather.gov API requires lat/lon coordinates to get the forecast grid
            headers = {
                "User-Agent": "wtop/1.0 (tony.test@example.com)",
                "Accept": "application/json"
            }
            
            # First, get the forecast office and grid coordinates using lat/lon
            url = f"https://api.weather.gov/points/{LATITUDE},{LONGITUDE}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            points_data = response.json()
            
            # Extract the forecast URL from the points response
            forecast_url = points_data["properties"]["forecast"]
            stations_url = points_data["properties"]["observationStations"]
            
            # Get stations data to find the nearest weather station
            stations_response = requests.get(stations_url, headers=headers)
            stations_response.raise_for_status()
            stations_data = stations_response.json()
            
            # Get the first (nearest) station
            if stations_data["features"]:
                station_id = stations_data["features"][0]["properties"]["stationIdentifier"]
                
                # Get the latest observation from this station
                observation_url = f"https://api.weather.gov/stations/{station_id}/observations/latest"
                observation_response = requests.get(observation_url, headers=headers)
                observation_response.raise_for_status()
                observation_data = observation_response.json()
                
                # Get the forecast data
                forecast_response = requests.get(forecast_url, headers=headers)
                forecast_response.raise_for_status()
                forecast_data = forecast_response.json()
                
                # Convert to a format compatible with our existing app
                weather_data = {
                    "coord": {"lon": LONGITUDE, "lat": LATITUDE},
                    "weather": [{
                        "id": 800,  # Default clear sky
                        "main": observation_data["properties"]["textDescription"],
                        "description": observation_data["properties"]["textDescription"],
                        "icon": "01d"  # Default icon
                    }],
                    "base": "stations",
                    "main": {
                        # Convert from C to F if necessary
                        "temp": observation_data["properties"]["temperature"]["value"] * 9/5 + 32 if observation_data["properties"]["temperature"]["value"] is not None else 70,
                        "feels_like": observation_data["properties"]["temperature"]["value"] * 9/5 + 32 if observation_data["properties"]["temperature"]["value"] is not None else 70,
                        "temp_min": observation_data["properties"]["temperature"]["value"] * 9/5 + 32 if observation_data["properties"]["temperature"]["value"] is not None else 65,
                        "temp_max": forecast_data["properties"]["periods"][0]["temperature"] if forecast_data["properties"]["periods"] else 75,
                        "pressure": observation_data["properties"]["barometricPressure"]["value"] / 100 if observation_data["properties"]["barometricPressure"]["value"] is not None else 1013,
                        "humidity": round(observation_data["properties"]["relativeHumidity"]["value"]) if observation_data["properties"]["relativeHumidity"]["value"] is not None else 60
                    },
                    "visibility": observation_data["properties"]["visibility"]["value"] if observation_data["properties"]["visibility"]["value"] is not None else 10000,
                    "wind": {
                        "speed": round(observation_data["properties"]["windSpeed"]["value"] * 2.237) if observation_data["properties"]["windSpeed"]["value"] is not None else 8,  # Convert m/s to mph and round
                        "deg": observation_data["properties"]["windDirection"]["value"] if observation_data["properties"]["windDirection"]["value"] is not None else 270
                    },
                    "clouds": {"all": 10},  # Default value, not directly provided by Weather.gov
                    "dt": int(datetime.datetime.now().timestamp()),
                    "sys": {
                        "type": 1,
                        "id": 5545,
                        "country": "US",
                        "sunrise": SUNRISE_TIME,
                        "sunset": SUNSET_TIME
                    },
                    "timezone": -28800,  # Default Pacific timezone
                    "id": 5391811,
                    "name": CITY,
                    "cod": 200
                }
                return weather_data
            else:
                raise Exception("No weather stations found near the specified location")
        except Exception as e:
            print(f"Error getting weather data: {str(e)}")
            return {"error": str(e)}


def get_forecast_data():
    if MOCK_MODE:
        return MOCK_FORECAST_DATA
    else:
        try:
            # Weather.gov API requires lat/lon coordinates to get the forecast grid
            headers = {
                "User-Agent": "wtop/1.0 (tony.test@example.com)",
                "Accept": "application/json"
            }
            
            # First, get the forecast office and grid coordinates using lat/lon
            url = f"https://api.weather.gov/points/{LATITUDE},{LONGITUDE}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            points_data = response.json()
            
            # Extract the hourly forecast URL from the points response
            if "properties" in points_data and "forecastHourly" in points_data["properties"]:
                hourly_forecast_url = points_data["properties"]["forecastHourly"]
                
                # Get the hourly forecast data
                forecast_response = requests.get(hourly_forecast_url, headers=headers)
                forecast_response.raise_for_status()
                forecast_data = forecast_response.json()
                
                # Convert to a format compatible with our existing app
                formatted_forecast = {"list": []}
                
                for period in forecast_data["properties"]["periods"][:12]:  # Get first 12 hours
                    # Parse the time string
                    start_time = period.get("startTime", "")
                    dt_txt = start_time.replace("T", " ").split("+")[0]
                    
                    # Convert to app's expected format
                    forecast_entry = {
                        "dt_txt": dt_txt,
                        "main": {
                            "temp": period.get("temperature", 70),
                            "feels_like": period.get("temperature", 70) - 1.5,  # Approximate feels like
                            "humidity": round(period.get("relativeHumidity", {}).get("value", 60)) if isinstance(period.get("relativeHumidity", {}), dict) else 60
                        },
                        "weather": [
                            {
                                "description": period.get("shortForecast", "Clear").replace("Chance", "").replace("chance", "").strip(),
                                "icon": "01d"  # Default icon
                            }
                        ],
                        "clouds": {"all": 10},  # Default value
                        "wind": {
                            "speed": round(float(period.get("windSpeed", "5 mph").split(" ")[0])),  # Extract numeric value, convert to float, and round
                            "deg": get_wind_direction_deg(period.get("windDirection", "W"))  # Convert direction to degrees
                        }
                    }
                    
                    # Add precipitation if it's in the forecast
                    if "Showers" in period.get("shortForecast", "") or "Rain" in period.get("shortForecast", ""):
                        forecast_entry["rain"] = {"1h": 0.2}  # Default light rain
                    
                    formatted_forecast["list"].append(forecast_entry)
                
                return formatted_forecast
            else:
                raise Exception("Could not find hourly forecast URL in API response")
        except Exception as e:
            print(f"Error getting forecast data: {str(e)}")
            return {"error": str(e)}


def get_wind_direction_deg(direction):
    """Convert cardinal direction to degrees."""
    direction_map = {
        "N": 0, "NNE": 22.5, "NE": 45, "ENE": 67.5,
        "E": 90, "ESE": 112.5, "SE": 135, "SSE": 157.5,
        "S": 180, "SSW": 202.5, "SW": 225, "WSW": 247.5,
        "W": 270, "WNW": 292.5, "NW": 315, "NNW": 337.5
    }
    return direction_map.get(direction, 270)  # Default to west if not found


def draw_7day_forecast(box_width):
    """Draw the 7-day forecast with perfect box alignment.
    
    Args:
        box_width: Width of the box to fit the forecast into
        
    Returns:
        List of lines making up the forecast display
    """
    lines = []
    
    # Header line
    header = f"{Colors.BOLD}7-Day Forecast{Colors.RESET}"
    lines.append(draw_box_line(header, box_width))
    
    # If we're using the mock API, create some realistic 7-day forecast data
    if MOCK_MODE:
        # Generate sample 7-day forecast data with realistic weather patterns
        daily_forecasts = []
        base_temp = 72
        current_date = datetime.datetime.now()
        
        # Weather conditions to cycle through
        conditions = [
            "Sunny", "Partly Cloudy", "Mostly Cloudy", "Cloudy", 
            "Rain Showers", "Scattered Thunderstorms", "Clear"
        ]
        
        # Generate data for each day
        for i in range(7):
            next_date = current_date + datetime.timedelta(days=i)
            day_name = next_date.strftime("%a")  # Mon, Tue, etc.
            date_str = next_date.strftime("%m/%d")  # MM/DD format
            
            # Create some temperature variation
            temp_variation = ((i % 3) - 1) * 3  # -3, 0, or +3 degree variation
            high_temp = base_temp + temp_variation + (i % 2) * 2
            low_temp = high_temp - 10 - (i % 3)
            
            # Select a condition
            condition = conditions[(i + 2) % len(conditions)]
            
            # Add some precipitation for rainy days
            precip = 0
            if "Rain" in condition or "Thunder" in condition:
                precip = 0.2 * ((i % 3) + 1)
                
            # Calculate an icon based on the condition
            if "Sunny" in condition or "Clear" in condition:
                icon = "☀️"
                color = Colors.YELLOW
            elif "Partly" in condition:
                icon = "⛅"
                color = Colors.CYAN
            elif "Cloud" in condition:
                icon = "☁️"
                color = Colors.WHITE
            elif "Rain" in condition:
                icon = "🌧️"
                color = Colors.BLUE
            elif "Thunder" in condition:
                icon = "⛈️"
                color = Colors.MAGENTA
            else:
                icon = "🌤️"
                color = Colors.WHITE
                
            # Add to daily forecasts
            daily_forecasts.append({
                "day": day_name,
                "date": date_str,
                "high": high_temp,
                "low": low_temp,
                "condition": condition,
                "precip": precip,
                "icon": icon,
                "color": color
            })
    else:
        # In real mode, fetch data from Weather.gov API
        try:
            # Weather.gov API requires lat/lon coordinates
            headers = {
                "User-Agent": "wtop/1.0 (tony.test@example.com)",
                "Accept": "application/json"
            }
            
            # Get the forecast URL from points API
            url = f"https://api.weather.gov/points/{LATITUDE},{LONGITUDE}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            points_data = response.json()
            
            # Extract the forecast URL (this is the 7-day forecast)
            forecast_url = points_data["properties"]["forecast"]
            
            # Get the forecast data
            forecast_response = requests.get(forecast_url, headers=headers)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            # Process the forecast periods (Weather.gov provides 14 periods - 7 days with day/night)
            periods = forecast_data["properties"]["periods"]
            
            # Create daily forecasts by combining day/night periods
            daily_forecasts = []
            
            # Process only daytime periods (even indices in Weather.gov's format)
            for i in range(0, min(14, len(periods)), 2):
                # Get the day period
                day_period = periods[i]
                
                # Try to get the night period if available
                night_period = periods[i+1] if i+1 < len(periods) else None
                
                # Parse the start time to get the date
                start_time = datetime.datetime.fromisoformat(day_period["startTime"].replace("Z", "+00:00"))
                day_name = start_time.strftime("%a")  # Mon, Tue, etc.
                date_str = start_time.strftime("%m/%d")  # MM/DD format
                
                # Get high and low temperatures
                high_temp = day_period["temperature"]
                low_temp = night_period["temperature"] if night_period else high_temp - 10
                
                # Get the weather condition
                condition = day_period["shortForecast"].replace("Chance", "").replace("chance", "").strip()
                
                # Estimate precipitation based on forecast text
                precip = 0
                if "rain" in day_period["detailedForecast"].lower() or "shower" in day_period["detailedForecast"].lower():
                    precip = 0.3
                if "thunder" in day_period["detailedForecast"].lower():
                    precip = 0.5
                
                # Determine icon based on the condition
                if "Sunny" in condition or "Clear" in condition:
                    icon = "☀️"
                    color = Colors.YELLOW
                elif "Partly" in condition:
                    icon = "⛅"
                    color = Colors.CYAN
                elif "Cloud" in condition:
                    icon = "☁️"
                    color = Colors.WHITE
                elif "Rain" in condition:
                    icon = "🌧️"
                    color = Colors.BLUE
                elif "Thunder" in condition:
                    icon = "⛈️"
                    color = Colors.MAGENTA
                else:
                    icon = "🌤️"
                    color = Colors.WHITE
                
                # Add to daily forecasts
                daily_forecasts.append({
                    "day": day_name,
                    "date": date_str,
                    "high": high_temp,
                    "low": low_temp,
                    "condition": condition,
                    "precip": precip,
                    "icon": icon,
                    "color": color
                })
                
                # Only keep 7 days
                if len(daily_forecasts) >= 7:
                    break
                    
        except Exception as e:
            print(f"Error getting 7-day forecast: {str(e)}")
            # Create empty forecast if there's an error
            daily_forecasts = []
    
    # Now draw the forecast table with perfect alignment
    # Format: | Day Date | Icon | High/Low | Condition | Precip |
    
    # Fixed column widths for perfect alignment
    day_width = 8    # Width for day/date
    icon_width = 4   # Width for icon
    temp_width = 10  # Width for high/low temps
    cond_width = 18  # Width for condition
    precip_width = 6 # Width for precipitation
    
    # Calculate left margin to center the table
    total_table_width = day_width + icon_width + temp_width + cond_width + precip_width + 4  # +4 for separators
    left_margin = 2  # Default left margin
    
    # Header row
    header_row = f"{' ' * left_margin}{'Day':^{day_width}}│{'':^{icon_width}}│{'Temp °F':^{temp_width}}│{'Condition':^{cond_width}}│{'Rain':^{precip_width}}"
    
    # Separator line
    separator = f"{' ' * left_margin}{'─' * day_width}┼{'─' * icon_width}┼{'─' * temp_width}┼{'─' * cond_width}┼{'─' * precip_width}"
    
    # Add header and separator to output
    lines.append(draw_box_line(header_row, box_width))
    lines.append(draw_box_line(separator, box_width))
    
    # Add each day's forecast
    for forecast in daily_forecasts:
        # Format high/low with color
        if forecast["high"] > 85:
            high_color = Colors.RED
        elif forecast["high"] > 75:
            high_color = Colors.YELLOW
        elif forecast["high"] > 65:
            high_color = Colors.GREEN
        else:
            high_color = Colors.BLUE
        
        if forecast["low"] > 75:
            low_color = Colors.YELLOW
        elif forecast["low"] > 65:
            low_color = Colors.GREEN
        elif forecast["low"] > 55:
            low_color = Colors.BLUE
        else:
            low_color = Colors.CYAN
        
        temp_display = f"{high_color}{forecast['high']}°{Colors.RESET}/{low_color}{forecast['low']}°{Colors.RESET}"
        
        # Format precipitation with color
        if forecast["precip"] > 0.4:
            precip_color = Colors.BLUE
        elif forecast["precip"] > 0:
            precip_color = Colors.CYAN
        else:
            precip_color = Colors.RESET
        
        precip_display = f"{precip_color}{forecast['precip']:.1f}{Colors.RESET}" if forecast["precip"] > 0 else "0"
        
        # Truncate condition if too long
        condition = forecast["condition"]
        if len(condition) > cond_width - 2:
            condition = condition[:cond_width - 5] + "..."
        
        # Build the row with proper spacing
        day_col = f"{forecast['day']} {forecast['date']}"
        icon_col = forecast["color"] + forecast["icon"] + Colors.RESET
        
        # Construct the full row with exact spacing
        row = f"{' ' * left_margin}{day_col:^{day_width}}│{icon_col:^{icon_width}}│{temp_display:^{temp_width}}│{condition:^{cond_width}}│{precip_display:^{precip_width}}"
        lines.append(draw_box_line(row, box_width))
    
    return lines


def draw_gauge(value, max_value, width=20, title="", unit=""):
    percentage = min(1.0, value / max_value)
    filled_width = int(width * percentage)
    
    # Color based on percentage
    if percentage < 0.3:
        color = Colors.BLUE
    elif percentage < 0.6:
        color = Colors.GREEN
    elif percentage < 0.8:
        color = Colors.YELLOW
    else:
        color = Colors.RED
    
    # Format the gauge with a consistent layout
    gauge = f"{title} [{color}{'█' * filled_width}{Colors.RESET}{' ' * (width - filled_width)}]"
    return gauge


def draw_gauge_bar(value, max_value, width=20, label=None):
    """Draw a gauge bar with consistent coloring based on percentage.
    
    Args:
        value: Current value
        max_value: Maximum value
        width: Width of the bar (inner width, not including brackets)
        label: Optional label to display before the bar
        
    Returns:
        Formatted gauge bar
    """
    percentage = min(1.0, value / max_value)
    filled_width = int(width * percentage)
    
    # Color based on percentage
    if percentage < 0.3:
        color = Colors.BLUE
    elif percentage < 0.6:
        color = Colors.GREEN
    elif percentage < 0.8:
        color = Colors.YELLOW
    else:
        color = Colors.RED
    
    # Make sure filled_width is at least 1 if value > 0
    if value > 0 and filled_width == 0:
        filled_width = 1
    
    # Format gauge bar with consistent width
    bar_display = f"{color}{'█' * filled_width}{Colors.RESET}{' ' * (width - filled_width)}"
    
    # Format the gauge with label and bar
    if label:
        # Calculate consistent spacing
        label_space = 25  # Fixed width for label
        label_padded = label.ljust(label_space)
        bar = f"{label_padded}[{bar_display}]"
    else:
        bar = f"[{bar_display}]"
        
    return bar


def get_wind_direction_name(degrees):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / 22.5) % 16
    return directions[index]


def get_wind_direction_arrow(degrees):
    # Unicode arrows for 8 major directions
    arrows = {
        "N": "↑",
        "NE": "↗",
        "E": "→",
        "SE": "↘",
        "S": "↓",
        "SW": "↙",
        "W": "←",
        "NW": "↖"
    }
    
    # Convert degrees to the closest major direction
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(degrees / 45) % 8
    direction = directions[index]
    
    return arrows[direction]


def draw_temperature_chart(temps, box_width):
    """Draw a more compact temperature chart with consistent formatting.
    
    Args:
        temps: List of (time, temperature) tuples
        box_width: Width of the box to fit the chart into
    
    Returns:
        List of lines making up the chart
    """
    lines = []
    
    # Header line
    header = f"{Colors.BOLD}Temperature Forecast (°F){Colors.RESET}"
    lines.append(draw_box_line(header, box_width))
    
    # Calculate max temperature for scaling - use the max temperature of the day
    max_temp = max(item[1] for item in temps)
    # Round max temperature up to the next even number to make nice 2-degree increments
    max_temp = (max_temp + (2 - max_temp % 2)) if max_temp % 2 != 0 else max_temp
    
    # Determine min temperature - calculate based on 2-degree increments and chart height
    chart_height = 3  # Reduced from 6 to 3 rows for the chart
    min_temp = max_temp - (2 * (chart_height - 1))  # Each row is 2 degrees apart
    
    # Calculate exact space available for the chart
    temp_label_width = 7  # Width for temperature labels on the left
    chart_width = box_width - temp_label_width - 1  # Space for temperature labels and borders
    
    # Use only 6 time periods instead of 12 (every other time period)
    if len(temps) > 6:
        temps = temps[::2]  # Use every other temperature reading
    
    # Calculate column width for each time period
    col_width = max(1, chart_width // len(temps))
    
    # Draw each row of the chart
    for row in range(chart_height):
        # Calculate the temperature at this row using 2-degree increments (no decimal)
        temp_at_row = max_temp - (row * 4)  # Increase the temperature step to 4 degrees
        
        # Print the y-axis label (temperature value with no decimal)
        row_content = f"{temp_at_row:>5} │"
        
        # Draw the bars for each time period
        for i, (time, temp) in enumerate(temps):
            # Determine if the bar should be drawn at this temperature
            if temp >= temp_at_row:
                # Choose color based on temperature
                if temp > 85:
                    color = Colors.RED
                elif temp > 75:
                    color = Colors.YELLOW
                elif temp > 65:
                    color = Colors.GREEN
                else:
                    color = Colors.BLUE
                    
                # Draw the bar segment with proper width
                bar_chars = "█" * col_width
                row_content += color + bar_chars + Colors.RESET
            else:
                row_content += " " * col_width
        
        # Add the row to the lines
        lines.append(draw_box_line(row_content, box_width))
    
    # X-axis with exact length for perfect alignment
    x_axis_start = "       └"
    # Calculate how many horizontal line characters we need to reach the edge
    x_line_width = chart_width - len(x_axis_start)
    # Make sure it's not negative
    x_line_width = max(1, x_line_width)
    # Draw the horizontal line with exact length
    x_axis = x_axis_start + "─" * x_line_width
    lines.append(draw_box_line(x_axis, box_width))
    
    # Time labels under the x-axis with perfect spacing
    time_labels_start = "        "  # Same indentation as x-axis
    label_area_width = chart_width - len(time_labels_start) + 1  # Available space for labels
    
    # Calculate spacing between time labels
    spacing_per_label = label_area_width / len(temps)
    
    # Build time labels string
    time_labels = time_labels_start
    for i, (time, _) in enumerate(temps):
        # Position for this label
        pos = int(i * spacing_per_label)
        
        # For the first label, add it at the start
        if i == 0:
            label_space = int(spacing_per_label)
            time_labels += time.ljust(label_space)
        else:
            # Calculate padding to position this label exactly
            pad_before_label = pos - len(time_labels_start) - sum(len(temps[j][0]) for j in range(i))
            time_labels += " " * max(1, pad_before_label) + time
    
    # Make sure the time labels line doesn't exceed the chart area
    if len(strip_color_codes(time_labels)) > chart_width:
        time_labels = time_labels[:chart_width]
        
    lines.append(draw_box_line(time_labels, box_width))
    
    return lines


def display_wtop():
    """Display the weather dashboard with all components."""
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Get weather and forecast data
    weather_data = get_weather_data()
    forecast_data = get_forecast_data()
    
    # Check for error
    if "error" in weather_data:
        print(f"Error fetching weather data: {weather_data['error']}")
        if "Invalid API key" in str(weather_data["error"]):
            print("Please update the API_KEY in the script with your OpenWeatherMap API key.")
        return
    
    # Use static borders for perfect alignment - no width calculations needed
    # All borders are predefined with exact character counts
    
    # Extract weather data we'll need
    temp = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    humidity = weather_data["main"]["humidity"]
    pressure = weather_data["main"]["pressure"]
    weather_desc = weather_data["weather"][0]["description"].capitalize()
    wind_speed = weather_data["wind"]["speed"]
    wind_deg = weather_data["wind"].get("deg", 0)
    wind_dir = get_wind_direction_name(wind_deg)
    wind_arrow = get_wind_direction_arrow(wind_deg)
    clouds = weather_data.get("clouds", {}).get("all", 0)
    visibility = weather_data.get("visibility", 0) / 1000  # Convert to km
    
    # Get sunrise/sunset times
    if "sys" in weather_data:
        sunrise = datetime.datetime.fromtimestamp(weather_data["sys"]["sunrise"]).strftime("%H:%M")
        sunset = datetime.datetime.fromtimestamp(weather_data["sys"]["sunset"]).strftime("%H:%M")
    else:
        sunrise = "N/A"
        sunset = "N/A"
    
    # Current time 
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Temperature color
    temp_color = Colors.BLUE
    if temp > 85:
        temp_color = Colors.RED
    elif temp > 75:
        temp_color = Colors.YELLOW
    elif temp > 65:
        temp_color = Colors.GREEN
    
    # Weather type for icon selection
    weather_type = weather_data["weather"][0]["description"].lower()
    
    # Title bar with proper centering - using static box width
    title = f"WTOP - Weather Dashboard for {CITY}, {STATE}"
    title_content = f"{Colors.CYAN}{Colors.BOLD}{title}{Colors.RESET}"
    
    # Create centered title with exact padding
    title_no_color = strip_color_codes(title_content)
    title_padding = (Box.DEFAULT_WIDTH - 2 - len(title_no_color)) // 2
    centered_title = ' ' * title_padding + title_content + ' ' * (Box.DEFAULT_WIDTH - 2 - len(title_no_color) - title_padding)
    print(f" {centered_title} ")
    
    # Start the current conditions box with static top border
    print(Box.SINGLE_TOP)
    
    # Format the time
    time_section = f"{Colors.BOLD}Current Time:{Colors.RESET} {current_time}"
    
    # Create the first line with icon, current conditions, and time
    if "clear" in weather_type:
        icon_line = f"{Colors.YELLOW}     \\   /      {Colors.RESET}"
        conditions_text = f"{Colors.BOLD}Current Conditions{Colors.RESET}"
    elif "cloud" in weather_type:
        icon_line = f"{Colors.CYAN}       .--.      {Colors.RESET}"
        conditions_text = f"{Colors.BOLD}Current Conditions{Colors.RESET}"
    elif "rain" in weather_type:
        icon_line = f"{Colors.CYAN}      .-.        {Colors.RESET}"
        conditions_text = f"{Colors.BOLD}Current Conditions{Colors.RESET}"
    else:
        icon_line = ""
        conditions_text = f"{Colors.BOLD}Current Conditions{Colors.RESET}"
    
    # Construct first line content with proper spacing
    first_line = f"{icon_line}{conditions_text}"
    # Add time to the middle of the box
    half_point = (Box.DEFAULT_WIDTH - 2 - len(strip_color_codes(first_line)) - len(strip_color_codes(time_section))) // 2
    first_line_content = f"{first_line}{' ' * half_point}{time_section}"
    print(draw_box_line(first_line_content))
    
    # Temperature line
    if "clear" in weather_type:
        icon_line = f"{Colors.YELLOW}      .-.       {Colors.RESET}"
    elif "cloud" in weather_type:
        icon_line = f"{Colors.CYAN}    .-(    ).    {Colors.RESET}"
    elif "rain" in weather_type:
        icon_line = f"{Colors.CYAN}     (   ).      {Colors.RESET}"
    else:
        icon_line = ""
    
    temp_line = f"{icon_line} {Colors.BOLD}Temperature:{Colors.RESET} {temp_color}{temp:.1f}°F{Colors.RESET} / {temp_color}{(temp-32)*5/9:.1f}°C{Colors.RESET}"
    print(draw_box_line(temp_line))
    
    # Feels like line
    if "clear" in weather_type:
        icon_line = f"{Colors.YELLOW}   ― (   ) ―    {Colors.RESET}"
    elif "cloud" in weather_type:
        icon_line = f"{Colors.CYAN}   (___.__)__)   {Colors.RESET}"
    elif "rain" in weather_type:
        icon_line = f"{Colors.CYAN}    (___(__)     {Colors.RESET}"
    else:
        icon_line = ""
    
    feels_line = f"{icon_line} {Colors.BOLD}Feels Like:{Colors.RESET} {temp_color}{feels_like:.1f}°F{Colors.RESET}"
    print(draw_box_line(feels_line))
    
    # Condition line
    if "clear" in weather_type:
        icon_line = f"{Colors.YELLOW}      `-'       {Colors.RESET}"
    elif "cloud" in weather_type:
        icon_line = f"{Colors.CYAN}                 {Colors.RESET}"
    elif "rain" in weather_type:
        icon_line = f"{Colors.BLUE}    ' ' ' '      {Colors.RESET}"
    else:
        icon_line = ""
    
    condition_line = f"{icon_line} {Colors.BOLD}Condition:{Colors.RESET} {weather_desc}"
    print(draw_box_line(condition_line))
    
    # Wind line
    if "clear" in weather_type:
        icon_line = f"{Colors.YELLOW}     /   \\      {Colors.RESET}"
    elif "cloud" in weather_type:
        icon_line = f"{Colors.WHITE}                 {Colors.RESET}"
    elif "rain" in weather_type:
        icon_line = f"{Colors.BLUE}   ' ' ' '       {Colors.RESET}"
    else:
        icon_line = ""
    
    wind_line = f"{icon_line} {Colors.BOLD}Wind:{Colors.RESET} {wind_speed} mph {wind_dir} {Colors.CYAN}{wind_arrow}{Colors.RESET}"
    print(draw_box_line(wind_line))
    
    # Sun info line
    sun_info = f"{' ' * 20} {Colors.BOLD}Sunrise:{Colors.RESET} {Colors.YELLOW}{sunrise}{Colors.RESET}  {Colors.BOLD}Sunset:{Colors.RESET} {Colors.MAGENTA}{sunset}{Colors.RESET}"
    print(draw_box_line(sun_info))
    
    # System stats header
    system_stats = f"{Colors.BOLD}System Stats:{Colors.RESET}"
    print(draw_box_line(system_stats))
    
    # Normalize values to percentages
    # Pressure: normal range 970-1030 hPa, normalize to percentage scale
    pressure_percentage = min(100, max(0, (pressure - 970) / (1030 - 970) * 100))
    # Visibility: max is usually 10km (10000m), normalize to percentage scale
    visibility_percentage = min(100, (visibility / 10) * 100)
    
    # Fixed bar width for consistency
    gauge_bar_width = 30  # Width of just the bar portion
    
    # Create gauge labels
    humidity_label = f"Humidity ({humidity}%)"
    cloud_label = f"Cloud Cover ({clouds}%)"
    pressure_label = f"Pressure ({pressure} hPa)"
    visibility_label = f"Visibility ({visibility:.1f} km)"
    
    # First row: Humidity gauge
    humidity_gauge = draw_gauge_bar(humidity, 100, gauge_bar_width, humidity_label)
    print(draw_box_line(humidity_gauge))
    
    # Second row: Cloud Cover gauge
    cloud_gauge = draw_gauge_bar(clouds, 100, gauge_bar_width, cloud_label)
    print(draw_box_line(cloud_gauge))
    
    # Third row: Pressure gauge
    pressure_gauge = draw_gauge_bar(pressure_percentage, 100, gauge_bar_width, pressure_label)
    print(draw_box_line(pressure_gauge))
    
    # Fourth row: Visibility gauge
    visibility_gauge = draw_gauge_bar(visibility_percentage, 100, gauge_bar_width, visibility_label)
    print(draw_box_line(visibility_gauge))
    
    # Close the current conditions box
    print(Box.SINGLE_BOTTOM)
    print()  # Add a blank line for visual separation
        
    # Build a completely static forecast box with fixed borders
    print()  # Add a blank line for visual separation
    
    # Static box dimensions for consistency
    box_width = Box.DEFAULT_WIDTH
    left_width = 86  # Fixed width for hourly column
    right_width = 43  # Fixed width for daily column
    
    # These are redundant - remove them since we're using Box constants
    
    # Make these global in the function scope for other calculations
    global left_column_width, right_column_width
    left_column_width = left_width - 1  # -1 for the left border
    right_column_width = right_width - 2  # -2 for middle and right borders
    
    # Draw fixed top border
    print(Box.FORECAST_TOP)
    
    # Draw fixed title row
    title = f"{Colors.BOLD}Weather Forecast{Colors.RESET}"
    # Create exact centered title
    title_no_color = strip_color_codes(title)
    padding = (Box.DEFAULT_WIDTH - 2 - len(title_no_color)) // 2
    title_centered = ' ' * padding + title + ' ' * (Box.DEFAULT_WIDTH - 2 - len(title_no_color) - padding)
    print(f"{Box.VERTICAL}{title_centered}{Box.VERTICAL}")
    
    # Draw fixed division line below title
    print(Box.FORECAST_DIVIDER)
    
    # Draw fixed section headers
    left_header = f"{Colors.BOLD}Hourly Forecast (Next 12 Hours){Colors.RESET}"
    right_header = f"{Colors.BOLD}7-Day Forecast{Colors.RESET}"
    
    # Use the draw_forecast_line function for perfect column alignment
    print(draw_forecast_line(left_header, right_header))
    
    # ------ Step 2: Generate the forecast data ------
    
    # Process forecast data to get hourly forecasts
    if "list" in forecast_data:
        forecasts = forecast_data["list"]  # Get all forecasts
        
        if MOCK_MODE and len(forecasts) < 12:  # Ensure we have 12 hours of data
            # Extend existing forecasts with variations for hourly data
            base_forecast = forecasts[-1].copy()
            for i in range(len(forecasts), 12):
                new_forecast = base_forecast.copy()
                hours_ahead = i  # One forecast per hour
                # Get current time for each refresh
                current_datetime = datetime.datetime.now()
                new_time = current_datetime + datetime.timedelta(hours=hours_ahead)
                new_forecast["dt_txt"] = new_time.strftime("%Y-%m-%d %H:%M:%S")
                
                # Add some variation
                temp_variation = ((i % 3) - 1)  # -1, 0, or 1 degree variation
                new_forecast["main"]["temp"] = base_forecast["main"]["temp"] + temp_variation
                new_forecast["main"]["feels_like"] = base_forecast["main"]["feels_like"] + temp_variation
                new_forecast["main"]["humidity"] = min(100, base_forecast["main"]["humidity"] + (i % 5))
                
                # Add precipitation for some forecasts
                if i % 4 == 0:
                    new_forecast["rain"] = {"1h": 0.2 * ((i % 3) + 1)}
                
                forecasts.append(new_forecast)
    
    # Generate 7-day forecast data
    daily_forecasts = []
    
    if MOCK_MODE:
        # Generate sample forecast data
        base_temp = 72
        current_date = datetime.datetime.now()
        
        conditions = [
            "Sunny", "Partly Cloudy", "Mostly Cloudy", "Cloudy", 
            "Rain Showers", "Scattered Thunderstorms", "Clear"
        ]
        
        for i in range(7):
            next_date = current_date + datetime.timedelta(days=i)
            day_name = next_date.strftime("%a")
            date_str = next_date.strftime("%m/%d")
            
            temp_variation = ((i % 3) - 1) * 3
            high_temp = base_temp + temp_variation + (i % 2) * 2
            low_temp = high_temp - 10 - (i % 3)
            
            condition = conditions[(i + 2) % len(conditions)]
            
            precip = 0
            if "Rain" in condition or "Thunder" in condition:
                precip = 0.2 * ((i % 3) + 1)
                
            if "Sunny" in condition or "Clear" in condition:
                icon = "☀️"
                color = Colors.YELLOW
            elif "Partly" in condition:
                icon = "⛅"
                color = Colors.CYAN
            elif "Cloud" in condition:
                icon = "☁️"
                color = Colors.WHITE
            elif "Rain" in condition:
                icon = "🌧️"
                color = Colors.BLUE
            elif "Thunder" in condition:
                icon = "⛈️"
                color = Colors.MAGENTA
            else:
                icon = "🌤️"
                color = Colors.WHITE
                
            daily_forecasts.append({
                "day": day_name,
                "date": date_str,
                "high": high_temp,
                "low": low_temp,
                "condition": condition,
                "precip": precip,
                "icon": icon,
                "color": color
            })
    else:
        try:
            # Weather.gov API requires lat/lon coordinates
            headers = {
                "User-Agent": "wtop/1.0 (tony.test@example.com)",
                "Accept": "application/json"
            }
            
            # Get the forecast URL from points API
            url = f"https://api.weather.gov/points/{LATITUDE},{LONGITUDE}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            points_data = response.json()
            
            # Extract the forecast URL (this is the 7-day forecast)
            forecast_url = points_data["properties"]["forecast"]
            
            # Get the forecast data
            forecast_response = requests.get(forecast_url, headers=headers)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            # Process the forecast periods (Weather.gov provides 14 periods - 7 days with day/night)
            periods = forecast_data["properties"]["periods"]
            
            # Process only daytime periods (even indices in Weather.gov's format)
            for i in range(0, min(14, len(periods)), 2):
                day_period = periods[i]
                night_period = periods[i+1] if i+1 < len(periods) else None
                
                start_time = datetime.datetime.fromisoformat(day_period["startTime"].replace("Z", "+00:00"))
                day_name = start_time.strftime("%a")
                date_str = start_time.strftime("%m/%d")
                
                high_temp = day_period["temperature"]
                low_temp = night_period["temperature"] if night_period else high_temp - 10
                
                condition = day_period["shortForecast"].replace("Chance", "").replace("chance", "").strip()
                
                precip = 0
                if "rain" in day_period["detailedForecast"].lower() or "shower" in day_period["detailedForecast"].lower():
                    precip = 0.3
                if "thunder" in day_period["detailedForecast"].lower():
                    precip = 0.5
                
                if "Sunny" in condition or "Clear" in condition:
                    icon = "☀️"
                    color = Colors.YELLOW
                elif "Partly" in condition:
                    icon = "⛅"
                    color = Colors.CYAN
                elif "Cloud" in condition:
                    icon = "☁️"
                    color = Colors.WHITE
                elif "Rain" in condition:
                    icon = "🌧️"
                    color = Colors.BLUE
                elif "Thunder" in condition:
                    icon = "⛈️"
                    color = Colors.MAGENTA
                else:
                    icon = "🌤️"
                    color = Colors.WHITE
                
                daily_forecasts.append({
                    "day": day_name,
                    "date": date_str,
                    "high": high_temp,
                    "low": low_temp,
                    "condition": condition,
                    "precip": precip,
                    "icon": icon,
                    "color": color
                })
                
                if len(daily_forecasts) >= 7:
                    break
        except Exception as e:
            print(f"Error getting 7-day forecast: {str(e)}")
    
    # ------ Step 3: Format the data for display ------
    
    # 3.1 Hourly forecast section
    hourly_data = []
    
    # Create hourly header
    date_width = 6      # Date column width
    time_width = 6      # Time column width
    temp_width = 8      # Temperature column width
    cond_width = 12     # Weather condition column width
    wind_width = 10     # Wind information column width
    precip_width = 5    # Precipitation column width
    
    left_margin = 2
    table_formats = f"{' ' * left_margin}{{:^{date_width}}}│{{:^{time_width}}}│{{:^{temp_width}}}│{{:^{cond_width}}}│{{:^{wind_width}}}│{{:^{precip_width}}}"
    
    # Header row
    hourly_data.append(table_formats.format("Date", "Time", "Temp °F", "Condition", "Wind", "Rain"))
    
    # Separator row
    separator_formats = f"{' ' * left_margin}{{:─^{date_width}}}┼{{:─^{time_width}}}┼{{:─^{temp_width}}}┼{{:─^{cond_width}}}┼{{:─^{wind_width}}}┼{{:─^{precip_width}}}"
    hourly_data.append(separator_formats.format("", "", "", "", "", ""))
    
    # Format the hourly forecasts
    for forecast in forecasts[:12]:
        dt_txt = forecast.get("dt_txt", "")
        date = dt_txt.split(" ")[0].split("-")[2] + "/" + dt_txt.split(" ")[0].split("-")[1]  # Display as DD/MM
        time = dt_txt.split(" ")[1][:5]  # HH:MM
        
        temp = forecast.get("main", {}).get("temp", 0)
        weather = forecast.get("weather", [{}])[0].get("description", "").capitalize()
        if len(weather) > cond_width - 2:
            weather = weather[:cond_width - 2]
            
        wind_speed = forecast.get("wind", {}).get("speed", 0)
        wind_deg = forecast.get("wind", {}).get("deg", 0)
        wind_dir = get_wind_direction_name(wind_deg)
        wind_arrow = get_wind_direction_arrow(wind_deg)
        
        # Handle 1h precipitation (instead of 3h)
        precip = forecast.get("rain", {}).get("1h", 0) + forecast.get("snow", {}).get("1h", 0)
        # Fallback to 3h data if 1h is not available
        if precip == 0:
            precip = (forecast.get("rain", {}).get("3h", 0) + forecast.get("snow", {}).get("3h", 0)) / 3
        
        # Color coding based on values
        temp_color = Colors.BLUE
        if temp > 85:
            temp_color = Colors.RED
        elif temp > 75:
            temp_color = Colors.YELLOW
        elif temp > 65:
            temp_color = Colors.GREEN
            
        precip_color = Colors.RESET
        if precip > 0.5:
            precip_color = Colors.BLUE
        elif precip > 0.1:
            precip_color = Colors.CYAN
        
        # Format each value
        temp_formatted = f"{temp_color}{temp:.1f}{Colors.RESET}"
        wind_formatted = f"{wind_speed:.1f}mph {wind_arrow}"
        precip_formatted = f"{precip_color}{precip:.1f}{Colors.RESET}" if precip > 0 else "0"
        
        # Add the row
        hourly_data.append(table_formats.format(date, time, temp_formatted, weather, wind_formatted, precip_formatted))
    
    # 3.2 Daily forecast section
    daily_data = []
    
    # Fixed column widths for daily forecast
    day_width = 6
    icon_width = 3
    temp_width = 8
    cond_width = 10
    rain_width = 5
    
    # Calculate total width of the daily forecast table content
    table_content_width = day_width + icon_width + temp_width + cond_width + rain_width + 4  # +4 for the separator characters
    
    # Center the table in the available space
    daily_margin = (right_column_width - table_content_width) // 2
    daily_margin = max(2, daily_margin)  # Ensure at least 2 spaces of margin
    
    # Format string with centered columns
    daily_formats = f"{' ' * daily_margin}{{:^{day_width}}}│{{:^{icon_width}}}│{{:^{temp_width}}}│{{:^{cond_width}}}│{{:^{rain_width}}}"
    
    # Header row
    daily_data.append(daily_formats.format("Day", "", "Temp °F", "Condition", "Rain"))
    
    # Separator row
    daily_separator = f"{' ' * daily_margin}{{:─^{day_width}}}┼{{:─^{icon_width}}}┼{{:─^{temp_width}}}┼{{:─^{cond_width}}}┼{{:─^{rain_width}}}"
    daily_data.append(daily_separator.format("", "", "", "", ""))
    
    # Format the daily forecasts
    for forecast in daily_forecasts:
        day = forecast['day'][:3]
        
        # Format temperature with color
        if forecast["high"] > 85:
            high_color = Colors.RED
        elif forecast["high"] > 75:
            high_color = Colors.YELLOW
        elif forecast["high"] > 65:
            high_color = Colors.GREEN
        else:
            high_color = Colors.BLUE
        
        if forecast["low"] > 75:
            low_color = Colors.YELLOW
        elif forecast["low"] > 65:
            low_color = Colors.GREEN
        elif forecast["low"] > 55:
            low_color = Colors.BLUE
        else:
            low_color = Colors.CYAN
        
        temp_formatted = f"{high_color}{forecast['high']}°{Colors.RESET}/{low_color}{forecast['low']}°{Colors.RESET}"
        
        # Format precipitation
        if forecast["precip"] > 0.4:
            precip_color = Colors.BLUE
        elif forecast["precip"] > 0:
            precip_color = Colors.CYAN
        else:
            precip_color = Colors.RESET
        
        precip_formatted = f"{precip_color}{forecast['precip']:.1f}{Colors.RESET}" if forecast["precip"] > 0 else "0"
        
        # Format condition
        condition = forecast["condition"]
        if len(condition) > cond_width - 2:
            condition = condition[:cond_width - 2]
        
        # Format icon
        icon = forecast["color"] + forecast["icon"] + Colors.RESET
        
        # Add the row
        daily_data.append(daily_formats.format(day, icon, temp_formatted, condition, precip_formatted))
    
    # ------ Step 4: Combine and display within the fixed border ------
    
    # Determine how many content rows we need
    content_rows = max(len(hourly_data), len(daily_data))
    
    # Pad the shorter columns to match
    while len(hourly_data) < content_rows:
        hourly_data.append(" " * left_column_width)
    while len(daily_data) < content_rows:
        daily_data.append(" " * right_column_width)
    
    # Display content rows inside the fixed border
    # Pre-calculate content row locations
    content_rows = max(len(hourly_data), len(daily_data), 14)  # Ensure at least 14 content rows for aesthetics
    
    # Make sure we have enough data rows
    while len(hourly_data) < content_rows:
        hourly_data.append("")
    while len(daily_data) < content_rows:
        daily_data.append("")
    
    # Process and display each content row with fixed borders
    for i in range(content_rows):
        # Get row data from each column
        left_content = hourly_data[i] if i < len(hourly_data) else ""
        right_content = daily_data[i] if i < len(daily_data) else ""
        
        # Use our specialized function to draw the row with perfect alignment
        print(draw_forecast_line(left_content, right_content))
    
    # Draw the completely static bottom border
    print(Box.FORECAST_BOTTOM)


def main():
    """Main function to run the weather dashboard."""
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        print("WTOP - A terminal-based weather dashboard")
        print("Usage: python wtop.py")
        print(f"\nCurrently displaying weather for: {CITY}, {STATE}")
        print(f"Location coordinates: {LATITUDE}, {LONGITUDE}")
        print("Your location is automatically detected using IP geolocation and saved for future use.")
        print("Location data is stored in: " + CONFIG_FILE)
        print("\nFor real weather data (currently using mock data):")
        print("1. Get an API key from https://openweathermap.org/")
        print("2. Update the API_KEY in the script")
        print("3. Set MOCK_MODE = False in the script")
        print("\nThe dashboard updates automatically every 60 seconds.")
        print("Press Ctrl+C to exit.")
        sys.exit(0)
    
    # Run in a continuous loop, updating every 5 seconds
    try:
        while True:
            # Display the dashboard
            display_wtop()
            
            # Create a simple status message
            exit_msg = "Press Ctrl+C to exit"
            update_msg = "Auto-updating every 5 seconds"
            combined_msg = f"{update_msg} | {exit_msg}"
            
            # Calculate exact centering
            msg_len = len(combined_msg)
            left_padding = (Box.DEFAULT_WIDTH - msg_len) // 2
            right_padding = Box.DEFAULT_WIDTH - msg_len - left_padding
            
            # Print message without a box for simplicity
            print()
            print(' ' * left_padding + combined_msg + ' ' * right_padding)
            
            # Sleep for 5 seconds before refreshing
            time.sleep(5)
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nExiting WTOP dashboard. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()