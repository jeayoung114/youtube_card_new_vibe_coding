from PIL import Image, ImageDraw, ImageFont
import os

def create_card_image(text, output_path, width=1080, height=1920, bg_color=(0, 102, 204), font_color=(255, 255, 255), max_font_size=1800, min_font_size=40, margin=100):
    # Create a blank image with solid background
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Try to load a scalable font (DejaVuSans or macOS Arial)
    def get_font(size):
        font_paths = [
            "/Library/Fonts/Arial.ttf",  # macOS Arial
            "/System/Library/Fonts/Supplemental/Arial.ttf",  # macOS supplemental
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "/usr/local/share/fonts/DejaVuSans.ttf",  # Homebrew or custom
        ]
        for path in font_paths:
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
        # Fallback to PIL's default font (will be small)
        return ImageFont.load_default()

    # Auto-scale font size
    font_size = max_font_size
    while font_size >= min_font_size:
        font = get_font(font_size)
        # Word wrap
        lines = []
        words = text.split()
        line = ''
        for word in words:
            test_line = f'{line} {word}'.strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            w = bbox[2] - bbox[0]
            if w > width - margin * 2:
                lines.append(line)
                line = word
            else:
                line = test_line
        lines.append(line)
        # Check both width and height
        max_line_width = max([draw.textbbox((0, 0), l, font=font)[2] - draw.textbbox((0, 0), l, font=font)[0] for l in lines])
        total_text_height = sum([draw.textbbox((0, 0), l, font=font)[3] - draw.textbbox((0, 0), l, font=font)[1] for l in lines])
        if total_text_height <= height - margin * 2 and max_line_width <= width - margin * 2:
            break
        font_size -= 20
    # Center text
    y = (height - total_text_height) // 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (width - w) // 2
        draw.text((x, y), line, font=font, fill=font_color)
        y += h
    img.save(output_path)
    print(f"[Card] Saved card image: {output_path} (font size used: {font_size})")

if __name__ == "__main__":
    # Example usage
    os.makedirs("cards", exist_ok=True)
    texts = [
        "This is a sample card news summary.",
        "Another impactful sentence for card news.",
        "Keep it short and punchy!"
    ]
    for idx, text in enumerate(texts, 1):
        create_card_image(text, f"cards/card_{idx}.png")
