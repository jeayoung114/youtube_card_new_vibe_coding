import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

JAMENDO_CLIENT_ID = os.getenv("JAMENDO_CLIENT_ID")
print(f"[DEBUG] JAMENDO_CLIENT_ID: {JAMENDO_CLIENT_ID}")  # Debug print

# Popular Jamendo tags that are known to work
POPULAR_GENRE_TAGS = [
    "pop", "rock", "electronic", "jazz", "classical", "metal", 
    "hiphop", "folk", "blues", "reggae", "funk", "country",
    "soundtrack", "world", "ambient", "lounge"
]

POPULAR_MOOD_TAGS = [
    "happy", "energetic", "calm", "upbeat", "chill", "romantic",
    "dark", "uplifting", "peaceful", "dramatic", "party"
]

# Featured selections recommended by Jamendo API documentation
FEATURED_GENRES = [
    "lounge", "classical", "electronic", "jazz", "pop", 
    "hiphop", "relaxation", "rock", "songwriter", "world", 
    "metal", "soundtrack"
]

def get_working_tags_by_topic(topic):
    """
    Return single working tags (not comma-separated) based on topic.
    Uses only proven Jamendo tags.
    """
    topic = topic.lower()
    
    # Map topics to single, popular tags
    if any(word in topic for word in ["kids", "children", "playful", "funny", "cartoon"]):
        return ["pop", "happy"]  # Children-friendly content
    elif any(word in topic for word in ["tech", "ai", "robot", "future", "startup"]):
        return ["electronic", "upbeat"]  # Tech/corporate content
    elif any(word in topic for word in ["news", "update", "trend", "today"]):
        return ["pop", "upbeat"]  # News content
    elif any(word in topic for word in ["happy", "joy", "smile", "celebrate"]):
        return ["happy", "upbeat"]  # Happy content
    elif any(word in topic for word in ["calm", "relax", "meditation", "peaceful"]):
        return ["calm", "relaxation"]  # Calm content
    elif any(word in topic for word in ["party", "dance", "club", "energetic"]):
        return ["party", "energetic"]  # Party content
    elif any(word in topic for word in ["romantic", "love", "date", "wedding"]):
        return ["romantic", "pop"]  # Romantic content
    else:
        # Default fallback to most popular working tags
        return ["pop", "happy"]

