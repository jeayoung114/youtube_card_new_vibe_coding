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

## Changelog

---
#### 2025-06-29 — First Push
- **Initial Modular Structure:** Set up Python project, requirements, .env, and modular structure for news search, summarization, card image/audio/video generation.
- **Automated News Search:** Implemented news search (SerpAPI) and summarization (OpenAI) with robust error handling.
- **Card Image Generator:** Created pastel backgrounds, high-contrast text, and auto-scaling font for card images.
- **Audio & Video Generation:** Added ElevenLabs audio generator and MoviePy video generator.
- **Basic Workflow:** Automated workflow in `article_search.py` to go from keyword to finished video.

---
#### 2025-06-29 — Second Push
- **Card News Agent:** Generates 3–5 sequential, story-like slides with hashtags.
- **Card Content Truncation:** Truncates at sentence boundaries; lively, joyful language.
- **Script Generator Agent:** Produces lively, conversational scripts for audio.
- **Output JSON:** Includes articles, summaries, card contents, scripts, and music theme tags.
- **Asset Folders:** All asset folders (`cards`, `audio`, `music`) are now consistently used and auto-created as needed.

---
#### 2025-06-29 — Third Push
- **Jamendo Integration:** Downloads and uses copyright-free background music from Jamendo, with multi-step fallback to guarantee at least one track is always included in the video.
- **Background Music Automation:** Copyright-free background music is automatically fetched from Jamendo and mixed into the final video.
- **Robust Music Fallback:** If no music is found for suggested tags, the system retries with default and broad tags, ensuring at least one track is always loaded.
- **Consistent Video Output:** The video generator always uses the downloaded background music and outputs to `card_news_video.mp4`.

---
#### 2025-06-29 — Fourth Push
- **Smooth Card Script Transitions:** Card scripts are now generated with smooth, story-like connections between each card.
- **Changelog Improvements:** Changelog now tracks each push with date and order, and is ready for future pushes.


## License
MIT

## Credits
- [OpenAI](https://openai.com/)
- [SerpAPI](https://serpapi.com/)
- [ElevenLabs](https://elevenlabs.io/)
- [Pillow](https://python-pillow.org/), [MoviePy](https://zulko.github.io/moviepy/)

---

Enjoy making fun, automated card news for YouTube Shorts!
