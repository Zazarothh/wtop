# WTOP v1.0.0 Release Notes

## 🎉 First Stable Release

### Download Options

#### Windows Users (Recommended)
- **[wtop-v1.0.0-windows-x64.exe](./wtop-v1.0.0-windows-x64.exe)** - Standalone executable (11MB)
  - No Python installation required
  - Just download and run!

#### All Platforms
- **[wtop-v1.0.0-source.zip](./wtop-v1.0.0-source.zip)** - Source code
  - Requires Python 3.6+
  - Run with `python wtop.py`

### What's New in v1.0.0

#### ✨ Major Features
- **Smooth Refresh**: Updates every 5 seconds without screen flicker
- **Responsive Design**: Automatically adapts to any terminal size
- **Weather.gov API**: Free, reliable weather data for US locations
- **Auto-Location**: Detects your location via IP geolocation
- **Visual Gauges**: Color-coded bars for humidity, pressure, visibility
- **7-Day Forecast**: With weather emoji icons
- **Hourly Forecast**: Next 12 hours with detailed conditions

#### 🛠️ Technical Improvements
- UTF-8 encoding support for Windows terminals
- Proper error handling and recovery
- Location caching for faster startup
- Minimal CPU usage (<1%)
- Cross-platform compatibility

### System Requirements

#### For Executable (Windows)
- Windows 10 or later
- Terminal with UTF-8 support (Windows Terminal recommended)
- Internet connection
- US location (API limitation)

#### For Python Script
- Python 3.6 or higher
- `requests` library (auto-installs)
- Any OS (Windows, macOS, Linux)

### Installation Instructions

#### Windows Executable
1. Download `wtop-v1.0.0-windows-x64.exe`
2. Double-click to run or run from terminal: `.\wtop-v1.0.0-windows-x64.exe`
3. Enjoy your weather dashboard!

#### Python Script
1. Download and extract `wtop-v1.0.0-source.zip`
2. Navigate to extracted folder
3. Run: `python wtop.py`
4. Dependencies will auto-install on first run

### Known Limitations
- Weather data only available for US locations (Weather.gov API)
- Requires internet connection for data fetching
- Best viewed in terminals 100+ characters wide

### Terminal Recommendations
- **Windows**: Windows Terminal (best), PowerShell 7+
- **macOS**: iTerm2, Terminal.app
- **Linux**: GNOME Terminal, Konsole, Alacritty

### Troubleshooting

If you see garbled characters:
- Windows: Use Windows Terminal or run `chcp 65001` first
- Ensure your terminal supports UTF-8
- Try a different terminal emulator

### File Sizes
- `wtop-v1.0.0-windows-x64.exe`: ~11 MB
- `wtop-v1.0.0-source.zip`: ~15 KB

### Checksums
```
MD5:    [To be calculated after upload]
SHA256: [To be calculated after upload]
```

### What's Next
- International weather support (v2.0)
- Custom themes and colors
- Weather alerts and notifications
- Historical data tracking

### Support
Report issues at: https://github.com/Zazarothh/wtop/issues

---
Built with ❤️ for the terminal