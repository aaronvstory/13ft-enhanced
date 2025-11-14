# 13ft Ladder - Updated Usage Guide

## ⚠️ IMPORTANT: Recent Fixes Applied

**Date:** 2025-11-13
**Issues Fixed:**
1. ✅ Blank page display (JavaScript errors)
2. ✅ Favicon 400 errors
3. ✅ Better error logging
4. ✅ Route handling improvements

## 🚀 How to Use (Updated)

### Method 1: Web Form (Recommended)

1. **Start the server**:
   ```powershell
   cd C:\claude\13ft
   .\start-13ft.ps1
   ```

2. **Open browser** to http://127.0.0.1:5000

3. **Paste the article URL** in the text box:
   ```
   https://beingpax.medium.com/9-crazy-new-mac-apps-you-must-install-today-43a17fc0d4d4
   ```

4. **Click Submit** - The article should display without paywall

### Method 2: Direct URL Append

Navigate directly to:
```
http://127.0.0.1:5000/https://beingpax.medium.com/9-crazy-new-mac-apps-you-must-install-today-43a17fc0d4d4
```

### Method 3: Bookmarklet (⚠️ READ CAREFULLY)

**IMPORTANT:** The bookmarklet must be clicked WHILE YOU'RE ON THE PAYWALLED ARTICLE, not on the 13ft page!

#### Steps:

1. **Go to the paywalled article** first (e.g., Medium article)
2. **Click the bookmarklet** (see creation steps below)
3. **You'll be redirected** to http://127.0.0.1:5000/[article-url]

#### Create the Bookmarklet:

1. **Create a new bookmark** in your browser
2. **Name:** "13ft Bypass"
3. **URL:** Copy this EXACT JavaScript code:
   ```javascript
   javascript:(function(){window.location.href='http://127.0.0.1:5000/'+encodeURIComponent(window.location.href);})();
   ```

#### Using the Bookmarklet:

✅ **CORRECT:**
- Navigate to Medium article
- Click bookmarklet while ON the Medium page
- Gets redirected to 13ft with article displayed

❌ **WRONG:**
- Clicking bookmarklet while on 13ft page itself
- Results in malformed URL: `http://127.0.0.1:5000/http://127.0.0.1:5000/article`

## 🐛 Troubleshooting

### Problem: Blank Page After Submit

**Check browser console** (F12) for errors. The latest fix should prevent JavaScript errors.

**Server logs** will show:
```
Fetching: https://...
Successfully fetched: https://...
```

If you see errors in server logs, the site might be blocking requests.

### Problem: "Invalid URL" Error

Make sure you're including the full URL with `https://` or `http://`

### Problem: Bookmarklet Not Working

**Common mistake:** You're clicking it while on the 13ft page.
- ✅ **Click bookmarklet ONLY when on the paywalled article page**
- ❌ Don't click it while already on http://127.0.0.1:5000

### Problem: Still Getting JavaScript Errors

Some sites may have additional protections. The fix applied:
- Wraps `history.replaceState` in try-catch to prevent CORS errors
- Wraps `history.pushState` in try-catch
- Disables `location.replace` to prevent redirects

If you still see errors, check the browser console and report which site.

## 🔍 Testing the Fix

**Test URL:** https://beingpax.medium.com/9-crazy-new-mac-apps-you-must-install-today-43a17fc0d4d4

**Expected Result:**
- Article loads successfully
- No SecurityError in console
- Article text visible and readable
- Images and formatting preserved

**Check server logs for:**
```
Fetching: https://beingpax.medium.com/...
https://beingpax.medium.com/
Successfully fetched: https://beingpax.medium.com/...
127.0.0.1 - - [timestamp] "POST /article HTTP/1.1" 200 -
```

## 📝 What Changed

### Previous Issue:
```javascript
Uncaught SecurityError: Failed to execute 'replaceState' on 'History'
```

### Fix Applied:
Instead of removing all JavaScript (which broke the page), we now:
1. **Inject protective code** that wraps problematic methods
2. **Catch errors** silently instead of breaking the page
3. **Let most JavaScript run** to preserve page functionality

### Code Changes:
- `portable.py:190-239` - New protection injection method
- `portable.py:283-345` - Improved route handling and logging
- `portable.py:289-292` - Added `.well-known` route handler

## 🎯 Next Steps

1. **Restart the server** to apply fixes:
   ```powershell
   # Press Ctrl+C to stop if running
   .\start-13ft.ps1
   ```

2. **Test with the form method** first (easiest)

3. **If successful**, try the bookmarklet method

4. **Report any remaining issues** with:
   - URL you're trying
   - Browser console errors (F12 → Console tab)
   - Server log output

## 📚 Additional Resources

- **Original README:** `README.md`
- **Bug Fix Details:** `BUGFIX_NOTES.md`
- **Complete Setup:** `SETUP_COMPLETE.md`
- **Launcher Guide:** `LAUNCHER_GUIDE.md`

---

**Last Updated:** 2025-11-13 18:30
**Status:** Ready for testing
