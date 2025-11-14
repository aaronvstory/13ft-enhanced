# Quick Restart and Test Instructions

## 🔄 Restart the Server

If the server is currently running, press **Ctrl+C** to stop it.

Then restart:
```powershell
cd C:\claude\13ft
.\start-13ft.ps1
```

## ✅ Test These Changes

### Key Improvements Made:

1. **JavaScript Protection** - No longer removes JavaScript, instead wraps problematic methods to prevent errors
2. **Better Logging** - Server now prints "Fetching:" and "Successfully fetched:" messages
3. **Route Fixes** - Proper handling of `.well-known`, `favicon.ico`, and URL paths
4. **Error Messages** - Clearer error messages when something goes wrong

### What to Look For:

**In Server Console:**
```
Fetching: https://beingpax.medium.com/...
https://beingpax.medium.com/
Successfully fetched: https://beingpax.medium.com/...
127.0.0.1 - - [timestamp] "POST /article HTTP/1.1" 200 -
```

**In Browser:**
- Article content should be visible
- Check console (F12) - should see "History X blocked for CORS safety" (this is expected and harmless)
- No SecurityError should appear

### Test URL:
```
https://beingpax.medium.com/9-crazy-new-mac-apps-you-must-install-today-43a17fc0d4d4
```

## 📋 What Changed (Technical)

### portable.py Changes:

**Line 190-239:** New `sanitize_html()` function
- Injects protective JavaScript at page start
- Wraps `history.pushState` and `history.replaceState` in try-catch
- Prevents CORS errors without breaking functionality

**Line 283-292:** Route handlers
- `/favicon.ico` → Returns 204 (No Content)
- `/.well-known/<path>` → Returns 204 (No Content)

**Line 295-316:** Improved `/article` route
- Better error handling
- Detailed logging
- Clearer error messages

**Line 319-345:** Improved `/<path:path>` route
- Better URL parsing
- Detailed logging
- Handles bookmarklet URLs correctly

## 🎯 Expected Behavior

### Form Submit Method:
1. Paste URL in form
2. Click Submit
3. Server logs show "Fetching: ..."
4. Article appears (might have some layout differences from original)
5. Server logs show "Successfully fetched: ..."

### Direct URL Method:
1. Navigate to `http://127.0.0.1:5000/https://medium.com/article-url`
2. Same as above

### Bookmarklet Method:
1. Be ON the Medium article page
2. Click bookmarklet
3. Redirects to 13ft proxy
4. Article displays

## ⚠️ Important Notes

### Bookmarklet Usage:
- **MUST be clicked while on the paywalled page**
- Don't click while already on the 13ft page
- That creates a malformed URL like `http://127.0.0.1:5000/http://127.0.0.1:5000/article`

### Console Messages:
These are **EXPECTED and SAFE**:
```
History pushState blocked for CORS safety
History replaceState blocked for CORS safety
```

These indicate the protection is working!

### Some Sites Won't Work:
- Sites with strong anti-bot measures
- Sites that require JavaScript-heavy rendering
- Sites that detect and block proxy access

## 📝 Files Modified

- `app/portable.py` - Core changes
- `UPDATED_USAGE.md` - Usage guide
- `BUGFIX_NOTES.md` - Technical details
- `RESTART_AND_TEST.md` - This file

---

**Ready to test!** Restart the server and try the Medium article.
