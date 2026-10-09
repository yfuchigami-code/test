# -*- coding: utf-8 -*-
"""動画・スライド用の図表PNGを生成する。色はPGカラー（紺の濃淡・灰）のみ使用。"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
os.makedirs(OUT, exist_ok=True)

for path in ("/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf",
             "C:/Windows/Fonts/meiryo.ttc"):
    if os.path.exists(path):
        fm.fontManager.addfont(path)
        plt.rcParams["font.family"] = fm.FontProperties(fname=path).get_name()
        break
plt.rcParams["axes.unicode_minus"] = False

NAVY, MID, LIGHT, GRAY, TXT = "#273771", "#7A86B3", "#B9BFD8", "#808080", "#404040"
CO = ["ネクステージ", "IDOM", "ケーユーHD"]


def base(figsize=(9.2, 4.9)):
    fig, ax = plt.subplots(figsize=figsize, dpi=200)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRAY)
    ax.tick_params(axis="x", labelsize=15, colors=TXT, length=0)
    ax.tick_params(axis="y", left=False, labelleft=False)
    return fig, ax


def finish(fig, name, note):
    fig.text(0.01, 0.01, note, fontsize=10, color=GRAY, ha="left", va="bottom")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(OUT, name), transparent=False, facecolor="white")
    plt.close(fig)


def bars(ax, xs, vals, colors, fmt, width=0.55, pad=0.02):
    rects = ax.bar(xs, vals, width=width, color=colors)
    top = max(abs(v) for v in vals)
    for r, v in zip(rects, vals):
        y = r.get_height()
        off = top * pad
        ax.text(r.get_x() + r.get_width() / 2, y + (off if v >= 0 else -off),
                fmt(v), ha="center", va="bottom" if v >= 0 else "top",
                fontsize=18, color=TXT, fontweight="bold")
    return rects


# 1 売上高
fig, ax = base()
bars(ax, CO, [6520, 5628, 1691], [NAVY, MID, LIGHT], lambda v: f"{v:,}億円")
ax.set_ylim(0, 7600)
finish(fig, "01_売上高.png",
       "出所：各社決算短信・決算説明資料（ネクステージ2025年11月期／IDOM2026年2月期／ケーユーHD2026年3月期）")

# 2 営業利益の伸び率
fig, ax = base()
vals = [51.4, 1.6, -8.8]
bars(ax, CO, vals, [NAVY, MID, LIGHT], lambda v: f"{v:+.1f}%")
ax.axhline(0, color=GRAY, lw=1)
ax.set_ylim(-16, 62)
finish(fig, "02_営業利益の伸び率.png", "出所：各社決算短信（前期比）。決算期は各社で異なる")

# 3 営業利益率
fig, ax = base()
bars(ax, CO, [3.0, 3.6, 5.0], [NAVY, MID, LIGHT], lambda v: f"{v:.1f}%")
ax.set_ylim(0, 6.2)
finish(fig, "03_営業利益率.png", "出所：各社決算短信の売上高・営業利益から算出した概算")

# 4 台数の伸びと営業利益の伸び
fig, ax = base()
import numpy as np
x = np.arange(2)
w = 0.34
v_units = [4.0, 10.0]
v_op = [51.4, 1.6]
r1 = ax.bar(x - w / 2, v_units, w, color=LIGHT, label="小売台数の伸び")
r2 = ax.bar(x + w / 2, v_op, w, color=NAVY, label="営業利益の伸び")
for rs, vs in ((r1, v_units), (r2, v_op)):
    for r, v in zip(rs, vs):
        ax.text(r.get_x() + r.get_width() / 2, v + 1, f"+{v:.1f}%".replace(".0%", "%"),
                ha="center", fontsize=18, color=TXT, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(["ネクステージ", "IDOM"])
ax.set_ylim(0, 62)
ax.legend(frameon=False, fontsize=14, loc="upper right")
finish(fig, "04_台数と営業利益の伸び.png",
       "出所：各社決算資料。ネクステージは前年比104.0%、IDOMは前期比約+10%（直営店）")

# 5 買取台数と小売台数（ネクステージ）
fig, ax = base()
bars(ax, ["買取台数", "小売販売台数"], [283017, 184823], [NAVY, MID], lambda v: f"{v:,}台", width=0.45)
ax.set_ylim(0, 330000)
finish(fig, "05_買取と小売台数.png", "出所：ネクステージ統合報告書（2025年11月期）")

# 6 事業別売上総利益（ネクステージ）
fig, ax = base()
bars(ax, ["販売店", "買取店", "整備店"], [499, 375, 103], [NAVY, MID, LIGHT], lambda v: f"{v:,}億円", width=0.5)
for xi, t in enumerate(["前年比109.0%", "前年比111.3%", "前年比123.9%"]):
    ax.text(xi, -60, t, ha="center", fontsize=13, color=GRAY)
ax.set_ylim(-90, 580)
finish(fig, "06_事業別売上総利益.png", "出所：ネクステージ統合報告書（2025年11月期）")

# 7 ROEと自己資本比率
fig, ax = base()
x = np.arange(3)
roe = [16.0, 14.2, 8.0]
eq = [34.9, 33.4, 73.0]
r1 = ax.bar(x - w / 2, roe, w, color=NAVY, label="ROE（概算を含む）")
r2 = ax.bar(x + w / 2, eq, w, color=LIGHT, label="自己資本比率")
for rs, vs in ((r1, roe), (r2, eq)):
    for r, v in zip(rs, vs):
        ax.text(r.get_x() + r.get_width() / 2, v + 1.2, f"{v:.1f}%", ha="center",
                fontsize=16, color=TXT, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(CO)
ax.set_ylim(0, 85)
ax.legend(frameon=False, fontsize=14, loc="upper left")
finish(fig, "07_ROEと自己資本比率.png",
       "出所：決算短信等から算出。ネクステージ・ケーユーのROEは概算、IDOMは第三者サイト掲載値")

print("done:", sorted(os.listdir(OUT)))
