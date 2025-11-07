from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>TikTok Downloader</title>
  <style>
    body { font-family: Arial; margin: 40px; background: #f8f9fa; }
    textarea { width: 100%; border-radius: 8px; padding: 10px; border: 1px solid #ccc; }
    button { background-color: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; }
    button:hover { background-color: #0056b3; }
    h2 { color: #333; }
    p { background: white; padding: 10px; border-radius: 6px; }
  </style>
</head>
<body>
  <h2>TikTok Downloader</h2>
  <form method="post">
    <textarea name="url" rows="5" placeholder="Paste TikTok URLs here (one per line)"></textarea><br><br>
    <button type="submit">Download</button>
  </form>
  <p>{{ message|safe }}</p>
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
