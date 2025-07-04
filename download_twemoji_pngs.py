"""
download_twemoji_pngs.py: Downloads emoji PNGs from Twemoji CDN for all emojis found in card news content.
"""
import os
import requests
import emoji
import json

TWEMOJI_BASE = "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/"
EMOJI_PNG_DIR = "emoji_png"

# Utility to get all emojis from card_news_output.json

def get_emojis_from_card_news(json_path="card_news_output.json"):
    """
    Extract all unique emojis from the card news output JSON file.

    Args:
        json_path (str): Path to card news output JSON.
    Returns:
        set[str]: Set of unique emoji characters found in card contents/scripts.
    """
    if not os.path.exists(json_path):
        print(f"[WARN] {json_path} not found. Please run article_search.py first.")
        return set()
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    scripts = data.get("card_contents") or data.get("scripts") or []
    text = " ".join(scripts)
    return set(c for c in text if emoji.is_emoji(c))

def emoji_to_codepoint(e):
    """
    Convert an emoji character to its Twemoji codepoint string.

    Args:
        e (str): Emoji character.
    Returns:
        str: Twemoji codepoint string (e.g., '1f600').
    """
    return "-".join(f"{ord(c):x}" for c in e)

def download_emoji_png(codepoint, out_path):
    """
    Download a PNG for the given emoji codepoint from Twemoji CDN.

    Args:
        codepoint (str): Twemoji codepoint string.
        out_path (str): Path to save the PNG file.
    Returns:
        bool: True if download succeeded, False otherwise.
    """
    url = f"{TWEMOJI_BASE}{codepoint}.png"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            with open(out_path, "wb") as f:
                f.write(r.content)
            print(f"[OK] Downloaded {out_path}")
            return True
        else:
            print(f"[FAIL] {url} - HTTP {r.status_code}")
    except Exception as e:
        print(f"[ERROR] {url} - {e}")
    return False

def main():
    """
    Download all required emoji PNGs for the current card news content.
    No arguments. Runs download if run directly.
    """
    os.makedirs(EMOJI_PNG_DIR, exist_ok=True)
    emojis = get_emojis_from_card_news()
    if not emojis:
        print("No emojis found in card news content.")
        return
    for e in emojis:
        codepoint = emoji_to_codepoint(e)
        out_path = os.path.join(EMOJI_PNG_DIR, f"{codepoint}.png")
        if not os.path.exists(out_path):
            download_emoji_png(codepoint, out_path)
        else:
            print(f"[SKIP] {out_path} already exists.")
    print("Done.")

if __name__ == "__main__":
    main()
