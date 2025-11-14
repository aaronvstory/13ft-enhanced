# 13ft Ladder - Launcher Scripts Guide

## Quick Start

### Option 1: PowerShell Launcher (Recommended)
```powershell
.\start-13ft.ps1
```

### Option 2: Batch File Launcher
```cmd
start-13ft.bat
```

Both launchers will:
1. Activate the virtual environment
2. Start the Flask server on http://127.0.0.1:5000
3. Automatically open your default browser

## Custom Configuration

### Run on a different port:
```powershell
.\start-13ft-custom.ps1 -Port 8080
```

### Run on a different host (e.g., to allow network access):
```powershell
.\start-13ft-custom.ps1 -Host "0.0.0.0" -Port 8080
```

⚠️ **Security Warning**: Using host "0.0.0.0" makes the server accessible from your network. Only use this if you understand the implications.

## Usage

1. **Launch the server** using one of the methods above
2. **Open your browser** to http://127.0.0.1:5000 (opens automatically)
3. **Enter a URL** of a paywalled article you want to read
4. **Click Submit** to bypass the paywall

### Alternative URL Method
You can also append the URL directly to the server address:
```
http://127.0.0.1:5000/https://example.com/article
```

## Creating a Desktop Shortcut

### For PowerShell Launcher:
1. Right-click on your desktop → New → Shortcut
2. Enter location:
   ```
   powershell.exe -ExecutionPolicy Bypass -File "C:\claude\13ft\start-13ft.ps1"
   ```
3. Name it "13ft Ladder"
4. (Optional) Right-click shortcut → Properties → Change Icon

### For Batch Launcher:
1. Right-click on `start-13ft.bat`
2. Select "Create shortcut"
3. Move the shortcut to your desktop

## Browser Bookmarklet

To quickly send any page to 13ft, create a bookmarklet:

1. Create a new bookmark in your browser
2. Name: "13ft-ize"
3. URL:
```javascript
javascript:(function(){window.location.href='http://127.0.0.1:5000/'+encodeURIComponent(window.location.href);})();
```

Click the bookmarklet when on a paywalled article to instantly bypass it.

## Troubleshooting

### Server won't start
- Ensure Python is installed and in PATH
- Check that virtual environment was created properly
- Verify all dependencies are installed

### Port already in use
- Use the custom launcher to specify a different port:
  ```powershell
  .\start-13ft-custom.ps1 -Port 8080
  ```

### Permission errors
- Run PowerShell as Administrator if needed
- Or use the batch file launcher instead

## Stopping the Server

Press `Ctrl+C` in the terminal window to stop the server.

## System Requirements

- Python 3.7+
- Windows with PowerShell 5.0+ (for .ps1 launcher)
- Network connection for fetching articles

## How It Works

13ft pretends to be GoogleBot (Google's web crawler) to access paywalled content. Most websites allow GoogleBot full access to their content for SEO purposes, and 13ft takes advantage of this to bypass paywalls.
