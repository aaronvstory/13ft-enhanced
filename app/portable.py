import flask
import requests
from curl_cffi import requests as curl_requests
import cloudscraper
from flask import request
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time

app = flask.Flask(__name__)

# Multiple user agents for fallback
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.119 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
]

googlebot_headers = {
    "User-Agent": USER_AGENTS[0],
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>13ft Ladder - Enhanced</title>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap" rel="stylesheet" async>
<style>
body{font-family:'Open Sans',sans-serif;background-color:#FFF;margin:0;padding:0;display:flex;justify-content:center;align-items:center;height:90vh;transition:background-color 0.3s,color 0.3s}
h1{font-size:1.5rem;margin-bottom:20px;text-align:center;color:#333}
.subtitle{font-size:0.9rem;color:#666;text-align:center;margin-bottom:20px}
label{display:block;margin-bottom:10px;font-weight:bold}
input[type=text]{padding:10px;margin-bottom:10px;border:1px solid #ccc;border-radius:5px;width:100%;font-size:1rem;box-sizing:border-box}
input[type="submit"]{padding:10px;background-color:#6a0dad;color:#fff;border:none;border-radius:5px;width:100%;text-transform:uppercase;font-weight:600;cursor:pointer;transition:background-color 0.3s ease}
input[type="submit"]:hover{background-color:#4e0875}
.dark-mode-toggle{position:absolute;top:10px;right:10px}
.dark-mode-toggle input{display:none}
.dark-mode-toggle label{cursor:pointer;text-indent:-9999px;width:52px;height:27px;background:grey;display:block;border-radius:100px;position:relative}
.dark-mode-toggle label:after{content:'';position:absolute;top:2px;left:2px;width:23px;height:23px;background:#fff;border-radius:90px;transition:0.3s}
.dark-mode-toggle input:checked+label{background:#6a0dad}
.dark-mode-toggle input:checked+label:after{left:calc(100% - 2px);transform:translateX(-100%)}
@media only screen and (max-width:600px){form{padding:10px}h1{font-size:1.2rem}}
body.dark-mode{background-color:#333;color:#FFF}
body.dark-mode h1{color:#FFF}
body.dark-mode .subtitle{color:#AAA}
body.dark-mode input[type=text]{background-color:#555;border:1px solid #777;color:#FFF}
body.dark-mode input[type="submit"]{background-color:#9b30ff}
body.dark-mode input[type="submit"]:hover{background-color:#7a1bb5}
</style>
</head>
<body>
<div class="dark-mode-toggle">
<input type="checkbox" id="dark-mode-toggle">
<label for="dark-mode-toggle" title="Toggle Dark Mode"></label>
</div>
<form action="/article" method="post">
<h1>13ft Ladder - Enhanced</h1>
<p class="subtitle">✨ Now with Cloudflare bypass using curl_cffi</p>
<label for="link">Link of the website you want to remove paywall for:</label>
<input type="text" id="link" name="link" required autofocus>
<input type="submit" value="Submit">
</form>
<script>
const toggleSwitch=document.getElementById('dark-mode-toggle');
const currentTheme=localStorage.getItem('theme')||(window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light");
if(currentTheme==="dark"){document.body.classList.add("dark-mode");toggleSwitch.checked=true}
toggleSwitch.addEventListener('change',function(){if(this.checked){document.body.classList.add("dark-mode");localStorage.setItem('theme','dark')}else{document.body.classList.remove("dark-mode");localStorage.setItem('theme','light')}})
</script>
</body>
</html>
"""

def add_base_tag(html_content, original_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    parsed_url = urlparse(original_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
    if parsed_url.path and not parsed_url.path.endswith('/'):
        base_url = urljoin(base_url, parsed_url.path.rsplit('/', 1)[0] + '/')
    base_tag = soup.find('base')
    if not base_tag:
        new_base_tag = soup.new_tag('base', href=base_url)
        if soup.head:
            soup.head.insert(0, new_base_tag)
        else:
            head_tag = soup.new_tag('head')
            head_tag.insert(0, new_base_tag)
            soup.insert(0, head_tag)
    return str(soup)

def is_cloudflare_blocked(html_text):
    html_lower = html_text.lower()
    return ("cloudflare" in html_lower and (
        "you have been blocked" in html_lower or
        "attention required" in html_lower or
        "just a moment" in html_lower or
        "cf-wrapper" in html_lower))

def bypass_paywall(url):
    if not url.startswith("http"):
        url = "https://" + url
    print(f"\n🔍 Attempting to bypass paywall for: {url}")

    # Method 1: curl_cffi
    try:
        print("  📡 Method 1: curl_cffi with Chrome impersonation...")
        response = curl_requests.get(url, impersonate="chrome110", timeout=15, allow_redirects=True)
        if response.status_code == 200 and not is_cloudflare_blocked(response.text):
            print("  ✅ SUCCESS with curl_cffi!")
            return add_base_tag(response.text, response.url)
        else:
            print(f"  ⚠️ curl_cffi returned {response.status_code} or Cloudflare block")
    except Exception as e:
        print(f"  ❌ curl_cffi failed: {str(e)[:100]}")

    # Method 2: cloudscraper
    try:
        print("  📡 Method 2: cloudscraper...")
        scraper = cloudscraper.create_scraper(browser={'browser':'chrome','platform':'windows','mobile':False})
        response = scraper.get(url, timeout=15)
        if response.status_code == 200 and not is_cloudflare_blocked(response.text):
            print("  ✅ SUCCESS with cloudscraper!")
            return add_base_tag(response.text, response.url)
        else:
            print(f"  ⚠️ cloudscraper returned {response.status_code} or Cloudflare block")
    except Exception as e:
        print(f"  ❌ cloudscraper failed: {str(e)[:100]}")

    # Method 3: Standard requests
    print("  📡 Method 3: Standard requests with multiple user agents...")
    for i, user_agent in enumerate(USER_AGENTS):
        try:
            headers = googlebot_headers.copy()
            headers["User-Agent"] = user_agent
            print(f"    Trying UA {i+1}/{len(USER_AGENTS)}: {user_agent[:50]}...")
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200 and not is_cloudflare_blocked(response.text):
                print(f"    ✅ SUCCESS with user agent {i+1}!")
                return add_base_tag(response.text, response.url)
            else:
                print(f"    ⚠️ UA {i+1} blocked or failed")
        except Exception as e:
            print(f"    ❌ UA {i+1} error: {str(e)[:50]}")

    raise Exception("All bypass methods failed. Site may have strong anti-bot protection.")

@app.route("/")
def main_page():
    return html

@app.route("/article", methods=["POST"])
def show_article():
    link = flask.request.form["link"]
    try:
        return bypass_paywall(link)
    except Exception as e:
        error_msg = str(e)
        error_html = """<html><head><title>Error</title></head>
<body style="font-family:Arial;padding:20px">
<h1>❌ Bypass Failed</h1>
<p><strong>URL:</strong> """ + link + """</p>
<p><strong>Error:</strong> """ + error_msg + """</p>
<p><a href="/">← Go Back</a></p>
</body></html>"""
        return error_html, 400

@app.route("/", defaults={"path":""})
@app.route("/<path:path>", methods=["GET"])
def get_article(path):
    full_url = request.url
    parts = full_url.split("/", 4)
    if len(parts) >= 5:
        actual_url = "https://" + parts[4].lstrip("/")
        try:
            return bypass_paywall(actual_url)
        except Exception as e:
            return str(e), 400
    else:
        return "Invalid URL", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
