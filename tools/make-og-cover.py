#!/usr/bin/env python3
"""生成 1200×630 社交分享封面（assets/img/og-cover.jpg）。

站点 og:image 需要绝对地址且推荐 1200×630，故单独合成一张：
纸色底 + 海军蓝标题 + 右侧灰度照片，与站点设计系统保持一致。

用法：python3 tools/make-og-cover.py
"""
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "img" / "players.jpg"
OUT = ROOT / "assets" / "img" / "og-cover.jpg"

W, H = 1200, 630
PAPER = (245, 244, 240)
NAVY = (46, 66, 128)
RED = (198, 54, 53)
MUTED = (94, 98, 112)

CJK = "/System/Library/Fonts/Hiragino Sans GB.ttc"  # 0 = W3, 2 = W6
LATIN_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def cjk(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(CJK, size, index=2 if bold else 0)


def latin(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(LATIN_BOLD, size)


def tracked(draw, xy, text, font, fill, tracking):
    """逐字绘制，实现字距；返回结束 x。"""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor="la")
        x += draw.textlength(ch, font=font) + tracking
    return x


def photo_panel(width: int) -> Image.Image:
    im = Image.open(SRC).convert("RGB")
    # 等比裁切填满目标面板
    scale = max(width / im.width, H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left = (im.width - width) // 2
    top = (im.height - H) // 2
    im = im.crop((left, top, left + width, top + H))

    gray = im.convert("L").convert("RGB")
    tint = ImageChops.multiply(gray, Image.new("RGB", gray.size, NAVY))
    return Image.blend(gray, tint, 0.35)


def main() -> None:
    canvas = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)

    # 右侧照片面板
    panel_w = 516
    canvas.paste(photo_panel(panel_w), (W - panel_w, 0))
    draw.line([(W - panel_w, 0), (W - panel_w, H)], fill=(46, 66, 128, 40), width=1)

    pad = 72
    # 眉标
    tracked(draw, (pad, 82), "GAME QA SERVICE", latin(18), NAVY, 5)
    # 主标题
    draw.text((pad, 122), "游戏测试服务", font=cjk(84, bold=True), fill=NAVY, anchor="la")
    # 红色短线
    draw.rectangle([pad, 246, pad + 64, 251], fill=RED)
    # 副标题
    draw.text((pad, 288), "为研发提供专业、灵活、可靠的质量保障，", font=cjk(27), fill=MUTED, anchor="la")
    draw.text((pad, 334), "覆盖功能 / 兼容 / 定制 / 海外测试。", font=cjk(27), fill=MUTED, anchor="la")
    # 分隔细线
    draw.line([(pad, 424), (pad + 468, 424)], fill=(46, 66, 128, 41), width=1)
    # 关键数据
    draw.text(
        (pad, 452),
        "15 年经验 · 20+ 项目 · 6 大品类",
        font=cjk(24, bold=True),
        fill=NAVY,
        anchor="la",
    )
    # 底部网址
    tracked(draw, (pad, 556), "ZHIZHUER9110.GITHUB.IO/GAME-QA-SITE", latin(15), MUTED, 2.4)

    canvas.save(OUT, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
