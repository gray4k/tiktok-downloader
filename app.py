from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>TikTok Downloader</title>
</head>
<body>
  <h2>TikTok Downloader</h2>
  <form method="post">
    <textarea name="url" rows="5" cols="60" placeholder="Paste TikTok URLs here (one per line)"></textarea><br><br>
    <button type="submit">Download</button>
  </form>
  <p>{{ message }}</p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    if request.method == "POST":
        urls = request.form["url"].strip().splitlines()
        download_dir = "/mnt/media/learn"
        os.makedirs(download_dir, exist_ok=True)
        for url in urls:
            if url:
                try:
                    subprocess.run(["yt-dlp", "-o", f"{download_dir}/%(title)s.%(ext)s", url], check=True)
                    message += f"✅ Downloaded: {url}<br>"
                except subprocess.CalledProcessError:
                    message += f"❌ Failed: {url}<br>"
    return render_template_string(HTML, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
