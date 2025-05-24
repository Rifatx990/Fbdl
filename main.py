from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Facebook Video Info API. Use /fbdl?url=..."})

@app.route('/fbdl', methods=['GET'])
def get_fb_video_info():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forcejson': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        result = {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
            "uploader": info.get("uploader"),
            "direct_url": info.get("url"),
            "formats": info.get("formats")
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
