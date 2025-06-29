# Card News Shorts Generator

Create fully automated, fun, and engaging YouTube Shorts card news videos from trending news articles with synchronized images, voice-over, and vertical video output.

## Features
- **Automated News Search:** Fetches the latest news articles using SerpAPI (Google News).
- **Smart Summarization:** Summarizes articles into concise, informative paragraphs with a fun fact using OpenAI GPT-4.
- **Card News Content Agent:** Gathers all summaries and generates 3–5 lively, story-like card news slides for a cohesive video.
- **Dynamic Card Images:** Generates vertical (1080x1920) card images with large, readable text and a unique background color for each card.
- **Voice-Over Generation:** Uses ElevenLabs API to create natural-sounding audio for each card.
- **Video Assembly:** Combines cards and audio into a perfectly synchronized vertical video, ready for YouTube Shorts.
- **Fun & Joyful Style:** All card news content is lively, playful, and ends sentences with exclamation marks for a joyful vibe!
- **Timing Control:** Each card is limited to ~10 seconds of speech for optimal Shorts pacing.

## Requirements
- Python 3.8+
- [OpenAI API key](https://platform.openai.com/)
- [SerpAPI key](https://serpapi.com/)
- [ElevenLabs API key](https://elevenlabs.io/)
- See `requirements.txt` for Python dependencies

## Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/card-news-shorts.git
   cd card-news-shorts
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Set up your `.env` file:**
   ```env
   OPENAI_API_KEY=your_openai_key
   SERPAPI_API_KEY=your_serpapi_key
   ELEVENLABS_API_KEY=your_elevenlabs_key
   ```

## Usage
1. Run the main script:
   ```sh
   python article_search.py
   ```
2. Enter a keyword when prompted (e.g., `AI news`).
3. The system will:
   - Search for news
   - Summarize and generate fun, lively card news content
   - Create card images and voice-over
   - Assemble a vertical video in `card_news_video.mp4`

## Output
- `cards/` — Generated card images
- `audio/` — Voice-over audio files
- `card_news_video.mp4` — Final vertical video for YouTube Shorts

## Customization
- **Colors:** Edit the `bg_colors` list in `article_search.py` for custom card backgrounds.
- **Card Count:** Change the `num_cards` parameter in `generate_card_news_contents`.
- **Timing:** Adjust `max_chars_per_card` for shorter/longer card durations.

## Major Updates (2025)

- **Pastel Card Backgrounds & High-Contrast Text:** Card backgrounds are now soft pastel tones, and each card uses a matching high-contrast text color for readability.
- **Sentence-Based Line Breaks:** Card content now starts a new line after each sentence for better visibility.
- **Smaller Font Size:** Maximum font size for card content is reduced for improved readability, especially with many lines.
- **Lively Spoken Scripts:** Each card gets a lively, conversational script (not just the card text) for audio generation, making the voice-over sound like a real person.
- **Script Length Control:** Spoken scripts are limited to 3 sentences or ~220 characters for punchy, short audio.
- **Modular Card Generation:** Card image generation (including backgrounds and text color) is handled in `card_image_generator.py` via `generate_cards_from_json`, keeping the agent logic clean.
- **Card Content Truncation:** Card text is never cut mid-sentence; truncation always happens at sentence boundaries.
- **Flexible CLI:** You can control the number of reference articles, cards, and other options via command-line arguments.
- **Output JSON:** All results (articles, summaries, card contents, scripts) are saved to `card_news_output.json` for easy reuse.

## Advanced Usage

- **Generate Only Cards from JSON:**
  ```sh
  python card_image_generator.py --json card_news_output.json --output_dir cards
  ```
- **Custom Card Generation in Agent:**
  The agent now only handles article search, summarization, and script generation. Card image generation is fully modular and handled in the image generator script.

## License
MIT

## Credits
- [OpenAI](https://openai.com/)
- [SerpAPI](https://serpapi.com/)
- [ElevenLabs](https://elevenlabs.io/)
- [Pillow](https://python-pillow.org/), [MoviePy](https://zulko.github.io/moviepy/)

---

Enjoy making fun, automated card news for YouTube Shorts!
