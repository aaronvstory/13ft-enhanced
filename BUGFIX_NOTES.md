# 13ft Ladder - Bug Fix Notes

## Issue: SecurityError with history.replaceState

**Error Message:**
```
Uncaught SecurityError: Failed to execute 'replaceState' on 'History':
A history state object with URL '...' cannot be created in a document
with origin 'http://127.0.0.1:5000'
```

**Root Cause:**
- Fetched HTML contains JavaScript that tries to manipulate browser history
- When served from 127.0.0.1:5000, the script can't manipulate history for the original domain
- This is a CORS/security restriction in modern browsers

## Fix Applied

### 1. Added HTML Sanitization Function

Created `sanitize_html()` function that removes:
- Scripts manipulating `history.replaceState` or `history.pushState`
- Scripts manipulating `window.history`, `location.replace`, or `document.location`
- External tracking/analytics scripts (Google Analytics, Facebook, etc.)
- `<noscript>` tags that can interfere

### 2. Fixed Favicon 400 Errors

Added `/favicon.ico` route to return proper HTTP 204 (No Content) response instead of 400 error.

## Changes Made

**File:** `C:\claude\13ft\app\portable.py`

**Changes:**
1. Added `sanitize_html()` function (lines 190-223)
2. Modified `add_base_tag()` to call `sanitize_html()` first (line 226)
3. Added `/favicon.ico` route handler (lines 267-270)

## Testing

The fix has been applied. To test:

1. **Restart the server** (if already running):
   - Press Ctrl+C to stop
   - Run `.\start-13ft.ps1` again

2. **Test with the same Medium article** that was failing:
   ```
   https://beingpax.medium.com/9-crazy-new-mac-apps-you-must-install-today-43a17fc0d4d4
   ```

3. **Expected behavior:**
   - No SecurityError in browser console
   - Article content should display without JavaScript errors
   - Favicon errors should be gone (204 response instead of 400)

## What Gets Removed

The sanitization removes:
- ✅ History manipulation scripts (the cause of the error)
- ✅ Location redirect scripts
- ✅ Analytics/tracking scripts
- ✅ Ad service scripts
- ✅ Noscript tags

## What Stays Intact

The sanitization preserves:
- ✅ Article content (text, images, formatting)
- ✅ CSS styling
- ✅ Non-problematic JavaScript
- ✅ Media embeds
- ✅ Links and navigation

## Additional Notes

- Some dynamic features may not work (e.g., interactive widgets)
- This is expected behavior - we're prioritizing content readability
- If a site doesn't work at all, it may have stronger anti-bot measures

## Rollback Instructions

If you need to revert the changes:

```bash
cd C:\claude\13ft
git checkout app/portable.py
```

## Date Applied

2025-11-13

---

**Status:** ✅ Fixed and ready for testing
