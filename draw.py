"""Draw the 18 November 2026 world-news poster (1024x1024 PNG).

Pure PIL, deterministic: same input, same bytes, every run. No network,
no clock, no randomness. Fonts are bundled in assets/ so the program
renders identically in any sandbox.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W = H = 1024

PAPER = (247, 243, 234)
INK = (20, 20, 24)
NAVY = (20, 33, 61)
GOLD = (197, 160, 60)
RED = (178, 28, 28)
MUTED = (90, 86, 78)
SKY = (208, 226, 238)
CARD_BG = (255, 255, 255)


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = os.path.join(ASSETS, name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.truetype("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_flag(draw, x, y, w, h, kind):
    """A small flag on a pole: china, usa or russia."""
    draw.rectangle([x, y, x + 4, y + 132], fill=(60, 60, 66))
    fx, fy, fw, fh = x + 4, y, w, h
    if kind == "china":
        draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
        draw.ellipse([fx + 8, fy + 8, fx + 20, fy + 20], fill=(255, 222, 0))
    elif kind == "usa":
        for i in range(7):
            col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
            draw.rectangle([fx, fy + i * fh // 7, fx + fw, fy + (i + 1) * fh // 7], fill=col)
        draw.rectangle([fx, fy, fx + fw * 2 // 5, fy + fh * 4 // 7], fill=(60, 59, 110))
    else:  # russia
        draw.rectangle([fx, fy, fx + fw, fy + fh // 3], fill=(255, 255, 255))
        draw.rectangle([fx, fy + fh // 3, fx + fw, fy + 2 * fh // 3], fill=(0, 57, 166))
        draw.rectangle([fx, fy + 2 * fh // 3, fx + fw, fy + fh], fill=(213, 0, 50))


def draw_summit(draw, x0, y0, x1, y1):
    """Shenzhen skyline at dawn with three flags in front."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # rising sun
    draw.ellipse([x1 - 84, y0 + 16, x1 - 36, y0 + 64], fill=(240, 196, 90))
    # skyline towers, back row lighter, front row darker
    base = y1 - 96
    towers = [(x0 + 6, 150, 46), (x0 + 58, 196, 52), (x0 + 116, 128, 44),
              (x0 + 166, 178, 58), (x0 + 230, 108, 48), (x0 + 284, 168, 54)]
    for tx, th, tw in towers:
        draw.rectangle([tx, base - th, tx + tw, base], fill=(158, 178, 196))
    front = [(x0 + 30, 96, 58), (x0 + 100, 130, 62), (x0 + 176, 84, 56), (x0 + 246, 118, 60)]
    for tx, th, tw in front:
        draw.rectangle([tx, base - th, tx + tw, base], fill=(52, 66, 88))
        for wy in range(base - th + 12, base - 10, 18):
            for wx in range(tx + 8, tx + tw - 8, 16):
                draw.rectangle([wx, wy, wx + 7, wy + 8], fill=(240, 196, 90))
    # ground
    draw.rectangle([x0, base, x1, y1], fill=(38, 48, 64))
    # three flags: China, USA, Russia
    draw_flag(draw, x0 + 52, base - 148, 44, 30, "china")
    draw_flag(draw, x0 + 150, base - 148, 44, 30, "usa")
    draw_flag(draw, x0 + 248, base - 148, 44, 30, "russia")


def draw_card(draw, x, y, w, h, kicker, headline, body):
    draw.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=(210, 204, 190), width=2)
    draw.rectangle([x, y, x + 8, y + h], fill=RED)
    pad = 24
    tx = x + pad + 8
    tw = w - pad * 2 - 8
    draw.text((tx, y + 14), kicker, font=font(19, bold=True), fill=RED)
    hl = wrap(draw, headline, font(27, bold=True), tw)
    yy = text_block(draw, tx, y + 42, hl[:2], font(27, bold=True), INK, 33)
    bl = wrap(draw, body, font(21), tw)
    text_block(draw, tx, yy + 8, bl[:3], font(21), (52, 50, 46), 26)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((40, 26), "T H E   W O R L D   I N   O N E   D A Y", font=font(22, bold=True), fill=GOLD)
    d.text((40, 58), "WEDNESDAY, 18 NOVEMBER 2026", font=font(52, bold=True), fill=(255, 255, 255))
    d.rectangle([0, 144, W, 148], fill=GOLD)

    # ---- lead story: APEC opens in Shenzhen ----
    d.text((40, 172), "CHINA  ·  APEC", font=font(20, bold=True), fill=RED)
    lead_head = wrap(d, "APEC opens in Shenzhen as the world watches", font(40, bold=True), 560)
    text_block(d, 40, 202, lead_head, font(40, bold=True), INK, 48)
    lead_body = wrap(
        d,
        "Leaders of 21 Pacific economies gather as Xi Jinping chairs the "
        "summit. Trump and Putin arrive for Thursday's first three-way talks.",
        font(23), 560)
    text_block(d, 40, 202 + len(lead_head) * 48 + 12, lead_body, font(23), (52, 50, 46), 30)
    draw_summit(d, 640, 172, 984, 440)

    d.line([40, 470, 984, 470], fill=(200, 192, 176), width=2)

    # ---- four more stories ----
    cards = [
        ("ASIA  ·  QUAD",
         "Trump lands in Manila for Quad talks",
         "The U.S. president arrives in the Philippines for talks with "
         "allies, ahead of his visit to China."),
        ("MIDDLE EAST  ·  IRAN WAR",
         "Iran says a 2m-barrel tanker sank off Hormuz",
         "Tehran claims a supertanker sank after hitting a mine. "
         "Shipping is at a standstill."),
        ("ISRAEL  ·  POLITICS",
         "Knesset picks a Speaker in a blow to Netanyahu",
         "Israel's parliament elects an ally of Gadi Eisenkot as Speaker, "
         "a setback for the prime minister's camp."),
        ("DIPLOMACY  ·  TRADE",
         "Canada and China extend their trade deals",
         "Xi meets Carney ahead of APEC as the two countries agree further "
         "tariff cuts and deeper ties."),
    ]
    cw, ch = 462, 196
    positions = [(40, 488), (522, 488), (40, 694), (522, 694)]
    for (kicker, head, body), (cx, cy) in zip(cards, positions):
        draw_card(d, cx, cy, cw, ch, kicker, head, body)

    # ---- also today ----
    d.rectangle([40, 900, 984, 988], fill=NAVY)
    d.text((60, 912), "ALSO TODAY", font=font(20, bold=True), fill=GOLD)
    also = [
        "Cyclone Akvan bears down on the Bay of Bengal",
        "Baidu chief warns of an AI bubble at APEC",
        "Ukraine bridge war enters its third day",
        "Dhoni retires from the IPL",
    ]
    yy = 940
    for line in also[:2]:
        d.text((60, yy), "·  " + line, font=font(17), fill=(235, 232, 224))
        yy += 24
    yy = 940
    for line in also[2:]:
        d.text((522, yy), "·  " + line, font=font(17), fill=(235, 232, 224))
        yy += 24

    d.text((40, 998), "All stories as reported on 18 November 2026  ·  Sources: AP, Reuters, Xinhua, UKMTO",
           font=font(15), fill=MUTED)
    return img


def main():
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = render()
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
