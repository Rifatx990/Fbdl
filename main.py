from flask import Flask, request, send_file, jsonify
import os
import uuid
import subprocess
import threading
import time

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def delete_file_after_delay(filepath, delay=600):
    def delete():
        time.sleep(delay)
        if os.path.exists(filepath):
            os.remove(filepath)
    threading.Thread(target=delete, daemon=True).start()

@app.route("/fbdl", methods=["GET"])
def download_facebook_video():
    link = request.args.get("link")
    if not link or "facebook.com" not in link:
        return jsonify({"error": "Invalid or missing Facebook link"}), 400

    file_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{file_id}.mp4")

    try:
        subprocess.run([
            "yt-dlp", "-o", output_path, link
        ], check=True)

        if not os.path.exists(output_path):
            return jsonify({"error": "Download failed"}), 500

        delete_file_after_delay(output_path)
        return send_file(output_path, as_attachment=True)

    except subprocess.CalledProcessError:
        return jsonify({"error": "Download command failed"}), 500

if __name__ == "__main__":
    app.run(debug=True)
