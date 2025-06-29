import os
from openai import OpenAI
import requests
from card_image_generator import create_card_image
from card_audio_generator import generate_card_audio
from card_video_generator import create_video_from_cards
from dotenv import load_dotenv

# Set your OpenAI API key here or use environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

load_dotenv()

def web_search(query, max_results=3):
    print(f"[Agent] Searching for news articles about: {query}")
    import os
    import requests
    api_key = os.getenv("SERPAPI_API_KEY")
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": api_key,
        "num": max_results,
        "engine": "google_news"
    }
    response = requests.get(url, params=params)
    results = []
    if response.status_code == 200:
        data = response.json()
        print(f"[Agent] Found {len(data.get('news_results', []))} articles.")
        for item in data.get("news_results", []):
            results.append({
                "title": item.get("title", ""),
                "summary": item.get("snippet", ""),
                "url": item.get("link", "")
            })
    else:
        print(f"[Agent] Failed to fetch articles. Status code: {response.status_code}")
    return results

def summarize_articles(articles, max_summaries=3):
    print(f"[Agent] Summarizing up to {max_summaries} articles for card news...")
    summaries = []
    for idx, article in enumerate(articles[:max_summaries], 1):
        print(f"[Agent] Summarizing article {idx}: {article['title']}")
        summary = article['summary']
        if not summary:
            print(f"[Agent] No snippet found. Using OpenAI to generate a paragraph summary and fun fact.")
            # Use OpenAI to generate a very short, punchy summary for card news
            prompt = (
                f"Summarize the news article titled '{article['title']}' in a concise but informative paragraph suitable for a YouTube card news slide. "
                f"Cover the main point and at least one key detail or context. Then, add a fun, surprising, or interesting fact about the topic or article. "
                f"Separate the summary and fun fact with a newline. Be engaging. If possible, use the URL: {article['url']}"
            )
            response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[{"role": "system", "content": "You are a helpful assistant that summarizes news articles for YouTube card news. Each summary should be a concise but informative paragraph, followed by a fun fact about the topic."},
                          {"role": "user", "content": prompt}],
                max_tokens=220,
                temperature=0.7
            )
            summary = response.choices[0].message.content.strip()
        else:
            print(f"[Agent] Compressing snippet using OpenAI for card news style and fun fact.")
            # If snippet exists, compress it using OpenAI for card news style
            prompt = (
                f"Rewrite the following news summary in a concise but informative paragraph suitable for a YouTube card news slide. "
                f"Cover the main point and at least one key detail or context. Then, add a fun, surprising, or interesting fact about the topic or article. "
                f"Separate the summary and fun fact with a newline. Be engaging.\nSummary: {summary}"
            )
            response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[{"role": "system", "content": "You are a helpful assistant that summarizes news articles for YouTube card news. Each summary should be a concise but informative paragraph, followed by a fun fact about the topic."},
                          {"role": "user", "content": prompt}],
                max_tokens=220,
                temperature=0.7
            )
            summary = response.choices[0].message.content.strip()
        summaries.append(summary)
    print(f"[Agent] All articles summarized.")
    return summaries

def generate_card_news_contents(summaries, topic, num_cards=3, max_chars_per_card=220):
    print(f"[Agent] Generating {num_cards} fun, joyful card news slides from all summaries...")
    # Join all summaries into one context
    all_summaries = "\n".join(summaries)
    prompt = (
        f"You are a creative, playful YouTube Shorts scriptwriter. Given the topic '{topic}' and the following article summaries, "
        f"create {num_cards} card news slide contents that together tell a fun, joyful mini-story or sequence! "
        f"Each slide should have a clear purpose: start with a hook or intro, then main points, key details, and end with a fun fact or outro! "
        f"Make the language lively, light, and engaging—avoid being stiff or formal! End every sentence with an exclamation mark (!) to give a joyful, energetic atmosphere! "
        f"Each slide should be concise, easy to read, and use line breaks for readability! Number each slide as 'Card 1:', 'Card 2:', etc.! Do not use Markdown or any formatting symbols like ** or __! "
        f"Limit each card's content so it can be read aloud in under 10 seconds (about {max_chars_per_card} characters or less)!\n\n"
        f"Article summaries:\n{all_summaries}"
    )
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[{"role": "system", "content": "You are a creative, playful YouTube Shorts scriptwriter for card news! Generate a sequence of fun, joyful card news slides from the provided summaries! Do not use Markdown or formatting symbols! Limit each card to {max_chars_per_card} characters or less!"},
                  {"role": "user", "content": prompt}],
        max_tokens=1200,
        temperature=0.9
    )
    # Split the response into individual card contents
    content = response.choices[0].message.content.strip()
    # Try to split by 'Card X:'
    import re
    card_contents = re.split(r'Card \d+:', content)
    # Filter out empty, trivial, or formatting-only results
    card_contents = [c.strip() for c in card_contents if c.strip() and c.strip() not in ['**', '__', '*', ''] and len(c.strip()) > 10]
    # Truncate each card to max_chars_per_card
    card_contents = [c[:max_chars_per_card].rstrip() for c in card_contents]
    # If not enough cards, fallback to splitting by double newlines
    if len(card_contents) < num_cards:
        card_contents = [c.strip() for c in content.split('\n\n') if c.strip() and c.strip() not in ['**', '__', '*', ''] and len(c.strip()) > 10]
        card_contents = [c[:max_chars_per_card].rstrip() for c in card_contents]
    # Limit to num_cards
    card_contents = card_contents[:num_cards]
    print(f"[Agent] Card news contents generated.")
    return card_contents

