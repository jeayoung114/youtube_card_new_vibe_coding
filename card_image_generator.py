from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def create_card_image(text, output_path, width=1080, height=1920, bg_color=(0, 102, 204), font_color=(255, 255, 255), max_font_size=90, min_font_size=14, margin=60, line_spacing=2, top_indent_lines=7, top_indent_font_size=22, title_font_size=32, title_box_height=100, box_border_color=(0,0,0), box_border_width=2, shadow_offset=8, shadow_color=(80,80,80,80)):
    # Split text into title line and content
    if '\n' in text:
        title_line, content = text.split('\n', 1)
    else:
        title_line, content = text, ''
    # Create a blank image with solid background
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    def get_font(size):
        font_paths = [
            "/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/local/share/fonts/DejaVuSans.ttf",
        ]
        for path in font_paths:
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
        return ImageFont.load_default()

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
    title_font = get_font(title_font_size)
    title_bbox = draw.textbbox((0,0), title_line, font=title_font)
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
        font = get_font(font_size)
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
    # Draw content text inside content box
    y = content_box_top + (allowed_height - total_text_height) // 2 if lines else content_box_top
    left_indent = content_box_left + margin // 2  # Indent from the left border
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = left_indent  # Left align with indent
        draw.text((x, y), line, font=font, fill=font_color)
        y += h + line_spacing
    img = img.convert('RGB')
    img.save(output_path)
    print(f"[Card] Saved card image: {output_path} (font size used: {font_size})")

def generate_cards_from_json(json_path="card_news_output.json", output_dir="cards"):
    import json
    os.makedirs(output_dir, exist_ok=True)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    card_contents = data.get("card_contents", [])
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
        create_card_image(text, os.path.join(output_dir, f"card_{idx}.png"), bg_color=bg_color, font_color=font_color)
    print(f"[Card] Card images generated in '{output_dir}' directory.")

if __name__ == "__main__":
    import json
    import argparse
    parser = argparse.ArgumentParser(description="Card Image Generator from JSON output")
    parser.add_argument('--json', type=str, default="card_news_output.json", help='Path to the card news output JSON file')
    parser.add_argument('--output_dir', type=str, default="cards", help='Directory to save card images')
    args = parser.parse_args()

    generate_cards_from_json(args.json, args.output_dir)
