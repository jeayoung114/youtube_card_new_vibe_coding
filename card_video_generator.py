"""
card_video_generator.py: Assembles card images and audio into a final video, adds background music, and handles output naming by topic.
"""
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
import os
import json

def get_music_path_from_json(json_path="music_info.json", default_path="music/bg_music.mp3"):
    """
    Get the background music path from music_info.json, or use the default if not found.

    Args:
        json_path (str): Path to music info JSON.
        default_path (str): Fallback music file path.
    Returns:
        str: Path to background music file.
    """
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            music_path = data.get("music_path")
            if music_path and os.path.exists(music_path):
                print(f"[Video] Using music from music_info.json: {music_path}")
                return music_path
        except Exception as e:
            print(f"[Video] Could not read music_info.json: {e}")
    return default_path

def get_topic_from_json(json_path="card_news_output.json"):
    """
    Extract the topic/keyword from the card news output JSON for use in filenames.

    Args:
        json_path (str): Path to card news output JSON.
    Returns:
        str: Topic/keyword string (sanitized for filenames).
    """
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            topic = data.get("keyword", "topic").replace(' ', '_').replace(':', '').replace('/', '').replace('\\', '').replace('"', '').replace("'", '').replace('.', '').replace(',', '').lower()
            return topic
        except Exception as e:
            print(f"[Video] Could not read topic from {json_path}: {e}")
    return "topic"

def create_video_from_cards(cards_dir="cards", audio_dir="audio", output_file=None, fps=30, duration=None, bg_music_path=None, music_fadeout=2, json_path="card_news_output.json"):
    """
    Create a vertical video from card images and audio, add background music, and save with topic in filename.

    Args:
        cards_dir (str): Directory with card images.
        audio_dir (str): Directory with audio files.
        output_file (str or None): Output video filename (auto if None).
        fps (int): Frames per second.
        duration (float or None): Default duration per card if no audio.
        bg_music_path (str or None): Path to background music file.
        music_fadeout (int): Seconds to fade out music.
        json_path (str): Path to card news output JSON.
    Returns:
        None. (Saves video file)
    """
    # Get topic for output file name
    topic = get_topic_from_json(json_path)
    if output_file is None:
        output_file = f"card_news_video_{topic}.mp4"
    # Get all card images sorted by name
    images = sorted([os.path.join(cards_dir, f) for f in os.listdir(cards_dir) if f.endswith('.png')])
    if not images:
        print("[Video] No card images found in the directory.")
        return
    clips = []
    for idx, img in enumerate(images, 1):
        audio_path = os.path.join(audio_dir, f"card_{idx}.mp3")
        if os.path.exists(audio_path):
            audio = AudioFileClip(audio_path)
            clip = ImageClip(img).set_duration(audio.duration).set_audio(audio)
        else:
            clip = ImageClip(img).set_duration(duration or 2)
        clips.append(clip)
    video = concatenate_videoclips(clips, method="compose")
    # Use music_info.json if available
    if bg_music_path is None:
        bg_music_path = get_music_path_from_json()
    if os.path.exists(bg_music_path):
        print(f"[Video] Adding background music: {bg_music_path}")
        bgm = AudioFileClip(bg_music_path)
        # Always fade out the last N seconds of the video duration
        if video.duration > music_fadeout:
            bgm = bgm.subclip(0, video.duration).audio_fadeout(music_fadeout)
        else:
            bgm = bgm.subclip(0, video.duration)
        bgm = bgm.volumex(0.15)
        narration = video.audio
        if narration:
            # Composite, then fade out the last N seconds of the whole audio
            final_audio = CompositeAudioClip([narration.set_duration(video.duration), bgm])
            final_audio = final_audio.set_duration(video.duration).audio_fadeout(music_fadeout)
        else:
            final_audio = bgm.set_duration(video.duration)
        video = video.set_audio(final_audio)
    else:
        print(f"[Video] WARNING: Background music file '{bg_music_path}' not found. Video will be generated without background music.")
    video.write_videofile(output_file, fps=fps)
    print(f"[Video] Video saved as {output_file}")

def main():
    """
    Command-line interface for generating the final card news video.
    No arguments. Runs video generation if run directly.
    """
    create_video_from_cards()

if __name__ == "__main__":
    main()
