import flask
import requests
from flask import request
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

app = flask.Flask(__name__)

# Multiple user agents to try - some sites block Googlebot
USER_AGENTS = [
    # GoogleBot Desktop
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    # GoogleBot Smartphone
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    # BingBot
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    # Twitterbot (often allowed for social sharing)
    "Twitterbot/1.0",
    # Facebookbot
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    # Regular Chrome (fallback)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
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
    <title>13ft Ladder</title>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap" rel="stylesheet" async>
    <style>
        body {
            font-family: 'Open Sans', sans-serif;
            background-color: #FFF;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 90vh;
            transition: background-color 0.3s, color 0.3s;
        }

        h1 {
            font-size: 1.5rem;
            margin-bottom: 20px;
            text-align: center;
            color: #333;
        }

        label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
        }

        input[type=text] {
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            width: 100%;
            font-size: 1rem;
            box-sizing: border-box;
        }

        input[type="submit"] {
            padding: 10px;
            background-color: #6a0dad;
            color: #fff;
            border: none;
            border-radius: 5px;
            width: 100%;
            text-transform: uppercase;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        input[type="submit"]:hover {
            background-color: #4e0875;
        }

        /* Toggle switch styles */
        .dark-mode-toggle {
            position: absolute;
            top: 10px;
            right: 10px;
        }

        .dark-mode-toggle input {
            display: none;
        }

        .dark-mode-toggle label {
            cursor: pointer;
            text-indent: -9999px;
            width: 52px;
            height: 27px;
            background: grey;
            display: block;
            border-radius: 100px;
            position: relative;
        }

        .dark-mode-toggle label:after {
            content: '';
            position: absolute;
            top: 2px;
            left: 2px;
            width: 23px;
            height: 23px;
            background: #fff;
            border-radius: 90px;
            transition: 0.3s;
        }

        .dark-mode-toggle input:checked+label {
            background: #6a0dad;
        }

        .dark-mode-toggle input:checked+label:after {
            left: calc(100% - 2px);
            transform: translateX(-100%);
        }

        /* Responsive adjustments */
        @media only screen and (max-width: 600px) {
            form {
                padding: 10px;
            }

            h1 {
                font-size: 1.2rem;
            }
        }

        /* Dark mode styles */
        body.dark-mode {
            background-color: #333;
            color: #FFF;
        }

        body.dark-mode h1 {
            color: #FFF;
        }

        body.dark-mode input[type=text] {
            background-color: #555;
            border: 1px solid #777;
            color: #FFF;
        }

        body.dark-mode input[type="submit"] {
            background-color: #9b30ff;
        }

        body.dark-mode input[type="submit"]:hover {
            background-color: #7a1bb5;
        }
    </style>
</head>

<body>
    <div class="dark-mode-toggle">
        <input type="checkbox" id="dark-mode-toggle">
        <label for="dark-mode-toggle" title="Toggle Dark Mode"></label>
    </div>
    <form action="/article" method="post">
        <h1>Enter Website Link</h1>
        <label for="link">Link of the website you want to remove paywall for:</label>
        <input type="text" id="link" name="link" required autofocus>
        <input type="submit" value="Submit">
    </form>

    <script>
        const toggleSwitch = document.getElementById('dark-mode-toggle');
        const currentTheme = localStorage.getItem('theme') || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");

        if (currentTheme === "dark") {
            document.body.classList.add("dark-mode");
            toggleSwitch.checked = true;
        }

        toggleSwitch.addEventListener('change', function () {
            if (this.checked) {
                document.body.classList.add("dark-mode");
                localStorage.setItem('theme', 'dark');
            } else {
                document.body.classList.remove("dark-mode");
                localStorage.setItem('theme', 'light');
            }
        });
    </script>
</body>

</html>
"""

def sanitize_html(html_content):
    """
    Inject protective JavaScript to prevent CORS/security errors
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create a script that overrides problematic methods to prevent errors
    protection_script = soup.new_tag('script')
    protection_script.string = """
    (function() {
        // Prevent history manipulation errors
        var originalPushState = history.pushState;
        var originalReplaceState = history.replaceState;

        history.pushState = function() {
            try {
                return originalPushState.apply(history, arguments);
            } catch(e) {
                console.log('History pushState blocked for CORS safety');
            }
        };

        history.replaceState = function() {
            try {
                return originalReplaceState.apply(history, arguments);
            } catch(e) {
                console.log('History replaceState blocked for CORS safety');
            }
        };

        // Prevent location changes that would break the proxy
        var originalLocationReplace = window.location.replace;
        Object.defineProperty(window.location, 'replace', {
            value: function() {
                console.log('Location replace blocked for CORS safety');
            },
            writable: false
        });
    })();
    """

    # Insert protection script at the very beginning of head
    if soup.head:
        soup.head.insert(0, protection_script)
    else:
        head_tag = soup.new_tag('head')
        head_tag.insert(0, protection_script)
        soup.insert(0, head_tag)

    return soup

def add_base_tag(html_content, original_url):
    soup = sanitize_html(html_content)
    parsed_url = urlparse(original_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"

    # Handle paths that are not root, e.g., "https://x.com/some/path/w.html"
    if parsed_url.path and not parsed_url.path.endswith('/'):
        base_url = urljoin(base_url, parsed_url.path.rsplit('/', 1)[0] + '/')
    base_tag = soup.find('base')

    print(base_url)
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
    """Check if response is a Cloudflare block page"""
    return ("cloudflare" in html_text.lower() and
            ("you have been blocked" in html_text.lower() or
             "attention required" in html_text.lower() or
             "cf-wrapper" in html_text.lower()))

def bypass_paywall(url):
    """
    Bypass paywall for a given url - tries multiple user agents if blocked
    """
    if url.startswith("http"):
        # Try each user agent in sequence
        for i, user_agent in enumerate(USER_AGENTS):
            headers = googlebot_headers.copy()
            headers["User-Agent"] = user_agent

            try:
                print(f"Trying user agent {i+1}/{len(USER_AGENTS)}: {user_agent[:50]}...")
                response = requests.get(url, headers=headers, timeout=10)
                response.encoding = response.apparent_encoding

                # Check if Cloudflare blocked us
                if is_cloudflare_blocked(response.text):
                    print(f"  ❌ Blocked by Cloudflare")
                    if i < len(USER_AGENTS) - 1:
                        continue  # Try next user agent
                    else:
                        print("  ⚠️  All user agents blocked - returning last response")
                        return add_base_tag(response.text, response.url)
                else:
                    print(f"  ✓ Success with user agent {i+1}")
                    return add_base_tag(response.text, response.url)
            except requests.exceptions.Timeout:
                print(f"  ⏱️  Timeout")
                if i < len(USER_AGENTS) - 1:
                    continue
                else:
                    raise
            except requests.exceptions.RequestException as e:
                if i < len(USER_AGENTS) - 1:
                    print(f"  ❌ Error: {e}")
                    continue
                else:
                    raise

    try:
        return bypass_paywall("https://" + url)
    except requests.exceptions.RequestException as e:
        return bypass_paywall("http://" + url)


@app.route("/")
def main_page():
    return html


@app.route("/favicon.ico")
def favicon():
    # Return empty response for favicon to prevent 400 errors
    return "", 204


@app.route("/.well-known/<path:subpath>")
def well_known(subpath):
    # Return empty response for .well-known requests
    return "", 204


@app.route("/article", methods=["POST", "GET"])
def show_article():
    if request.method == "POST":
        link = request.form.get("link", "")
    else:
        # Handle GET requests (shouldn't normally happen)
        return "Invalid request method. Use POST or append URL to path.", 400

    if not link:
        return "No URL provided", 400

    try:
        print(f"Fetching: {link}")
        result = bypass_paywall(link)
        print(f"Successfully fetched: {link}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {link}: {str(e)}")
        return f"Error fetching article: {str(e)}", 400
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return f"Unexpected error: {str(e)}", 500


@app.route("/<path:path>", methods=["GET"])
def get_article(path):
    # Handle direct URL appending: http://127.0.0.1:5000/https://example.com
    full_url = request.url
    parts = full_url.split("/", 3)

    if len(parts) >= 4:
        # Extract the actual URL (everything after the server address)
        actual_url = parts[3]

        # If it doesn't start with http, assume https
        if not actual_url.startswith("http"):
            actual_url = "https://" + actual_url

        try:
            print(f"Fetching via path: {actual_url}")
            result = bypass_paywall(actual_url)
            print(f"Successfully fetched via path: {actual_url}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {actual_url}: {str(e)}")
            return f"Error fetching article: {str(e)}", 400
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return f"Unexpected error: {str(e)}", 500
    else:
        return "Invalid URL format. Append the full URL after the server address.", 400


app.run(host="0.0.0.0", port=5000, debug=False)
