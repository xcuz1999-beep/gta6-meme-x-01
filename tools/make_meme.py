#!/usr/bin/env python3
"""Compose the gta6-meme-x-01 meme: AI scene + official make.fun ghost mark + captions.

Inputs : assets/scene-base.png (AI-generated scene, no text)
         assets/mark-1024.png (official make.fun ghost mark from make.fun/press)
Output : meme.png (1024x1024) at the repository root.
"""
from PIL import Image, ImageDraw, ImageFont

REPO = "/home/hatch/MUSE-PRO/projects/gta6-meme-x-01"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SIZE = 1024
MAX_TEXT_W = 950

TOP_LINES = ["WAITED 13 YEARS", "FOR GTA VI"]
BOTTOM_LINES = ["MY AI AGENT GOT PAID ON make.fun", "IN 13 MINUTES"]


def fit_font(draw, text, start_size):
    """Largest bold font (<= start_size) whose text fits MAX_TEXT_W."""
    size = start_size
    while size > 20:
        font = ImageFont.truetype(FONT_PATH, size)
        w = draw.textlength(text, font=font)
        if w <= MAX_TEXT_W:
            return font, size
        size -= 2
    return ImageFont.truetype(FONT_PATH, 20), 20


def draw_block(draw, lines, top_y, start_size):
    """Draw centred caption lines from top_y down; returns the y after the block."""
    # One shared size for the whole block: fit the widest line.
    size = start_size
    while size > 20:
        font = ImageFont.truetype(FONT_PATH, size)
        if max(draw.textlength(t, font=font) for t in lines) <= MAX_TEXT_W:
            break
        size -= 2
    font = ImageFont.truetype(FONT_PATH, size)
    stroke = max(3, size // 9)
    line_h = int(size * 1.18)
    y = top_y
    for text in lines:
        w = draw.textlength(text, font=font)
        draw.text(((SIZE - w) / 2, y), text, font=font, fill="white",
                  stroke_width=stroke, stroke_fill="black")
        y += line_h
    return y


def main():
    scene = Image.open(f"{REPO}/assets/scene-base.png").convert("RGB")
    scene = scene.resize((SIZE, SIZE), Image.LANCZOS)
    img = scene.convert("RGBA")

    # The official ghost, worked into the scene: floating in the sunset sky at
    # the right, above the TV, ~30% of the picture height.
    mark = Image.open(f"{REPO}/assets/mark-1024.png").convert("RGBA")
    ghost_h = int(SIZE * 0.30)
    mark = mark.resize((ghost_h, ghost_h), Image.LANCZOS)
    img.alpha_composite(mark, (SIZE - ghost_h - 28, 208))

    draw = ImageDraw.Draw(img)
    draw_block(draw, TOP_LINES, 26, 84)

    # Bottom block: measure its height first so it sits on the empty floor.
    size = 84
    while size > 20:
        font = ImageFont.truetype(FONT_PATH, size)
        if max(draw.textlength(t, font=font) for t in BOTTOM_LINES) <= MAX_TEXT_W:
            break
        size -= 2
    block_h = int(size * 1.18) * len(BOTTOM_LINES)
    draw_block(draw, BOTTOM_LINES, SIZE - block_h - 22, 84)

    img.convert("RGB").save(f"{REPO}/meme.png")
    print("wrote meme.png", img.size)


if __name__ == "__main__":
    main()
