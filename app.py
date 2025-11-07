from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_DIR = "/mnt/media/learn"

@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        ydl_opts = {
            "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
            "format": "mp4",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return jsonify({"status": "success", "title": info.get("title")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "✅ TikTok Downloader is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