def search_jamendo_tracks_single_tag(tag, limit=10):
    """
    Query Jamendo API for tracks using a single tag.
    Single tags work better than comma-separated ones.
    """
    url = "https://api.jamendo.com/v3.0/tracks/"
    params = {
        "client_id": JAMENDO_CLIENT_ID,
        "format": "json",
        "limit": limit,
        "tags": tag,  # Single tag only
        "audioformat": "mp32",
        "order": "popularity_total",
        "include": "musicinfo",
        "featured": "1"  # Only featured content for better quality
    }
    
    print(f"[DEBUG] Trying tag: '{tag}'")
    response = requests.get(url, params=params)
    print(f"[DEBUG] API status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"[DEBUG] API Error: {response.text}")
        return []
    
    data = response.json()
    print(f"[DEBUG] Results count: {data.get('headers', {}).get('results_count', 0)}")
    
    tracks = []
    for item in data.get("results", []):
        track = {
            "title": item.get("name"),
            "artist": item.get("artist_name"),
            "listen_url": item.get("audio"),
            "download_url": item.get("audiodownload"),
            "duration": item.get("duration"),
            "license": item.get("license_ccurl")
        }
        tracks.append(track)
    return tracks

def search_jamendo_tracks_comprehensive(topic_tags, limit=5):
    """
    Comprehensive search strategy using multiple approaches.
    """
    all_tracks = []
    
    # Strategy 1: Try topic-specific tags
    print("[DEBUG] Strategy 1: Topic-specific tags")
    for tag in topic_tags:
        tracks = search_jamendo_tracks_single_tag(tag, limit)
        if tracks:
            all_tracks.extend(tracks)
            print(f"[SUCCESS] Found {len(tracks)} tracks with tag: {tag}")
            if len(all_tracks) >= limit:
                return all_tracks[:limit]
    
    # Strategy 2: Try featured genres
    if not all_tracks:
        print("[DEBUG] Strategy 2: Featured genres")
        for genre in FEATURED_GENRES[:5]:  # Try first 5 featured genres
            tracks = search_jamendo_tracks_single_tag(genre, limit)
            if tracks:
                all_tracks.extend(tracks)
                print(f"[SUCCESS] Found {len(tracks)} tracks with featured genre: {genre}")
                if len(all_tracks) >= limit:
                    return all_tracks[:limit]
    
    # Strategy 3: Try popular mood tags
    if not all_tracks:
        print("[DEBUG] Strategy 3: Popular mood tags")
        for mood in ["happy", "upbeat", "energetic", "calm"][:3]:
            tracks = search_jamendo_tracks_single_tag(mood, limit)
            if tracks:
                all_tracks.extend(tracks)
                print(f"[SUCCESS] Found {len(tracks)} tracks with mood: {mood}")
                if len(all_tracks) >= limit:
                    return all_tracks[:limit]
    
    # Strategy 4: Try without tags (most popular)
    if not all_tracks:
        print("[DEBUG] Strategy 4: Most popular tracks (no tags)")
        url = "https://api.jamendo.com/v3.0/tracks/"
        params = {
            "client_id": JAMENDO_CLIENT_ID,
            "format": "json",
            "limit": limit,
            "order": "popularity_total",
            "featured": "1",
            "audioformat": "mp32",
            "include": "musicinfo"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("results", []):
                track = {
                    "title": item.get("name"),
                    "artist": item.get("artist_name"),
                    "listen_url": item.get("audio"),
                    "download_url": item.get("audiodownload"),
                    "duration": item.get("duration"),
                    "license": item.get("license_ccurl")
                }
                all_tracks.append(track)
            print(f"[SUCCESS] Found {len(all_tracks)} popular tracks without tags")
    
    return all_tracks[:limit]

def search_jamendo_tracks(tags="", limit=5):
    """
    Updated main search function that handles both old and new calling patterns.
    Accepts either a string (comma-separated) or a list of tags.
    """
    if isinstance(tags, str) and tags:
        # If tags is a string, split it and try each tag individually
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        return search_jamendo_tracks_comprehensive(tag_list, limit)
    elif isinstance(tags, list) and tags:
        return search_jamendo_tracks_comprehensive(tags, limit)
    else:
        # Default search
        return search_jamendo_tracks_comprehensive(["pop", "happy"], limit)

def download_music(url, output_path):
    """
    Download music file from URL.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"[Music] Attempting to download from: {url}")
    try:
        response = requests.get(url, stream=True, timeout=30)
        print(f"[Music] HTTP status: {response.status_code}")
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"[Music] Downloaded: {output_path}")
            return True
        else:
            print(f"[Music] Failed to download from {url}. Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"[Music] Exception occurred: {e}")
        return False

def suggest_tags_from_card_news(json_path="card_news_output.json"):
    """
    Suggest Jamendo tags based on the generated card news script/content using OpenAI.
    Returns a list of single tags (not comma-separated) from the curated lists.
    """
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        scripts = data.get("scripts") or data.get("card_contents") or []
        text = " ".join(scripts).strip()
        if not text:
            raise ValueError("No script or card content found in JSON.")
        # Use OpenAI to select tags from the curated lists
        import openai
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY')
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        genre_list = ', '.join(POPULAR_GENRE_TAGS)
        mood_list = ', '.join(POPULAR_MOOD_TAGS)
        prompt = (
            f"Given the following YouTube Shorts card news script, select the 1-2 most relevant music genre tags and 1-2 most relevant mood tags from the provided lists. "
            f"Only choose tags from these lists. Return your answer as a Python list of strings, e.g. ['pop', 'happy', 'energetic'].\n\n"
            f"Script: {text}\n\n"
            f"Genre tags: {genre_list}\nMood tags: {mood_list}\n"
            f"Your answer:"
        )
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[{"role": "system", "content": "You are a helpful assistant that selects music tags for background music. Only use the provided genre and mood tag lists."},
                      {"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.2
        )
        import ast
        # Try to parse the response as a Python list
        tags = []
        try:
            tags = ast.literal_eval(response.choices[0].message.content.strip())
            # Filter to only allow tags from the curated lists
            tags = [t for t in tags if t in POPULAR_GENRE_TAGS or t in POPULAR_MOOD_TAGS]
        except Exception as e:
            print(f"[Agent] Could not parse OpenAI tag response: {e}")
        if not tags:
            # Fallback to keyword-based method
            tags = get_working_tags_by_topic(text)
        return tags
    except Exception as e:
        print(f"[Agent] Could not analyze card news output: {e}")
        return ["pop", "happy"]  # Safe default

def main():
    """
    Main function to search and download music.
    """
    # Check if Jamendo client ID is configured
    if not JAMENDO_CLIENT_ID:
        print("[ERROR] JAMENDO_CLIENT_ID not found in environment variables!")
        print("Please add JAMENDO_CLIENT_ID=your_client_id to your .env file")
        return
    
    # Try to suggest tags from card news output JSON
    json_path = "card_news_output.json"
    if os.path.exists(json_path):
        topic_tags = suggest_tags_from_card_news(json_path)
        print(f"[Agent] Using tags from card news: {topic_tags}")
    else:
        # Fallback: Ask user for a topic or keyword for the card news
        topic = input("Enter the card news topic or keywords (or press Enter for default): ").strip()
        if topic:
            topic_tags = get_working_tags_by_topic(topic)
        else:
            topic_tags = ["pop", "happy"]  # Default safe tags
        print(f"[Agent] Using tags: {topic_tags}")
    
    # Search for tracks
    recommendations = search_jamendo_tracks_comprehensive(topic_tags, limit=5)
    
    if recommendations:
        print(f"\n[SUCCESS] Found {len(recommendations)} track(s):")
        for idx, track in enumerate(recommendations, 1):
            duration_str = f"{track['duration']//60}:{track['duration']%60:02d}" if track['duration'] else "Unknown"
            print(f"{idx}. {track['title']} by {track['artist']} ({duration_str})")
            print(f"   Listen: {track['listen_url']}")
            if track['download_url']:
                print(f"   Download: {track['download_url']}")
            if track['license']:
                print(f"   License: {track['license']}")
            print()
        
        # Automatically download the first track with a download link
        music_dir = "music"
        os.makedirs(music_dir, exist_ok=True)
        
        first_downloadable = next((t for t in recommendations if t['download_url']), None)
        if first_downloadable and first_downloadable['download_url']:
            filename = f"bg_music_{first_downloadable['title'][:30].replace(' ', '_')}.mp3"
            # Remove invalid filename characters
            filename = "".join(c for c in filename if c.isalnum() or c in "._-")
            full_path = os.path.join(music_dir, filename)
            success = download_music(first_downloadable['download_url'], full_path)
            if success:
                print(f"[SUCCESS] Background music downloaded: {filename}")
                # Write music info to JSON for video generator
                music_info = {
                    "music_title": first_downloadable['title'],
                    "music_artist": first_downloadable['artist'],
                    "music_path": full_path
                }
                with open("music_info.json", "w", encoding="utf-8") as f:
                    json.dump(music_info, f, ensure_ascii=False, indent=2)
                print(f"[INFO] Music info written to music_info.json")
        else:
            print("[WARNING] No download link available for any track.")
    else:
        print("[ERROR] No tracks found. This might indicate:")
        print("1. Invalid Jamendo API credentials")
        print("2. Network connectivity issues")
        print("3. Jamendo API service issues")

if __name__ == "__main__":
    main()