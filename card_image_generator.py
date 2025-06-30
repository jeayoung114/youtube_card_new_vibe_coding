from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import emoji as emoji_lib
import subprocess

def create_card_image(text, output_path, width=1080, height=1920, bg_color=(0, 102, 204), font_color=(255, 255, 255), max_font_size=90, min_font_size=14, margin=60, line_spacing=2, top_indent_lines=7, top_indent_font_size=22, title_font_size=32, title_box_height=100, box_border_color=(0,0,0), box_border_width=2, shadow_offset=8, shadow_color=(80,80,80,80)):
    # Split text into title line and content
    if '\n' in text:
        title_line, content = text.split('\n', 1)
    else:
        title_line, content = text, ''
    print(f"[DEBUG] Title line: '{title_line}' for {output_path}")
    # Create a blank image with solid background
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    def get_font(size, emoji=False):
        font_paths = [
            "/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/local/share/fonts/DejaVuSans.ttf",
        ]
        emoji_font_paths = [
            "/System/Library/Fonts/Apple Color Emoji.ttc",  # macOS
            "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",  # Linux
            "/usr/share/fonts/emoji/NotoColorEmoji.ttf",
            "/usr/share/fonts/truetype/seguiemj.ttf",  # Windows
        ]
        if emoji:
            for path in emoji_font_paths:
                if os.path.exists(path):
                    try:
                        return ImageFont.truetype(path, size)
                    except Exception:
                        continue
        for path in font_paths:
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
        return ImageFont.load_default()

    def split_text_with_emojis(text):
        # Returns a list of (is_emoji, segment) tuples
        result = []
        buffer = ''
        for char in text:
            if emoji_lib.is_emoji(char):
                if buffer:
                    result.append((False, buffer))
                    buffer = ''
                result.append((True, char))
            else:
                buffer += char
        if buffer:
            result.append((False, buffer))
        return result

    def draw_text_with_emojis(draw, img, text, font, x, y, fill, emoji_size):
        segments = split_text_with_emojis(text)
        cur_x = x
        for is_emoji, seg in segments:
            if is_emoji:
                codepoint = f"{ord(seg):x}".lower()
                emoji_path = os.path.join("emoji_png", f"{codepoint}.png")
                if os.path.exists(emoji_path):
                    emoji_img = Image.open(emoji_path).convert("RGBA").resize((emoji_size, emoji_size))
                    img.paste(emoji_img, (cur_x, y), emoji_img)
                    cur_x += emoji_size
                else:
                    # fallback: draw as text (may be square)
                    draw.text((cur_x, y), seg, font=font, fill=fill)
                    bbox = draw.textbbox((0, 0), seg, font=font)
                    cur_x += bbox[2] - bbox[0]
            else:
                draw.text((cur_x, y), seg, font=font, fill=fill)
                bbox = draw.textbbox((0, 0), seg, font=font)
                cur_x += bbox[2] - bbox[0]
        return cur_x

    # New: Increase border area for title and content boxes
    title_box_top = margin
    title_box_left = margin
    title_box_right = width - margin
    title_box_bottom = title_box_top + title_box_height

    # Draw shadow for title box
    shadow_img_title = Image.new('RGBA', img.size, (0,0,0,0))
    shadow_draw_title = ImageDraw.Draw(shadow_img_title)
    shadow_draw_title.rectangle([title_box_left+shadow_offset, title_box_top+shadow_offset, title_box_right+shadow_offset, title_box_bottom+shadow_offset], outline=shadow_color, width=box_border_width+2)
    img = Image.alpha_composite(img.convert('RGBA'), shadow_img_title)
    draw = ImageDraw.Draw(img)

    # Draw title box border (full width, thin black)
    draw.rectangle([title_box_left, title_box_top, title_box_right, title_box_bottom], outline=box_border_color, width=box_border_width)
    # Center title text in title box
    title_font = get_font(title_font_size, emoji=False)
    title_bbox = draw.textbbox((0,0), title_line, font=title_font)
    print(f"[DEBUG] Title bbox: {title_bbox} for '{title_line}'")
    title_w = title_bbox[2] - title_bbox[0]
    title_h = title_bbox[3] - title_bbox[1]
    title_x = (width - title_w) // 2
    title_y = title_box_top + (title_box_height - title_h) // 2
    draw.text((title_x, title_y), title_line, font=title_font, fill=font_color)

    # Content box: much closer to the edges, as in the red border
    content_box_top = title_box_bottom + margin//2
    content_box_left = margin//2
    content_box_right = width - margin//2
    content_box_bottom = height - margin//2

    # Draw shadow for content box (separately)
    shadow_img_content = Image.new('RGBA', img.size, (0,0,0,0))
    shadow_draw_content = ImageDraw.Draw(shadow_img_content)
    shadow_draw_content.rectangle([content_box_left+shadow_offset, content_box_top+shadow_offset, content_box_right+shadow_offset, content_box_bottom+shadow_offset], outline=shadow_color, width=box_border_width+2)
    img = Image.alpha_composite(img, shadow_img_content)
    draw = ImageDraw.Draw(img)

    # Draw content box border (thin black)
    draw.rectangle([content_box_left, content_box_top, content_box_right, content_box_bottom], outline=box_border_color, width=box_border_width)

    # Auto-scale font size for content
    font_size = max_font_size
    allowed_height = content_box_bottom - content_box_top - margin
    # Split content into sentences and wrap each sentence for better visibility
    import re
    sentence_splitter = re.compile(r'([^.!?]*[.!?])')
    sentences = [s.strip() for s in sentence_splitter.findall(content) if s.strip()]
    while font_size >= min_font_size:
        font = get_font(font_size, emoji=True)
        lines = []
        for sentence in sentences:
            words = sentence.split()
            line = ''
            for word in words:
                test_line = f'{line} {word}'.strip()
                bbox = draw.textbbox((0, 0), test_line, font=font)
                w = bbox[2] - bbox[0]
                if w > content_box_right - content_box_left - margin:
                    lines.append(line)
                    line = word
                else:
                    line = test_line
            if line:
                lines.append(line)
        max_line_width = max([draw.textbbox((0, 0), l, font=font)[2] - draw.textbbox((0, 0), l, font=font)[0] for l in lines]) if lines else 0
        total_text_height = sum([draw.textbbox((0, 0), l, font=font)[3] - draw.textbbox((0, 0), l, font=font)[1] + line_spacing for l in lines]) - line_spacing if lines else 0
        if total_text_height <= allowed_height and max_line_width <= content_box_right - content_box_left - margin:
            break
        font_size -= 2
    # Draw content text inside content box (with emoji support)
    font = get_font(font_size, emoji=False)
    y = content_box_top + (allowed_height - total_text_height) // 2 if lines else content_box_top
    left_indent = content_box_left + margin // 2  # Indent from the left border
    emoji_size = font_size  # Make emoji same height as text
    extra_line_spacing = int(font_size * 0.4)  # Add extra space between lines (40% of font size)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = left_indent  # Left align with indent
        draw_text_with_emojis(draw, img, line, font, x, y, font_color, emoji_size)
        y += h + line_spacing + extra_line_spacing
    img = img.convert('RGB')
    img.save(output_path)
    print(f"[Card] Saved card image: {output_path} (font size used: {font_size})")

