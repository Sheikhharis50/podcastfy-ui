import click
from dotenv import load_dotenv

from utils import generate_podcast_from_pdf, generate_podcast_from_text

# Load environment variables from .env file
load_dotenv()


@click.command()
@click.option("--text", "-t", required=False, help="Raw text")
@click.option("--urls", "-u", required=False, help="Comma-separated URLs")
def generate(urls: str, text: str):
    """Generate a podcast from URLs using the command line."""

    if not text and not urls:
        click.echo("Please provide either text or URLs.", err=True)
        return

    # Convert comma-separated URLs to list
    url_list = [url.strip() for url in (urls or "").split(",")]
    tts_model = "elevenlabs"

    # Set up the configuration dictionary
    conversation_config = {
        "word_count": 800,
        "conversation_style": ["Engaging", "Fast-paced", "Enthusiastic", "Educational"],
        "roles_person1": "Interviewer",
        "roles_person2": "Subject matter expert",
        "dialogue_structure": [
            "Topic Introduction",
            "Summary of Key Points",
            "Discussions",
            "Q&A Session",
            "Farewell Messages",
        ],
        "output_language": "English",
        "engagement_techniques": [
            "Rhetorical Questions",
            "Personal Testimonials",
            "Quotes",
            "Anecdotes",
            "Analogies",
            "Humor",
        ],
        "creativity": 0.7,
        "text_to_speech": {
            "temp_audio_dir": "./data/audio/tmp/",
            "ending_message": "Thank you for listening to this episode. Don't forget to subscribe to our podcast for more interesting conversations.",
            "default_tts_model": tts_model,
            "audio_format": "mp3",
        },
    }

    try:
        if text:
            result = generate_podcast_from_text(
                text=text,
                tts_model=tts_model,
                conversation_config=conversation_config,
            )
        else:
            result = generate_podcast_from_pdf(
                urls=url_list,
                tts_model=tts_model,
                conversation_config=conversation_config,
            )
        click.echo("Podcast generated successfully!")
        click.echo(result)
    except Exception as e:
        click.echo(f"Error generating podcast: {str(e)}", err=True)


if __name__ == "__main__":
    generate()
