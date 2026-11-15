#!/usr/bin/env python3
"""生成「交付保障」列表项的示例预览图（占位）。

输出：assets/img/tips/*.jpg（900×560）
替换同名图片即可换成真实截图，不需要改 HTML。
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "tips"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 900, 560
PAPER = (245, 244, 240)
PAPER_2 = (237, 235, 228)
CARD = (251, 250, 247)
NAVY = (46, 66, 128)
NAVY_DEEP = (27, 37, 64)
RED = (198, 54, 53)
RED_LIGHT = (224, 135, 133)
MUTED = (94, 98, 112)
LINE = (214, 212, 205)
SOFT = (224, 222, 215)
PALE = (232, 230, 223)

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


def block(draw, x, y, w, h=6, color=SOFT):
    draw.rectangle([x, y, x + w, y + h], fill=color)


def sheet(draw, x0=40, y0=214, x1=860, y1=508):
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=LINE, width=1)


def frame(title, subtitle, index):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # 顶部色带
    d.rectangle([0, 0, W, 58], fill=NAVY)
    tracked(d, (40, 22), "GAME QA · DELIVERABLE SAMPLE", latin(11), (226, 229, 238), 2.0)
    d.text((W - 40, 19), "示例图", font=cjk(12, bold=True), fill=(240, 169, 168), anchor="ra")
    # 标题
    d.text((40, 84), title, font=cjk(42, bold=True), fill=NAVY, anchor="la")
    d.text((40, 140), subtitle, font=cjk(16), fill=MUTED, anchor="la")
    d.rectangle([40, 178, 96, 183], fill=RED)
    d.text((W - 40, 158), f"0{index:02d}" if index < 100 else str(index), font=latin(13), fill=LINE, anchor="ra")
    sheet(d)
    # 页脚
    d.line([(40, 524), (860, 524)], fill=LINE, width=1)
    d.text((40, 532), "示例图片 · 可替换为真实截图", font=cjk(11), fill=MUTED, anchor="la")
    tracked(d, (W - 40 - 150, 533), "GAME QA SERVICE", latin(9), MUTED, 1.7)
    return img, d


def image_doc(title, subtitle, index, bars, stats, chart_label):
    img, d = frame(title, subtitle, index)
    # 左侧摘要
    tracked(d, (64, 236), "EXECUTIVE SUMMARY", latin(9), RED, 2.2)
    widths = [318, 292, 330, 248]
    for i, w in enumerate(widths):
        block(d, 64, 262 + i * 22, w, 6, SOFT if i < 3 else PALE)
    # 统计
    sx = 64
    for i, (num, label) in enumerate(stats):
        x = sx + i * 128
        d.text((x, 380), num, font=latin(26), fill=NAVY, anchor="la")
        d.text((x, 414), label, font=cjk(11), fill=MUTED, anchor="la")
        if i:
            d.line([(x - 14, 382), (x - 14, 424)], fill=LINE, width=1)
    # 右侧图表
    cx0, cy0, cx1, cy1 = 488, 234, 840, 484
    d.rectangle([cx0, cy0, cx1, cy1], fill=PAPER_2, outline=LINE, width=1)
    d.text((cx0 + 18, cy0 + 14), chart_label, font=cjk(12, bold=True), fill=NAVY, anchor="la")
    d.text((cx1 - 18, cy0 + 15), "近 5 个版本", font=cjk(10), fill=MUTED, anchor="ra")
    base_y = 446
    d.line([(cx0 + 22, base_y), (cx1 - 22, base_y)], fill=LINE, width=1)
    max_v = max(bars)
    bw = 30
    gap = 30
    start = cx0 + 48
    for i, v in enumerate(bars):
        h = int((v / max_v) * 126)
        x = start + i * (bw + gap)
        color = RED if i == len(bars) - 1 else NAVY
        d.rectangle([x, base_y - h, x + bw, base_y], fill=color)
        d.text((x + bw / 2, base_y + 10), f"V{i + 1}", font=latin(9), fill=MUTED, anchor="ma")
        d.text((x + bw / 2, base_y - h - 14), str(v), font=latin(9), fill=MUTED, anchor="ma")
    return img


def image_list():
    img, d = frame("Bug 清单", "缺陷跟踪 · 级别、状态与责任模块", 5)
    data = [
        ("QA-1042", "战斗", "技能冷却偶发不刷新", "P0", "已修复"),
        ("QA-1043", "登录", "弱网下登录超时无提示", "P1", "待验证"),
        ("QA-1044", "背包", "道具数量显示不一致", "P1", "处理中"),
        ("QA-1045", "副本", "结算界面偶现白屏", "P0", "已修复"),
        ("QA-1046", "UI", "小屏机型按钮遮挡", "P2", "待排期"),
    ]
    cols = [64, 168, 300, 660, 750]
    heads = ["ID", "模块", "描述", "级别", "状态"]
    for i, h in enumerate(heads):
        d.text((cols[i], 238), h, font=cjk(10, bold=True), fill=MUTED, anchor="la")
    d.line([(64, 260), (836, 260)], fill=LINE, width=1)
    for r, (bid, mod, desc, lvl, status) in enumerate(data):
        y = 278 + r * 40
        d.text((cols[0], y), bid, font=latin(11), fill=NAVY, anchor="la")
        d.text((cols[1], y - 1), mod, font=cjk(11), fill=MUTED, anchor="la")
        d.text((cols[2], y - 1), desc, font=cjk(11), fill=NAVY_DEEP, anchor="la")
        badge_color = RED if lvl == "P0" else (RED_LIGHT if lvl == "P1" else LINE)
        d.rectangle([cols[3], y - 2, cols[3] + 30, y + 15], fill=badge_color)
        d.text((cols[3] + 15, y + 6), lvl, font=latin(8), fill=(255, 255, 255), anchor="mm")
        d.text((cols[4], y - 1), status, font=cjk(10), fill=MUTED, anchor="la")
        d.line([(64, y + 25), (836, y + 25)], fill=PALE, width=1)
    d.text((64, 490), "共 42 条 · 仅展示前 5 条", font=cjk(10), fill=MUTED, anchor="la")
    return img


def image_plan():
    img, d = frame("测试计划", "版本 v2.4 · 提前 3 个工作日输出", 3)
    d.text((64, 236), "关键里程碑", font=cjk(12, bold=True), fill=NAVY, anchor="la")
    line_y = 292
    d.line([(96, line_y), (804, line_y)], fill=LINE, width=2)
    nodes = [
        ("D-5", "需求评审", "范围与验收口径"),
        ("D-3", "用例设计", "用例评审通过"),
        ("D-1", "测试执行", "功能 / 兼容回归"),
        ("D0", "上线回归", "发布前最终确认"),
    ]
    for i, (day, name, note) in enumerate(nodes):
        x = 120 + i * 220
        d.ellipse([x - 9, line_y - 9, x + 9, line_y + 9], fill=PAPER, outline=NAVY, width=3)
        d.text((x, line_y - 36), day, font=latin(11), fill=RED, anchor="ma")
        cx = x - 82
        d.rectangle([cx, 326, cx + 168, 402], fill=PAPER_2, outline=LINE, width=1)
        d.text((cx + 14, 338), name, font=cjk(12, bold=True), fill=NAVY, anchor="la")
        d.text((cx + 14, 362), note, font=cjk(10), fill=MUTED, anchor="la")
        block(d, cx + 14, 382, 112, 5, SOFT)
    # 甘特
    d.text((64, 432), "排期", font=cjk(11, bold=True), fill=NAVY, anchor="la")
    rows = [("用例设计", 0, 36), ("功能测试", 28, 56), ("兼容测试", 48, 78), ("上线回归", 78, 96)]
    for i, (label, s, e) in enumerate(rows):
        y = 454 + i * 14
        d.text((120, y - 2), label, font=cjk(9), fill=MUTED, anchor="la")
        d.rectangle([300, y, 800, y + 6], fill=PAPER_2)
        d.rectangle([300 + int(s * 5), y, 300 + int(e * 5), y + 6], fill=NAVY if i < 3 else RED)
    return img


def image_daily():
    img, d = frame("测试日报", "版本 v2.4 · 当日执行与风险同步", 7)
    stats = [("128", "执行用例"), ("116", "通过"), ("12", "新增缺陷")]
    for i, (num, label) in enumerate(stats):
        x = 64 + i * 268
        d.rectangle([x, 236, x + 240, 318], fill=PAPER_2, outline=LINE, width=1)
        d.text((x + 18, 252), num, font=latin(30), fill=NAVY if i < 2 else RED, anchor="la")
        d.text((x + 18, 292), label, font=cjk(10), fill=MUTED, anchor="la")
    d.text((64, 348), "通过率", font=cjk(10, bold=True), fill=MUTED, anchor="la")
    d.rectangle([120, 350, 836, 358], fill=PAPER_2)
    d.rectangle([120, 350, 120 + int(716 * 0.906), 358], fill=NAVY)
    d.text((836, 342), "90.6%", font=latin(10), fill=NAVY, anchor="ra")
    items = [
        ("战斗", "技能冷却问题已修复，等待复测"),
        ("兼容", "新增 2 台折叠屏机型，通过"),
        ("性能", "主城同屏帧率低于基线 4 帧"),
        ("风险", "次日 10:00 前需给出修复结论"),
    ]
    for i, (tag, text) in enumerate(items):
        y = 390 + i * 28
        d.rectangle([64, y + 4, 70, y + 10], fill=RED if i == 3 else NAVY)
        d.text((82, y), tag, font=cjk(10, bold=True), fill=NAVY, anchor="la")
        d.text((132, y), text, font=cjk(11), fill=MUTED, anchor="la")
    return img


def image_weekly():
    img, d = frame("测试周报", "第 46 周 · 进度、风险与下周计划", 8)
    d.text((64, 236), "本周执行趋势", font=cjk(12, bold=True), fill=NAVY, anchor="la")
    base_y = 390
    d.line([(64, base_y), (560, base_y)], fill=LINE, width=1)
    vals = [74, 96, 88, 112, 104, 62, 40]
    for i, v in enumerate(vals):
        h = int(v * 0.95)
        x = 78 + i * 66
        d.rectangle([x, base_y - h, x + 34, base_y], fill=NAVY if i < 5 else LINE)
        d.text((x + 17, base_y + 8), ["一", "二", "三", "四", "五", "六", "日"][i], font=cjk(9), fill=MUTED, anchor="ma")
    # 右侧结论
    x = 610
    d.rectangle([x, 236, 840, 490], fill=PAPER_2, outline=LINE, width=1)
    d.text((x + 18, 252), "本周结论", font=cjk(11, bold=True), fill=NAVY, anchor="la")
    block(d, x + 18, 280, 190, 5, SOFT)
    block(d, x + 18, 298, 160, 5, SOFT)
    block(d, x + 18, 316, 174, 5, SOFT)
    d.text((x + 18, 352), "风险", font=cjk(11, bold=True), fill=RED, anchor="la")
    block(d, x + 18, 378, 180, 5, SOFT)
    block(d, x + 18, 396, 150, 5, SOFT)
    d.text((x + 18, 432), "下周计划", font=cjk(11, bold=True), fill=NAVY, anchor="la")
    block(d, x + 18, 458, 168, 5, SOFT)
    return img


def image_process():
    img, d = frame("过程文档", "用例、报告与过程记录完整归档", 6)
    # 叠放文档
    offsets = [(86, 250, 300, 470), (110, 238, 500, 460), (134, 226, 700, 450)]
    labels = ["过程记录", "测试报告", "测试用例"]
    for i, (x0, y0, x1, y1) in enumerate(offsets):
        d.rectangle([x0, y0, x1, y1], fill=CARD, outline=LINE, width=1)
        d.rectangle([x0, y0, x1, y0 + 26], fill=NAVY)
        d.text((x0 + 12, y0 + 7), labels[i], font=cjk(9, bold=True), fill=PAPER, anchor="la")
    # 最上层内容
    x0, y0, x1, y1 = offsets[2]
    for i in range(5):
        block(d, x0 + 16, y0 + 44 + i * 24, 220 - i * 12, 5, SOFT)
    d.text((x0 + 16, y1 - 30), f"共 {1286:,} 条", font=cjk(9), fill=MUTED, anchor="la")
    # 右侧统计
    d.text((560, 260), "归档完整度", font=cjk(11, bold=True), fill=NAVY, anchor="la")
    d.text((560, 288), "100%", font=latin(40), fill=RED, anchor="la")
    d.text((560, 346), "用例 / 报告 / 记录 / 缺陷", font=cjk(10), fill=MUTED, anchor="la")
    d.line([(560, 382), (840, 382)], fill=LINE, width=1)
    for i, t in enumerate(["测试用例库", "版本测试报告", "过程会议记录"]):
        d.text((560, 402 + i * 28), "—", font=cjk(10), fill=RED, anchor="la")
        d.text((580, 402 + i * 28), t, font=cjk(10), fill=NAVY_DEEP, anchor="la")
    return img


def image_cases():
    img, d = frame("测试用例库", "1,286 条用例 · 按模块与优先级维护", 9)
    d.text((64, 236), "用例库 / 最近维护", font=cjk(11, bold=True), fill=NAVY, anchor="la")
    cards = [
        ("TC-012", "登录态失效", "P0"), ("TC-027", "技能冷却", "P1"),
        ("TC-041", "背包容量", "P1"), ("TC-058", "副本结算", "P0"),
        ("TC-073", "支付回调", "P0"), ("TC-086", "弱网重连", "P2"),
    ]
    for i, (cid, name, prio) in enumerate(cards):
        col, row = i % 3, i // 3
        x = 64 + col * 264
        y = 270 + row * 112
        d.rectangle([x, y, x + 240, y + 92], fill=PAPER_2, outline=LINE, width=1)
        d.text((x + 14, y + 12), cid, font=latin(10), fill=RED, anchor="la")
        d.text((x + 14, y + 34), name, font=cjk(12, bold=True), fill=NAVY, anchor="la")
        d.text((x + 14, y + 62), f"优先级 {prio}", font=cjk(9), fill=MUTED, anchor="la")
        d.rectangle([x + 200, y + 14, x + 226, y + 28], fill=NAVY)
        d.text((x + 213, y + 21), "通过", font=cjk(7), fill=PAPER, anchor="mm")
    return img


def image_automation():
    img, d = frame("自动化脚本沉淀", "回归脚本、断言与执行记录", 10)
    d.rectangle([64, 234, 836, 486], fill=NAVY_DEEP)
    for i in range(3):
        d.ellipse([80 + i * 16, 248, 88 + i * 16, 256], fill=LINE if i else RED)
    d.text((150, 248), "regression.spec.ts", font=latin(10), fill=(200, 207, 226), anchor="la")
    lines = [
        (14, "describe", 150, NAVY), (28, "test", 120, RED_LIGHT),
        (42, "expect", 180, (200, 207, 226)), (56, "click", 96, (150, 160, 190)),
        (70, "expect", 160, (200, 207, 226)), (84, "close", 80, (150, 160, 190)),
    ]
    for i, (indent, word, width, color) in enumerate(lines):
        y = 286 + i * 26
        d.text((82, y), f"{i + 1:02d}", font=latin(8), fill=(110, 120, 150), anchor="la")
        d.rectangle([112 + indent, y + 2, 112 + indent + width, y + 10], fill=color)
    d.text((82, 456), "通过率 98.2% · 本次执行 214 条", font=cjk(9), fill=(180, 188, 212), anchor="la")
    return img


def image_retro():
    img, d = frame("线上问题复盘", "问题、原因与改进动作", 11)
    cols = [
        ("问题", ["登录超时无提示", "结算偶现白屏", "小屏按钮遮挡"]),
        ("原因", ["弱网异常未兜底", "资源加载竞态", "适配断点缺失"]),
        ("改进", ["补充异常提示", "增加兜底重试", "扩展小屏用例"]),
    ]
    for i, (head, rows) in enumerate(cols):
        x = 64 + i * 268
        d.rectangle([x, 234, x + 240, 490], fill=PAPER_2, outline=LINE, width=1)
        d.rectangle([x, 234, x + 240, 238], fill=RED if i == 2 else NAVY)
        d.text((x + 16, 250), head, font=cjk(11, bold=True), fill=NAVY, anchor="la")
        for r, text in enumerate(rows):
            y = 286 + r * 64
            d.text((x + 16, y), f"0{r + 1}", font=latin(9), fill=RED, anchor="la")
            d.text((x + 40, y - 2), text, font=cjk(11), fill=NAVY_DEEP, anchor="la")
            block(d, x + 16, y + 26, 180, 5, SOFT)
            if r < 2:
                d.line([(x + 16, y + 48), (x + 224, y + 48)], fill=PALE, width=1)
    return img


def main():
    items = [
        ("test-plan", image_plan),
        ("daily-report", image_daily),
        ("weekly-report", image_weekly),
        ("test-report", lambda: image_doc(
            "测试报告", "版本 v2.4 · 功能与回归测试汇总", 4,
            [32, 26, 18, 12, 7], [("1,286", "用例执行"), ("96.4%", "通过率"), ("12", "遗留缺陷")],
            "缺陷趋势",
        )),
        ("bug-list", image_list),
        ("process-docs", image_process),
        ("special-report", lambda: image_doc(
            "专项测试报告", "兼容性 / 性能专项结论", 12,
            [18, 15, 11, 8, 4], [("218", "覆盖机型"), ("99.1%", "通过率"), ("2", "阻塞问题")],
            "问题分布",
        )),
        ("quality-report", lambda: image_doc(
            "版本质量评估报告", "发布前质量结论与风险提示", 13,
            [24, 19, 13, 9, 3], [("4.6", "质量评分"), ("A", "发布建议"), ("1", "高风险项")],
            "风险趋势",
        )),
        ("test-cases", image_cases),
        ("automation", image_automation),
        ("retro", image_retro),
    ]
    for name, maker in items:
        img = maker()
        path = OUT / f"{name}.jpg"
        img.save(path, "JPEG", quality=88, optimize=True, progressive=True)
        print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
