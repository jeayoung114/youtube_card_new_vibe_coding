**Note:**  
> All code in this project was generated with Vibe Coding — not a single line was typed by hand. Even Readme file!

# Card News Shorts Generator

Create fully automated, fun, and engaging YouTube Shorts card news videos from trending news articles with synchronized images, voice-over, and vertical video output.

## Features
- **Automated News Search:** Uses an MCP (agent-based) workflow to fetch the latest news articles via SerpAPI (Google News).
- **Smart Summarization/Tag Generation:** Summarizes articles into concise, informative paragraphs with a fun fact and generates relevant tags using OpenAI GPT-4.1.
- **Card News Content Creation:** Gathers all summaries and generates 3–5 lively, story-like card news slides for a cohesive video.
- **Card News Script Creation:** Produces lively, conversational scripts for each card, optimized for voice-over.
- **Voice-Over Generation:** Uses ElevenLabs API to create natural-sounding audio for each card.
- **Background Music Retrieval:** Automatically fetches copyright-free background music based on the card news topic and mood.

### Additional Details
- Dynamic card images with emoji support and auto-scaling text
- Video assembly with perfect synchronization and vertical format
- Fun & joyful style: lively language, exclamation marks, and emojis
- Timing control for optimal Shorts pacing
- Output folders for cards, audio, and video

## Requirements
- Python 3.8+
- [OpenAI API key](https://platform.openai.com/)
- [SerpAPI key](https://serpapi.com/)
- [ElevenLabs API key](https://elevenlabs.io/)
- [Jamendo API client ID](https://developer.jamendo.com/v3.0)
- See `requirements.txt` for Python dependencies

## Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/jeayoung114/youtube_card_new_vibe_coding.git
   cd youtube_card_new_vibe_coding
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
   JAMENDO_CLIENT_ID=your_jamendo_client_id
   ```

## Usage
1. Run the pipeline script:
   ```sh
   python run_pipeline.py
   ```
2. Enter a keyword when prompted (e.g., `AI news`).
3. The system will:
   - Search for news
   - Summarize and generate fun, lively card news content
   - Create card images and voice-over
   - Assemble a vertical video in `card_news_video_<topic>.mp4`

## Output
- `cards/` — Generated card images
- `audio/` — Voice-over audio files
- `music/` — Downloaded background music tracks
- `emoji_png/` — Downloaded emoji PNGs for card rendering
- `card_news_output.json` — Full pipeline output (articles, summaries, cards, scripts, tags, etc.)
- `music_info.json` — Info about the selected background music
- `card_news_video_<topic>.mp4` — Final vertical video for YouTube Shorts

## Customization
- **Colors:** Edit the `bg_colors` list in `article_search.py` for custom card backgrounds.
- **Card Count:** Change the `num_cards` parameter in `generate_card_news_contents`.
- **Timing:** Adjust `max_chars_per_card` for shorter/longer card durations.

## Recent Features & Fixes

<details>
<summary>Show Details</summary>

- **Emoji Support in Card Images:**
  - Card image generator now uses emoji-compatible fonts if available, so emojis render correctly on cards (no more squares).
- **Background Music Fadeout:**
  - Video generator applies a smooth fadeout to the last 2 seconds of background music for a professional finish.
- **Audio Artifact Fix:**
  - Final audio (narration + background music) is always set to exactly the video duration, and fadeout is applied to the composite audio to prevent cracks or pops at the end.
- **Music Info Passing:**
  - `bg_music_retrieval.py` writes the downloaded music's name and path to `music_info.json`, which the video generator reads to use the correct background music.
- **OpenAI-based Music Tagging:**
  - Music tags for background music are now selected using OpenAI from a curated list, based on the generated card news script content.
- **Emojis in Card Content:**
  - Card news content generator instructs OpenAI to add relevant, fun, and visually appealing emojis to each card for better visual impact.

</details>

## Changelog

---
#### 2025-06-28 — First Push
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

---
#### 2025-06-29 — Fifth Push
- **Emoji Support:** Added support for emoji-compatible fonts in card images; improved music tag selection using OpenAI; ensured final audio matches video duration with fadeout to prevent artifacts.

## License
MIT

## Credits
- [OpenAI](https://openai.com/)
- [SerpAPI](https://serpapi.com/)
- [ElevenLabs](https://elevenlabs.io/)
- [Jamendo](https://www.jamendo.com/start)

---

Enjoy making fun, automated card news for YouTube Shorts!
