import os
import shutil
from typing import Any

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, send_file
from podcastfy.client import generate_podcast

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text", None)
        urls = list(filter(None, request.form.get("urls", "").split(",")))

        print(f"{text=}")
        print(f"{urls=}")
        print(f"{os.environ.get('ELEVENLABS_API_KEY')=}")
        print(f"{os.environ.get('GEMINI_API_KEY')=}")
        print(f"{os.environ.get('OPENAI_API_KEY')=}")

        payload: dict[str, Any] = {"transcript_only": True}
        if text:
            payload["text"] = text
        if urls:
            payload["urls"] = urls

        try:
            transcript_file = generate_podcast(**payload)
            result = generate_podcast(
                transcript_file=transcript_file,
                tts_model="elevenlabs",
            )

            # Create static/audio directory if it doesn't exist
            os.makedirs(os.path.join(app.static_folder, "audio"), exist_ok=True)

            # Generate a unique filename
            filename = f"podcast_{os.urandom(8).hex()}.mp3"
            static_file_path = os.path.join(app.static_folder, "audio", filename)

            # Copy the generated file to static location
            shutil.copy2(result, static_file_path)

            return jsonify(
                {
                    "audio_url": f"/audio/{filename}",
                    "details": (
                        result.details
                        if hasattr(result, "details")
                        else "Podcast generated successfully"
                    ),
                }
            )

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return render_template("index.html")


# Add a route to serve audio files
@app.route("/audio/<path:filename>")
def serve_audio(filename):
    return send_file(os.path.join(app.static_folder, "audio", filename))


if __name__ == "__main__":
    app.run(debug=True)
