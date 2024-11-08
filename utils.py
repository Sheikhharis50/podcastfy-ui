import os
from typing import Any

from podcastfy.client import generate_podcast


def generate_podcast_from_text(
    text: str,
    tts_model: str = "elevenlabs",
    conversation_config: dict[str, Any] | None = None,
):
    """Generate a podcast from text"""

    transcript_file = generate_podcast(text=text, transcript_only=True)
    result = generate_podcast(
        transcript_file=transcript_file,
        tts_model=tts_model,
        conversation_config=conversation_config,
    )

    return result


def generate_podcast_from_pdf(
    urls: list[str],
    tts_model: str = "elevenlabs",
    conversation_config: dict[str, Any] | None = None,
):
    """Generate a podcast from pdf urls"""

    transcript_file = generate_podcast(urls=urls, transcript_only=True)
    result = generate_podcast(
        transcript_file=transcript_file,
        tts_model=tts_model,
        conversation_config=conversation_config,
    )

    return result


def create_audio_directory(root_dir: str = "static"):
    """Create audio directory if it doesn't exist"""
    import os

    os.makedirs(os.path.join(root_dir, "audio"), exist_ok=True)


def create_audio_file_path(root_dir: str = "static"):
    """Create audio file path"""

    create_audio_directory(root_dir)
    filename = f"podcast_{os.urandom(8).hex()}.mp3"
    return os.path.join(root_dir, filename)


def copy_generated_audio_to_static(audio_file_path: str, root_dir: str = "static"):
    """Copy generated audio file to static directory"""

    import shutil

    static_file_path = create_audio_file_path(root_dir)
    shutil.copy2(audio_file_path, static_file_path)
