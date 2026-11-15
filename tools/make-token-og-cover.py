#!/usr/bin/env python3
"""生成 Token 业务页的 1200×630 社交分享封面（token/assets/og-cover.jpg）。

视觉沿用站点的纸色 / 海军蓝 / 印章红：左侧标题，右侧六档费率表。
用法：python3 tools/make-token-og-cover.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "token" / "assets" / "og-cover.jpg"

W, H = 1200, 630
PAPER = (245, 244, 240)
PAPER_2 = (237, 235, 228)
NAVY = (46, 66, 128)
NAVY_DEEP = (27, 37, 64)
RED = (198, 54, 53)
RED_LIGHT = (240, 169, 168)
MUTED = (94, 98, 112)
LINE = (218, 216, 210)
WHITE = (245, 244, 240)

CJK = "/System/Library/Fonts/Hiragino Sans GB.ttc"  # 0 = W3, 2 = W6
LATIN_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
LATIN = "/System/Library/Fonts/Supplemental/Arial.ttf"


def cjk(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(CJK, size, index=2 if bold else 0)


def latin(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(LATIN_BOLD if bold else LATIN, size)


def tracked(draw, xy, text, font, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor="la")
        x += draw.textlength(ch, font=font) + tracking
    return x


def main() -> None:
    canvas = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)

    pad = 72

    # 眉标
    tracked(draw, (pad, 70), "TOKEN WHOLESALE", latin(17), NAVY, 4.6)
    draw.text((pad + 246, 70), "/", font=latin(17), fill=RED)
    tracked(draw, (pad + 264, 70), "B2B SUPPLY", latin(17), MUTED, 3.2)

    # 主标题
    draw.text((pad, 112), "大模型 Token", font=cjk(78, bold=True), fill=NAVY, anchor="la")
    draw.text((pad, 204), "额度采购", font=cjk(92, bold=True), fill=NAVY, anchor="la")

    # 红色短线
    draw.rectangle([pad, 336, pad + 64, 341], fill=RED)

    # 副标题
    draw.text((pad, 372), "文本 76 折起 · 视频 87 折起", font=cjk(27, bold=True), fill=NAVY, anchor="la")
    draw.text((pad, 418), "季度采购越高，折扣越低", font=cjk(21), fill=MUTED, anchor="la")
    draw.text((pad, 456), "一个入口，买齐主流大模型额度", font=cjk(21), fill=MUTED, anchor="la")

    # 底部数据
    draw.line([(pad, 526), (pad + 470, 526)], fill=LINE, width=1)
    draw.text((pad, 548), "6 档位 · 12 个月有效期 · 90 天报价有效期", font=cjk(20, bold=True), fill=NAVY, anchor="la")
    tracked(draw, (pad, 592), "ZHIZHUER9110.GITHUB.IO/GAME-QA-SITE/TOKEN", latin(12), MUTED, 1.9)

    # 右侧费率卡
    panel_x = 742
    panel_w = W - panel_x
    draw.rectangle([panel_x, 0, W, H], fill=NAVY)
    draw.rectangle([panel_x, 0, panel_x + 4, H], fill=RED)

    px = panel_x + 44
    tracked(draw, (px, 60), "TOKEN RATE CARD", latin(14), (196, 202, 222), 3.4)
    draw.text((W - 44, 60), "V1.0 / 2026", font=latin(11), fill=RED_LIGHT, anchor="ra")
    draw.line([(px, 96), (W - 44, 96)], fill=(80, 98, 150), width=1)

    # 表头
    draw.text((px, 112), "档位", font=cjk(13), fill=(170, 178, 202), anchor="la")
    draw.text((px + 78, 112), "季度累计实付", font=cjk(13), fill=(170, 178, 202), anchor="la")
    draw.text((W - 148, 112), "文本", font=cjk(13), fill=(170, 178, 202), anchor="ra")
    draw.text((W - 44, 112), "视频", font=cjk(13), fill=(170, 178, 202), anchor="ra")

    rows = [
        ("T1", "0.5–5 万", "95%", "95%"),
        ("T2", "5–20 万", "92%", "92%"),
        ("T3", "20–50 万", "88%", "88%"),
        ("T4", "50–100 万", "84%", "87%"),
        ("T5", "100–200 万", "80%", "87%"),
        ("T6", "200 万及以上", "76%", "87%"),
    ]

    y = 148
    row_h = 62
    for i, (tier, amount, text_pct, video_pct) in enumerate(rows):
        bottom = y + row_h
        if tier == "T6":
            draw.rectangle([px - 16, y, W - 28, bottom], fill=(74, 58, 116))
        draw.text((px, y + 16), tier, font=latin(19), fill=WHITE if tier != "T6" else RED_LIGHT, anchor="la")
        draw.text((px + 78, y + 20), amount, font=cjk(16), fill=(206, 211, 228), anchor="la")
        draw.text(
            (W - 148, y + 13),
            text_pct,
            font=latin(23),
            fill=RED_LIGHT if tier == "T6" else WHITE,
            anchor="ra",
        )
        draw.text((W - 44, y + 13), video_pct, font=latin(23), fill=WHITE, anchor="ra")
        draw.line([(px - 16, y), (W - 28, y)], fill=(66, 84, 138), width=1)
        y = bottom

    draw.line([(px - 16, y), (W - 28, y)], fill=(66, 84, 138), width=1)
    draw.text((px, 528), "官网标准价 = 100%", font=cjk(14, bold=True), fill=(196, 202, 222), anchor="la")
    draw.text((px, 556), "按自然季度累计实付（左闭右开）", font=cjk(12), fill=(150, 160, 190), anchor="la")

    # 红色印章（简洁版）
    cx, cy, r = W - 96, 586, 46
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED_LIGHT, width=3)
    draw.text((cx, cy - 14), "6 TIERS", font=latin(13), fill=RED_LIGHT, anchor="ma")
    draw.text((cx, cy + 6), "RATE CARD", font=latin(8), fill=RED_LIGHT, anchor="ma")

    canvas.save(OUT, "JPEG", quality=90, optimize=True, progressive=True)
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
