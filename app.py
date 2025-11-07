from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
  <head><title>TikTok Downloader</title></head>
  <body style="font-family:Arial; padding:40px;">
    <h2>TikTok Downloader</h2>
    <form method="post" action="/download">
      <textarea name="urls" rows="5" cols="80" placeholder="Paste TikTok URLs (one per line)"></textarea><br><br>
      <button type="submit">Download</button>
    </form>
  </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/download', methods=['POST'])
def download():
    urls = request.form['urls'].strip().split('\n')
    output_dir = '/downloads'
    os.makedirs(output_dir, exist_ok=True)

    results = []
    for url in urls:
        url = url.strip()
        if url:
            try:
                cmd = ['yt-dlp', '-o', f'{output_dir}/%(title)s.%(ext)s', url]
                subprocess.run(cmd, check=True)
                results.append(f"✅ Downloaded: {url}")
            except subprocess.CalledProcessError:
                results.append(f"❌ Failed: {url}")
    return "<br>".join(results)
