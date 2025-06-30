"""
Run the full Card News pipeline: article search, summarization, card content, image, audio, video, and music.
This script links together all modules: article_search, card_image_generator, card_audio_generator, card_video_generator.
"""
import os
import subprocess
import json
from article_search import web_search, summarize_articles, generate_card_news_contents, generate_card_scripts
from card_image_generator import generate_cards_from_json
from card_audio_generator import generate_card_audio
from card_video_generator import create_video_from_cards

def suggest_music_tags_from_scripts(scripts):
    text = " ".join(scripts).lower()
    if any(word in text for word in ["kids", "children", "playful", "funny", "cartoon"]):
        return "children,playful,fun,cheerful"
    if any(word in text for word in ["tech", "ai", "robot", "future", "startup"]):
        return "electronic,upbeat,corporate,techno,fun"
    if any(word in text for word in ["news", "update", "trend", "today"]):
        return "pop,upbeat,corporate,fun,cheerful"
    if any(word in text for word in ["happy", "joy", "smile", "celebrate"]):
        return "happy,cheerful,fun,upbeat,pop"
    return "fun,upbeat,cheerful,pop"

def run_pipeline(keyword, max_results=10, max_summaries=6, num_cards=3, generate_cards=True, generate_audio=True, generate_video=True, auto_music=True):
    print(f"[Pipeline] Starting pipeline for keyword: '{keyword}'")
    articles = web_search(keyword, max_results)
    summaries = summarize_articles(articles, max_summaries)
    card_contents = generate_card_news_contents(summaries, keyword, num_cards=num_cards)
    card_scripts = generate_card_scripts(card_contents)
    music_theme_tags = suggest_music_tags_from_scripts(card_scripts)
    output = {
        "keyword": keyword,
        "articles": articles,
        "summaries": summaries,
        "card_contents": card_contents,
        "card_scripts": card_scripts,
        "music_theme_tags": music_theme_tags
    }
    with open("card_news_output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"[Pipeline] Results saved to card_news_output.json.")
    if generate_cards:
        generate_cards_from_json(json_path="card_news_output.json", output_dir="cards")
    if generate_audio:
        generate_card_audio(card_scripts)
        print(f"[Pipeline] Audio files generated in 'audio/' directory.")
    if auto_music:
        print("[Pipeline] Fetching background music using bg_music_retrieval.py ...")
        subprocess.run(["python", "bg_music_retrieval.py"])
    if generate_video:
        create_video_from_cards(duration=None)
        print(f"[Pipeline] Card news video generated.")
    print(f"[Pipeline] Pipeline complete.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run the full Card News pipeline")
    parser.add_argument('--keyword', type=str, required=False, help='Keyword to search for articles')
    parser.add_argument('--max_results', type=int, default=10, help='Number of articles to search (SERPAPI)')
    parser.add_argument('--max_summaries', type=int, default=6, help='Number of articles to summarize (reference articles)')
    parser.add_argument('--num_cards', type=int, default=3, help='Number of card news slides to generate')
    parser.add_argument('--no_cards', action='store_true', help='Do not generate card images')
    parser.add_argument('--no_audio', action='store_true', help='Do not generate audio files')
    parser.add_argument('--no_video', action='store_true', help='Do not generate video file')
    parser.add_argument('--no_music', action='store_true', help='Do not fetch background music')
    args = parser.parse_args()

    keyword = args.keyword or input("Enter a keyword to search for articles: ")
    run_pipeline(
        keyword,
        max_results=args.max_results,
        max_summaries=args.max_summaries,
        num_cards=args.num_cards,
        generate_cards=not args.no_cards,
        generate_audio=not args.no_audio,
        generate_video=not args.no_video,
        auto_music=not args.no_music
    )

if __name__ == "__main__":
    main()
