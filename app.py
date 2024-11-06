from flask import Flask, render_template, request, jsonify, send_file
from podcastfy.client import generate_podcast
import os
from dotenv import load_dotenv
import tempfile
import shutil

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect data from the form
        urls = request.form.get('urls').split(',')
        podcast_name = request.form.get('podcast_name')
        podcast_tagline = request.form.get('podcast_tagline')
        user_instructions = request.form.get('user_instructions')
        tts_model = request.form.get('tts_model', 'gemini')

        # Get API keys from form
        api_keys = {
            'gemini': request.form.get('gemini_key'),
            'openai': request.form.get('openai_key'),
            'elevenlabs': request.form.get('elevenlabs_key')
        }

        # Temporarily set environment variables for the API keys
        original_env = {}
        for key, value in api_keys.items():
            if value:
                env_key = f"{key.upper()}_API_KEY"
                original_env[env_key] = os.getenv(env_key)
                os.environ[env_key] = value

        try:
            # Set up the configuration dictionary
            conversation_config = {
                'word_count': 800,
                'conversation_style': ['Engaging', 'Fast-paced', 'Enthusiastic', 'Educational'],
                'roles_person1': 'Interviewer',
                'roles_person2': 'Subject matter expert',
                'dialogue_structure': ['Topic Introduction', 'Summary of Key Points', 'Discussions', 'Q&A Session', 'Farewell Messages'],
                'podcast_name': podcast_name,
                'podcast_tagline': podcast_tagline,
                'output_language': 'English',
                'user_instructions': user_instructions,
                'engagement_techniques': ['Rhetorical Questions', 'Personal Testimonials', 'Quotes', 'Anecdotes', 'Analogies', 'Humor'],
                'creativity': 0.7,
                'text_to_speech': {
                    'temp_audio_dir': './data/audio/tmp/',
                    'ending_message': "Thank you for listening to this episode. Don't forget to subscribe to our podcast for more interesting conversations.",
                    'default_tts_model': tts_model,
                    'audio_format': 'mp3'
                }
            }

            # Generate the podcast
            result = generate_podcast(
                urls=urls,
                conversation_config=conversation_config,
                tts_model=tts_model
            )

            # Copy the generated file to a static location
            static_audio_dir = os.path.join(app.static_folder, 'audio')
            os.makedirs(static_audio_dir, exist_ok=True)

            audio_filename = os.path.basename(result)
            static_audio_path = os.path.join(static_audio_dir, audio_filename)
            shutil.copy2(result, static_audio_path)

            return jsonify({
                'details': f"Generated podcast: {audio_filename}",
                'audio_url': f"/static/audio/{audio_filename}"
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 400

        finally:
            # Restore original environment variables
            for key, value in original_env.items():
                if value is None:
                    del os.environ[key]
                else:
                    os.environ[key] = value

    return render_template('index.html')

# Add a route to serve audio files
@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_file(os.path.join(app.static_folder, 'audio', filename))

if __name__ == '__main__':
    app.run(debug=True)