"""
article_search.py: Handles news article search (via SerpAPI), summarization (via OpenAI), and card/script content generation for the Card News pipeline.
"""
import os
from openai import OpenAI
import requests
from dotenv import load_dotenv

# Set your OpenAI API key here or use environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

load_dotenv()

def web_search(query, max_results=3):
    """
    Search for news articles using SerpAPI Google News engine.

    Args:
        query (str): The search keyword or phrase.
        max_results (int): Maximum number of articles to return.
    Returns:
        list[dict]: List of articles, each as a dict with 'title', 'summary', and 'url'.
    """
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
    """
    Summarize up to max_summaries articles using OpenAI if needed.

    Args:
        articles (list[dict]): List of articles with 'title', 'summary', and 'url'.
        max_summaries (int): Maximum number of articles to summarize.
    Returns:
        list[str]: List of summary strings (with fun facts).
    """
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
    """
    Generate card news slide contents from summaries and topic using OpenAI.

    Args:
        summaries (list[str]): List of article summaries.
        topic (str): The main topic or keyword.
        num_cards (int): Number of card slides to generate.
        max_chars_per_card (int): Max characters per card.
    Returns:
        list[str]: List of card content strings (with hashtags as title line).
    """
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
        f"IMPORTANT: Make each card's content mutually exclusive—avoid repeating the same facts, details, or fun facts across cards. Each card should feel fresh and unique, so viewers don't get tired or bored!\n"
        f"Add relevant, fun, and visually appealing emojis to each card to make the visuals more attractive and engaging. Use at least 2-3 emojis per card, and place them naturally in the text or at the start/end of lines.\n\n"
        f"Article summaries:\n{all_summaries}"
    )
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[{"role": "system", "content": f"You are a creative, playful YouTube Shorts scriptwriter for card news! Generate a sequence of fun, joyful card news slides from the provided summaries! Do not use Markdown or formatting symbols! Limit each card to {max_chars_per_card} characters or less! Add relevant, fun, and visually appealing emojis to each card for better visual impact."},
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
    """
    Generate lively spoken scripts for each card using OpenAI, with smooth transitions.

    Args:
        card_contents (list[str]): List of card content strings (with hashtags/title line).
    Returns:
        list[str]: List of spoken script strings for each card.
    """
    print(f"[Agent] Generating lively spoken scripts for each card...")
    import openai
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY')
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    scripts = []
    previous_content = None
    for idx, text in enumerate(card_contents, 1):
        # Remove hashtags/title line for script
        if '\n' in text:
            _, content = text.split('\n', 1)
        else:
            content = text
        if idx == 1:
            prompt = (
                f"Rewrite the following card news content as if a lively, friendly person is talking directly to the viewer for a YouTube Short. "
                f"Make it sound natural, conversational, and engaging—add a greeting, rhetorical questions, or reactions if appropriate. "
                f"Keep it short and energetic, and don't just read the text—make it feel like a real person is talking! Limit the script to 3 sentences or about 220 characters maximum.\n\nContent: {content}"
            )
        else:
            prompt = (
                f"Rewrite the following card news content as if a lively, friendly person is talking directly to the viewer for a YouTube Short. "
                f"Make it sound natural, conversational, and engaging—add a transition from the previous card, referencing what was just said or using a connecting phrase (like 'And that's not all!', 'Next up,', 'But wait, there's more!', etc.). "
                f"Make the flow feel like a continuous story, not isolated slides. "
                f"Don't just read the text—make it feel like a real person is talking! Limit the script to 3 sentences or about 220 characters maximum.\n\nPrevious card: {previous_content}\nCurrent card: {content}"
            )
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[{"role": "system", "content": "You are a lively YouTube Shorts host. Rewrite the content as a natural, spoken script, not just reading the text. For cards after the first, make sure to connect the script smoothly to the previous card, using transition phrases or referencing what was just said. Keep it short: 3 sentences or about 220 characters max."},
                      {"role": "user", "content": prompt}],
            max_tokens=180,
            temperature=0.95
        )
        script = response.choices[0].message.content.strip()
        scripts.append(script)
        previous_content = content
    print(f"[Agent] Card scripts generated.")
    return scripts

def main():
    # Example usage for testing
    query = input("Enter a search query for news articles: ")
    articles = web_search(query)
    summaries = summarize_articles(articles)
    card_contents = generate_card_news_contents(summaries, query)
    scripts = generate_card_scripts(card_contents)
    print("\n[RESULT] Card Scripts:")
    for idx, script in enumerate(scripts, 1):
        print(f"Card {idx}: {script}\n")

if __name__ == "__main__":
    main()
