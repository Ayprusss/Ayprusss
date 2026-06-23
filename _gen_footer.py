#!/usr/bin/env python3
"""Animated ASCII snowy-mountain footer SVG (grayscale, SMIL animation).

Mountains: a hand-tuned, asymmetric, overlapping silhouette filled with '#'
(natural monospace width -- no glyph stretching, so it can never collapse into
solid bars). A white cap layer sits on the top edge of every ridge for snow,
over a white->gray body gradient. Snow falls in front; stars twinkle behind.
"""
import bisect
import random

W, H = 900, 240
FS = 20
LINE_H = 16
Y0 = 60
GROUND_Y = 206
CX = W / 2
FILL = "#"

# --- hand-tuned skyline (x, top_row); smaller row = taller -----------------
pts = [(0, 8), (5, 6), (9, 7), (14, 3), (18, 4), (22, 1), (24, 0), (27, 2),
       (31, 3), (35, 6), (39, 5), (43, 7), (47, 4), (50, 2), (52, 3), (56, 6),
       (60, 5), (64, 7), (68, 6), (72, 8)]
N = pts[-1][0] + 1
xs = [p[0] for p in pts]
R = 10

def surf(x):
    i = bisect.bisect_right(xs, x) - 1
    x0, r0 = pts[i]
    x1, r1 = pts[min(i + 1, len(pts) - 1)]
    return r0 if x1 == x0 else round(r0 + (r1 - r0) * (x - x0) / (x1 - x0))

S = [surf(x) for x in range(N)]

# body (everything below the ridge) and cap (the top ridge cell) per row
body = ["".join(FILL if r > S[x] else " " for x in range(N)) for r in range(R)]
cap = ["".join(FILL if r == S[x] else " " for x in range(N)) for r in range(R)]

# white snowy summit -> dark rocky base
fills = ["#f6f8fa", "#e6edf3", "#cdd9e5", "#aeb9c5", "#8b949e",
         "#717b85", "#5c656e", "#49515a", "#3a414a", "#2d333b"]

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# --- snow ------------------------------------------------------------------
random.seed(7)
flakes = []
for _ in range(38):
    x = round(random.uniform(4, W - 4), 1)
    fs = random.randint(9, 16)
    dur = round(random.uniform(5.0, 11.0), 2)
    begin = round(-random.uniform(0, dur), 2)
    drift = round(random.uniform(-7, 7), 1)
    ddur = round(random.uniform(2.2, 4.5), 2)
    ch = random.choice(["*", ".", "+", "·", "•", "'", "`"])
    flakes.append((x, fs, dur, begin, drift, ddur, ch))

# --- twinkling stars -------------------------------------------------------
random.seed(21)
stars = [(round(random.uniform(20, W - 20), 1), round(random.uniform(12, 50), 1),
          round(random.uniform(2.5, 5.0), 2), round(-random.uniform(0, 4), 2))
         for _ in range(12)]

# --- emit ------------------------------------------------------------------
out = ['<?xml version="1.0" encoding="UTF-8"?>',
       f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" '
       f'role="img" aria-label="Animated ASCII snowy mountains">',
       f'  <rect width="{W}" height="{H}" fill="#0d1117"/>']

out.append('  <g font-family="monospace" font-size="11" fill="#6e7681">')
for x, y, dur, begin in stars:
    out.append(f'    <text x="{x}" y="{y}" text-anchor="middle">.'
               f'<animate attributeName="opacity" values="0.12;0.8;0.12" '
               f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></text>')
out.append('  </g>')

out.append(f'  <g font-family="monospace" font-size="{FS}" xml:space="preserve" '
           f'text-anchor="middle">')
# body gradient
for r in range(R):
    out.append(f'    <text x="{CX}" y="{Y0 + r * LINE_H}" fill="{fills[r]}">'
               f'{esc(body[r])}</text>')
# snow caps (white, on top)
for r in range(R):
    out.append(f'    <text x="{CX}" y="{Y0 + r * LINE_H}" fill="#ffffff">'
               f'{esc(cap[r])}</text>')
out.append('  </g>')

out.append(f'  <line x1="0" y1="{GROUND_Y}" x2="{W}" y2="{GROUND_Y}" '
           f'stroke="#30363d" stroke-width="1"/>')

out.append('  <g font-family="monospace" fill="#ffffff">')
for x, fs, dur, begin, drift, ddur, ch in flakes:
    out.append(
        f'    <text x="{x}" y="-10" font-size="{fs}" text-anchor="middle" opacity="0">'
        f'{esc(ch)}'
        f'<animate attributeName="y" values="-10;{GROUND_Y + 4}" '
        f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;0.85;0.85;0" '
        f'keyTimes="0;0.08;0.9;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
        f'<animate attributeName="x" values="{x};{round(x + drift, 1)};{x}" '
        f'dur="{ddur}s" begin="{begin}s" repeatCount="indefinite"/>'
        f'</text>')
out.append('  </g>')

out.append('</svg>')

with open("snowy-mountain.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")

# ASCII preview to stdout (cap shown as 'o' so the snow line is visible)
print("PREVIEW (o = snow cap, # = rock):\n")
for r in range(R):
    print("".join("o" if cap[r][x] == FILL else (body[r][x]) for x in range(N)))
print("\nwrote snowy-mountain.svg")