def generate_cards_from_json(json_path="card_news_output.json", output_dir="cards"):
    import json
    os.makedirs(output_dir, exist_ok=True)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    card_contents = data.get("card_contents", [])
    topic = data.get("keyword", "topic").replace(' ', '_').replace(':', '').replace('/', '').replace('\\', '').replace('"', '').replace("'", '').replace('.', '').replace(',', '').lower()
    # Check for emojis and download PNGs if needed
    import emoji as emoji_lib
    all_text = " ".join(card_contents)
    emojis = set(c for c in all_text if emoji_lib.is_emoji(c))
    if emojis:
        print(f"[Card] Detected emojis: {emojis}. Downloading PNGs if missing...")
        subprocess.run(["python", "download_twemoji_pngs.py"])
    # Pastel background colors
    bg_colors = [
        (186, 225, 255),  # Pastel Blue
        (197, 255, 197),  # Pastel Green
        (255, 209, 220),  # Pastel Pink
        (255, 255, 204),  # Pastel Yellow
        (221, 204, 255),  # Pastel Purple
        (255, 239, 186),  # Pastel Peach
        (204, 255, 229),  # Pastel Mint
        (255, 204, 229),  # Pastel Rose
        (204, 229, 255),  # Pastel Sky
        (255, 255, 255),  # White
    ]
    # High-contrast text colors for each background
    text_colors = [
        (30, 30, 60),    # Dark blue for pastel blue
        (30, 60, 30),    # Dark green for pastel green
        (120, 30, 60),   # Deep rose for pastel pink
        (120, 120, 30),  # Olive for pastel yellow
        (70, 30, 120),   # Deep purple for pastel purple
        (120, 100, 30),  # Brown for pastel peach
        (30, 120, 90),   # Teal for pastel mint
        (120, 30, 70),   # Plum for pastel rose
        (30, 70, 120),   # Blue for pastel sky
        (30, 30, 30),    # Black for white
    ]
    for idx, text in enumerate(card_contents, 1):
        bg_color = bg_colors[(idx - 1) % len(bg_colors)]
        font_color = text_colors[(idx - 1) % len(text_colors)]
        # Add topic to filename for distinction
        filename = f"card_{idx}_{topic}.png"
        create_card_image(text, os.path.join(output_dir, filename), bg_color=bg_color, font_color=font_color)
    print(f"[Card] Card images generated in '{output_dir}' directory.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Card Image Generator from JSON output")
    parser.add_argument('--json', type=str, default="card_news_output.json", help='Path to the card news output JSON file')
    parser.add_argument('--output_dir', type=str, default="cards", help='Directory to save card images')
    args = parser.parse_args()
    generate_cards_from_json(args.json, args.output_dir)

if __name__ == "__main__":
    main()
