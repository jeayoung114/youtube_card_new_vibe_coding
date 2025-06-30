import requests
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

def download_music(url, output_path):
    """Download music file from a direct URL."""
    print(f"[Music] Attempting to download from: {url}")
    try:
        response = requests.get(url, stream=True, timeout=20)
        print(f"[Music] HTTP status: {response.status_code}")
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"[Music] Downloaded: {output_path}")
        else:
            print(f"[Music] Failed to download from {url}. Status: {response.status_code}")
    except Exception as e:
        print(f"[Music] Exception occurred: {e}")

def generate_card_audio(texts, output_dir="audio", voice_id="JBFqnCBsd6RMkjVDRZzb", model_id="eleven_multilingual_v2"):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    elevenlabs = ElevenLabs(api_key=api_key)
    os.makedirs(output_dir, exist_ok=True)
    for idx, text in enumerate(texts, 1):
        print(f"[Audio] Generating audio for card {idx}...")
        audio = elevenlabs.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            output_format="mp3_44100_128"
        )
        with open(os.path.join(output_dir, f"card_{idx}.mp3"), "wb") as f:
            for chunk in audio:
                f.write(chunk)
        print(f"[Audio] Saved: {output_dir}/card_{idx}.mp3")

def main():
    # Example usage
    texts = [
        "This is a sample card news summary.",
        "Another impactful sentence for card news.",
        "Keep it short and punchy!"
    ]
    generate_card_audio(texts)
    # Example: Download a music file (replace with a real direct MP3 URL)
    music_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"  # Replace with your chosen music URL
    download_music(music_url, "bg_music.mp3")

if __name__ == "__main__":
    main()
