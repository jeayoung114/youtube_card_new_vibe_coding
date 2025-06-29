from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os

def create_video_from_cards(cards_dir="cards", audio_dir="audio", output_file="card_news_video.mp4", fps=30, duration=None):
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
    video.write_videofile(output_file, fps=fps)
    print(f"[Video] Video saved as {output_file}")

if __name__ == "__main__":
    create_video_from_cards()