def agent(keyword, max_results=3, max_summaries=3, generate_cards=False, generate_audio=False, generate_video=False):
    print(f"[Agent] Starting card news agent for keyword: '{keyword}'")
    # Step 1: Search articles
    articles = web_search(keyword, max_results)
    # Step 2: Summarize articles (limit number)
    summaries = []
    print(f"[Agent] Summarizing up to {max_summaries} articles for card news...")
    for idx, article in enumerate(articles[:max_summaries], 1):
        print(f"[Agent] Summarizing article {idx}: {article['title']}")
        summary = article['summary']
        if not summary:
            print(f"[Agent] No snippet found. Using OpenAI to generate a paragraph summary and fun fact.")
            prompt = (
                f"Summarize the news article titled '{article['title']}' in a paragraph but informative sentences suitable for a YouTube card news slide. "
                f"Cover the main point and at least one key detail or context. Then, add a fun, surprising, or interesting fact about the topic or article. "
                f"Separate the summary and fun fact with a newline. Be engaging. If possible, use the URL: {article['url']}"
            )
            response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[{"role": "system", "content": "You are a helpful assistant that summarizes news articles for YouTube card news. Each summary should be a concise but informative paragraph, followed by a fun fact about the topic."},
                          {"role": "user", "content": prompt}],
                max_tokens=220,
                temperature=0.7
            )
            summary = response.choices[0].message.content.strip()
        else:
            print(f"[Agent] Compressing snippet using OpenAI for card news style and fun fact.")
            prompt = (
                f"Rewrite the following news summary in a paragraph concise but informative sentences suitable for a YouTube card news slide. "
                f"Cover the main point and at least one key detail or context. Then, add a fun, surprising, or interesting fact about the topic or article. "
                f"Separate the summary and fun fact with a newline. Be engaging.\nSummary: {summary}"
            )
            response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[{"role": "system", "content": "You are a helpful assistant that summarizes news articles for YouTube card news. Each summary should be a concise but informative paragraph, followed by a fun fact about the topic."},
                          {"role": "user", "content": prompt}],
                max_tokens=220,
                temperature=0.7
            )
            summary = response.choices[0].message.content.strip()
        summaries.append(summary)
    print(f"[Agent] All articles summarized.")

    # NEW: Generate card news contents from summaries
    card_contents = generate_card_news_contents(summaries, keyword)

    if generate_cards:
        os.makedirs("cards", exist_ok=True)
        # Define a list of background colors (RGB tuples)
        bg_colors = [
            (0, 102, 204),    # Blue
            (34, 139, 34),    # Green
            (220, 20, 60),    # Crimson
            (255, 140, 0),    # Orange
            (128, 0, 128),    # Purple
            (255, 215, 0),    # Gold
            (70, 130, 180),   # Steel Blue
            (255, 99, 71),    # Tomato
            (0, 191, 255),    # Deep Sky Blue
            (255, 20, 147),   # Deep Pink
        ]
        for idx, content in enumerate(card_contents, 1):
            bg_color = bg_colors[(idx - 1) % len(bg_colors)]
            create_card_image(content, f"cards/card_{idx}.png", bg_color=bg_color)
        print(f"[Agent] Card images generated in 'cards/' directory.")
    if generate_audio:
        generate_card_audio(card_contents)
        print(f"[Agent] Audio files generated in 'audio/' directory.")
    if generate_video:
        create_video_from_cards(duration=None)  # duration will be set per audio length
        print(f"[Agent] Card news video generated.")
    print(f"[Agent] Card news generation complete.")
    return card_contents

if __name__ == "__main__":
    keyword = input("Enter a keyword to search for articles: ")
    agent(keyword, max_results=10, max_summaries=3, generate_cards=True, generate_audio=True, generate_video=True)
