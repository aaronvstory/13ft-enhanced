# 13ft Ladder - Setup Complete! 🎉

## Installation Summary

✅ Repository cloned from: https://github.com/wasi-master/13ft
✅ Virtual environment created
✅ All dependencies installed (Flask, Requests, BeautifulSoup4)
✅ Launcher scripts created
✅ System tested and verified

## Quick Start Guide

### Launch the Server

**Windows PowerShell:**
```powershell
cd C:\claude\13ft
.\start-13ft.ps1
```

**Windows Command Prompt:**
```cmd
cd C:\claude\13ft
start-13ft.bat
```

Both launchers will:
- Activate the virtual environment automatically
- Start the server on http://127.0.0.1:5000
- Open your default browser

### Using 13ft

1. **Enter a URL**: Paste the URL of any paywalled article
2. **Click Submit**: The paywall will be bypassed
3. **Read**: Enjoy the full content!

### Advanced Usage

**Custom Port/Host:**
```powershell
.\start-13ft-custom.ps1 -Port 8080
.\start-13ft-custom.ps1 -Host "0.0.0.0" -Port 8080
```

**Direct URL Access:**
```
http://127.0.0.1:5000/https://example.com/article
```

**Browser Bookmarklet:**
Create a bookmark with this URL to instantly bypass any paywall:
```javascript
javascript:(function(){window.location.href='http://127.0.0.1:5000/'+encodeURIComponent(window.location.href);})();
```

## Files Created

| File | Purpose |
|------|---------|
| `start-13ft.ps1` | PowerShell launcher (default: 127.0.0.1:5000) |
| `start-13ft.bat` | Batch file launcher (default: 127.0.0.1:5000) |
| `start-13ft-custom.ps1` | Custom host/port launcher |
| `test-server.ps1` | Installation verification script |
| `LAUNCHER_GUIDE.md` | Detailed launcher documentation |
| `SETUP_COMPLETE.md` | This file |

## Directory Structure

```
C:\claude\13ft\
├── app/
│   ├── portable.py      # Main Flask application
│   ├── index.html       # Web interface
│   └── requirements.txt # Python dependencies
├── venv/                # Virtual environment
├── start-13ft.ps1       # PowerShell launcher
├── start-13ft.bat       # Batch launcher
├── start-13ft-custom.ps1 # Custom launcher
├── test-server.ps1      # Test script
├── LAUNCHER_GUIDE.md    # Launcher documentation
├── SETUP_COMPLETE.md    # This file
└── README.md            # Original project README

## How It Works

13ft pretends to be GoogleBot (Google's web crawler) when fetching web pages. Since most paywalled sites allow GoogleBot full access for SEO purposes, this bypasses the paywall.

**User-Agent Used:**
```
Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36
(KHTML, like Gecko) Chrome/127.0.6533.119 Mobile Safari/537.36
(compatible; Googlebot/2.1; +http://www.google.com/bot.html)
```

## Supported Sites

13ft works with many paywalled sites including:
- Medium.com
- New York Times
- Washington Post
- Bloomberg
- And many more!

Some sites with stronger anti-bot measures may not work.

## Privacy & Ethics

⚠️ **Important Considerations:**
- This tool is for personal use and research purposes
- Consider supporting content creators you benefit from regularly
- Some sites may block Googlebot user agents
- Use responsibly and respect content creators' rights

## Troubleshooting

### Server won't start
```powershell
# Run the test script
.\test-server.ps1
```

### Port 5000 already in use
```powershell
# Use a different port
.\start-13ft-custom.ps1 -Port 8080
```

### Browser doesn't open automatically
Manually navigate to: http://127.0.0.1:5000

### Site not working
- Some sites may block Googlebot
- Try refreshing the page
- Check if the site has updated their paywall system

## Stopping the Server

Press `Ctrl+C` in the terminal window to stop the server.

## Updating 13ft

To update to the latest version:
```bash
cd C:\claude\13ft
git pull origin main
source venv/Scripts/activate  # or venv\Scripts\activate.bat
pip install -r app/requirements.txt --upgrade
```

## System Requirements

- ✅ Windows 10/11
- ✅ Python 3.7+ (detected and working)
- ✅ PowerShell 5.0+ (for .ps1 launchers)
- ✅ Internet connection

## Need Help?

- **Project README**: See `README.md` for detailed information
- **Launcher Guide**: See `LAUNCHER_GUIDE.md` for launcher options
- **GitHub Issues**: https://github.com/wasi-master/13ft/issues
- **Test Installation**: Run `.\test-server.ps1`

## Next Steps

1. **Test it now**: Run `.\start-13ft.ps1`
2. **Create desktop shortcut**: Follow guide in `LAUNCHER_GUIDE.md`
3. **Add bookmarklet**: For one-click paywall bypass
4. **Explore custom ports**: Use `start-13ft-custom.ps1` if needed

---

**Enjoy reading! 📚**

Setup completed on: 2025-11-13
Location: C:\claude\13ft
