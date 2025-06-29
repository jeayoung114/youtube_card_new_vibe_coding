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
                f"Summarize the news article titled '{article['title']}' in 2-4 short, punchy, but also informative sentences for a YouTube card news slide. "
                f"Make every sentence lively, energetic, and easy to read! Use exclamation marks and keep it fun! "
                f"Be sure to include the main point, at least one key detail, and any important context so viewers understand the story. Then, add a fun, surprising, or interesting fact about the topic or article. "
                f"Separate the summary and fun fact with a newline. Be engaging. If possible, use the URL: {article['url']}"
            )
            response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[{"role": "system", "content": "You are a helpful assistant that summarizes news articles for YouTube card news. Each summary should be 2-4 short, punchy but informative sentences, followed by a fun fact about the topic."},
                          {"role": "user", "content": prompt}],
                max_tokens=220,
                temperature=0.7
            )
            summary = response.choices[0].message.content.strip()
        else:
            print(f"[Agent] Compressing snippet using OpenAI for card news style and fun fact.")
            # If snippet exists, compress it using OpenAI for card news style
            prompt = (
                f"Rewrite the following news summary in 2-4 short, punchy, but also informative sentences for a YouTube card news slide. "
                f"Make every sentence lively, energetic, and easy to read! Use exclamation marks and keep it fun! "
                f"Be sure to include the main point, at least one key detail, and any important context so viewers understand the story. Then, add a fun, surprising, or interesting fact about the topic or article. "
                f"Separate the summary and fun fact with a newline. Be engaging.\nSummary: {summary}"
            )
            response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[{"role": "system", "content": "You are a helpful assistant that summarizes news articles for YouTube card news. Each summary should be 2-4 short, punchy but informative sentences, followed by a fun fact about the topic."},
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
        f"First, generate three hashtags (no more than two words each) that best describe the genre or category of the article. Format them as '#[topic], #[topic], #[topic]' and place them at the very top of each card's Title line. The hashtags should be short and relevant!\n"
        f"Then, for each card, write the main content as before: Each slide should have a clear purpose: start with a hook or intro, then main points, key details, and end with a fun fact or outro! "
        f"Make the language lively, light, and engaging—avoid being stiff or formal! End every sentence with an exclamation mark (!) to give a joyful, energetic atmosphere! "
        f"Each slide should be concise, easy to read, and use line breaks for readability! Number each slide as 'Card 1:', 'Card 2:', etc.! Do not use Markdown or any formatting symbols like ** or __! "
        f"Limit each card's content so it can be read aloud in under 10 seconds (about {max_chars_per_card} characters or less)!\n"
        f"IMPORTANT: Make each card's content mutually exclusive—avoid repeating the same facts, details, or fun facts across cards. Each card should feel fresh and unique, so viewers don't get tired or bored!\n\n"
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
    # Extract hashtags (assume they are at the very top, before Card 1:)
    import re
    hashtag_match = re.match(r"^#.*", content)
    hashtags = hashtag_match.group(0) if hashtag_match else ""
    # Remove hashtags from content for card splitting
    content_wo_hashtags = content[len(hashtags):].strip() if hashtags else content
    card_contents = re.split(r'Card \d+:', content_wo_hashtags)
    # Filter out empty, trivial, or formatting-only results
    card_contents = [c.strip() for c in card_contents if c.strip() and c.strip() not in ['**', '__', '*', ''] and len(c.strip()) > 10]
    # Truncate each card to max_chars_per_card, but only at sentence boundaries
    def truncate_at_sentence(text, max_chars):
        if len(text) <= max_chars:
            return text
        # Find all sentence boundaries
        import re
        sentences = re.findall(r'[^.!?]*[.!?]', text)
        result = ''
        for s in sentences:
            if len(result) + len(s) > max_chars:
                break
            result += s
        return result.strip() if result else text[:max_chars].rstrip()
    card_contents = [truncate_at_sentence(c, max_chars_per_card) for c in card_contents]
    # If not enough cards, fallback to splitting by double newlines
    if len(card_contents) < num_cards:
        card_contents = [c.strip() for c in content_wo_hashtags.split('\n\n') if c.strip() and c.strip() not in ['**', '__', '*', ''] and len(c.strip()) > 10]
        card_contents = [truncate_at_sentence(c, max_chars_per_card) for c in card_contents]
    # Limit to num_cards
    card_contents = card_contents[:num_cards]
    # Prepend hashtags to each card as the Title line
    card_contents = [f"{hashtags}\n{c}" for c in card_contents]
    print(f"[Agent] Card news contents generated.")
    return card_contents

def generate_card_scripts(card_contents):
    print(f"[Agent] Generating lively spoken scripts for each card...")
    import openai
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY')
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    scripts = []
    for idx, text in enumerate(card_contents, 1):
        # Remove hashtags/title line for script
        if '\n' in text:
            _, content = text.split('\n', 1)
        else:
            content = text
        prompt = (
            f"Rewrite the following card news content as if a lively, friendly person is talking directly to the viewer for a YouTube Short. "
            f"Make it sound natural, conversational, and engaging—add a greeting, rhetorical questions, or reactions if appropriate. "
            f"Keep it short and energetic, and don't just read the text—make it feel like a real person is talking! Limit the script to 3 sentences or about 220 characters maximum.\n\nContent: {content}"
        )
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[{"role": "system", "content": "You are a lively YouTube Shorts host. Rewrite the content as a natural, spoken script, not just reading the text. Keep it short: 3 sentences or about 220 characters max."},
                      {"role": "user", "content": prompt}],
            max_tokens=180,
            temperature=0.95
        )
        script = response.choices[0].message.content.strip()
        scripts.append(script)
    print(f"[Agent] Card scripts generated.")
    return scripts

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
                f"Summarize the news article titled '{article['title']}' in 2-4 short, punchy, but also informative sentences for a YouTube card news slide. "
                f"Make every sentence lively, energetic, and easy to read! Use exclamation marks and keep it fun! "
                f"Be sure to include the main point, at least one key detail, and any important context so viewers understand the story. Then, add a fun, surprising, or interesting fact about the topic or article. "
                f"Separate the summary and fun fact with a newline. Be engaging. If possible, use the URL: {article['url']}"
            )
            response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[{"role": "system", "content": "You are a helpful assistant that summarizes news articles for YouTube card news. Each summary should be 2-4 short, punchy but informative sentences, followed by a fun fact about the topic."},
                          {"role": "user", "content": prompt}],
                max_tokens=220,
                temperature=0.7
            )
            summary = response.choices[0].message.content.strip()
        else:
            print(f"[Agent] Compressing snippet using OpenAI for card news style and fun fact.")
            prompt = (
                f"Rewrite the following news summary in 2-4 short, punchy, but also informative sentences for a YouTube card news slide. "
                f"Make every sentence lively, energetic, and easy to read! Use exclamation marks and keep it fun! "
                f"Be sure to include the main point, at least one key detail, and any important context so viewers understand the story. Then, add a fun, surprising, or interesting fact about the topic or article. "
                f"Separate the summary and fun fact with a newline. Be engaging.\nSummary: {summary}"
            )
            response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[{"role": "system", "content": "You are a helpful assistant that summarizes news articles for YouTube card news. Each summary should be 2-4 short, punchy but informative sentences, followed by a fun fact about the topic."},
                          {"role": "user", "content": prompt}],
                max_tokens=220,
                temperature=0.7
            )
            summary = response.choices[0].message.content.strip()
        summaries.append(summary)
    print(f"[Agent] All articles summarized.")

    # Generate card news contents from summaries
    card_contents = generate_card_news_contents(summaries, keyword)

    # NEW: Generate lively scripts for each card
    card_scripts = generate_card_scripts(card_contents)

    if generate_cards:
        from card_image_generator import generate_cards_from_json
        generate_cards_from_json(
            json_path="card_news_output.json",
            output_dir="cards"
        )
    if generate_audio:
        generate_card_audio(card_scripts)  # Use scripts, not card text
        print(f"[Agent] Audio files generated in 'audio/' directory.")
    if generate_video:
        create_video_from_cards(duration=None)  # duration will be set per audio length
        print(f"[Agent] Card news video generated.")
    print(f"[Agent] Card news generation complete.")
    # Save results to JSON file
    import json
    output = {
        "keyword": keyword,
        "articles": articles,
        "summaries": summaries,
        "card_contents": card_contents,
        "card_scripts": card_scripts
    }
    with open("card_news_output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"[Agent] Results saved to card_news_output.json.")
    return card_contents

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Automated Card News Generator")
    parser.add_argument('--keyword', type=str, required=False, help='Keyword to search for articles')
    parser.add_argument('--max_results', type=int, default=10, help='Number of articles to search (SERPAPI)')
    parser.add_argument('--max_summaries', type=int, default=6, help='Number of articles to summarize (reference articles)')
    parser.add_argument('--num_cards', type=int, default=3, help='Number of card news slides to generate')
    parser.add_argument('--generate_cards', action='store_true', help='Generate card images')
    parser.add_argument('--generate_audio', action='store_true', help='Generate audio files')
    parser.add_argument('--generate_video', action='store_true', help='Generate video file')
    args = parser.parse_args()

    keyword = args.keyword or input("Enter a keyword to search for articles: ")
    card_contents = agent(
        keyword,
        max_results=args.max_results,
        max_summaries=args.max_summaries,
        generate_cards=args.generate_cards,
        generate_audio=args.generate_audio,
        generate_video=args.generate_video
    )
