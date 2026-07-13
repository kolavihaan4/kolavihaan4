"""
Terminal boot-sequence portrait (left hero panel) — pure SVG <text> so it
renders on GitHub (no embedded base64 image, which GitHub strips).

Alignment: each row is stretched to EXACTLY len*CELL_W via textLength +
lengthAdjust="spacing", so every char occupies CELL_W and columns stay vertical.
Boot: titlebar -> types `sudo ./launch --profile vihaan` -> `> launching…`
-> portrait reveals row-by-row -> freezes.  STATIC=1 = frozen preview.
"""
import html, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "ascii-art.txt")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "vihaan-ascii.svg")
STATIC = bool(os.environ.get("STATIC"))

lines = [l.rstrip() for l in open(SRC, encoding="utf-8", errors="replace").read().split("\n")]
while lines and not lines[-1].strip(): lines.pop()
while lines and not lines[0].strip(): lines.pop(0)
COLS = max(len(l) for l in lines)
ROWS = len(lines)

# smaller: tighter cells
CELL_W = 2.0
CELL_H = 3.7
PAD = 16
TITLEBAR_H = 28
BOOT_H = 46
STATUS_H = 26
ART_W = COLS * CELL_W
ART_H = ROWS * CELL_H
CANVAS_W = ART_W + PAD * 2
CANVAS_H = TITLEBAR_H + BOOT_H + ART_H + STATUS_H + PAD

BG2, BG = "#111722", "#0d1117"
FRAME = "#30363d"; MUTED = "#7d8590"; INK = "#ffffff"
GREEN = "#7ee787"; CYAN = "#22d3ee"; CURSOR = "#c9d1d9"
CMD = "sudo ./launch --profile vihaan"

type_speed = 0.042
cmd_start = 0.4
cmd_dur = len(CMD) * type_speed
cmd_done = cmd_start + cmd_dur
out_start = cmd_done + 0.35
art_start = out_start + 0.5
STAGGER = 0.011
ROW_DUR = 0.09

p = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W:.0f}" height="{CANVAS_H:.0f}" '
    f'viewBox="0 0 {CANVAS_W:.0f} {CANVAS_H:.0f}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{CANVAS_W:.0f}" height="{CANVAS_H:.0f}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{CANVAS_W-1:.0f}" height="{CANVAS_H-1:.0f}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W:.0f}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    p.append(f'<circle cx="{PAD + i*15}" cy="{TITLEBAR_H/2}" r="4.5" fill="{c}"/>')
p.append(f'<text x="{CANVAS_W/2:.0f}" y="{TITLEBAR_H/2+4}" fill="{MUTED}" font-size="11" text-anchor="middle">vihaan@github</text>')

y1 = TITLEBAR_H + 24
prompt = f'<tspan fill="{GREEN}">vihaan@github</tspan><tspan fill="{MUTED}">:~$</tspan> '
prompt_px = 118
if STATIC:
    p.append(f'<text x="{PAD}" y="{y1}" font-size="12.5">{prompt}<tspan fill="{CYAN}">{html.escape(CMD)}</tspan></text>')
else:
    cmd_px = len(CMD) * 7.1
    p.append(
        f'<text x="{PAD}" y="{y1}" font-size="12.5">{prompt}</text>'
        f'<clipPath id="cmdclip"><rect x="{PAD+prompt_px}" y="{y1-12}" width="0" height="16">'
        f'<animate attributeName="width" from="0" to="{cmd_px:.0f}" begin="{cmd_start}s" dur="{cmd_dur:.2f}s" fill="freeze" calcMode="linear"/></rect></clipPath>'
        f'<g clip-path="url(#cmdclip)"><text x="{PAD+prompt_px}" y="{y1}" font-size="12.5" fill="{CYAN}">{html.escape(CMD)}</text></g>'
        f'<rect x="{PAD+prompt_px}" y="{y1-10}" width="7" height="12" fill="{CURSOR}">'
        f'<animate attributeName="x" from="{PAD+prompt_px}" to="{PAD+prompt_px+cmd_px:.0f}" begin="{cmd_start}s" dur="{cmd_dur:.2f}s" fill="freeze" calcMode="linear"/>'
        f'<animate attributeName="opacity" values="1;1;0;0;1" dur="1s" begin="{cmd_done:.2f}s" repeatCount="6"/></rect>'
    )

y2 = y1 + 20
status2 = f'<tspan fill="{MUTED}">&#8250;</tspan> <tspan fill="{INK}">launching profile</tspan><tspan fill="{CYAN}"> vihaan</tspan><tspan fill="{MUTED}"> …</tspan>'
if STATIC:
    p.append(f'<text x="{PAD}" y="{y2}" font-size="11.5">{status2}</text>')
else:
    p.append(f'<g opacity="0"><text x="{PAD}" y="{y2}" font-size="11.5">{status2}</text><animate attributeName="opacity" from="0" to="1" begin="{out_start:.2f}s" dur="0.3s" fill="freeze"/></g>')

art_top = TITLEBAR_H + BOOT_H
font_size = CELL_H * 1.05

# Build all rows as ONE group of static <text> (no per-row animation).
rows_svg = []
for ry, line in enumerate(lines):
    n = len(line)
    if n == 0:
        continue
    ty = art_top + ry * CELL_H + CELL_H * 0.82
    row_w = n * CELL_W
    safe = html.escape(line)
    rows_svg.append(
        f'<text xml:space="preserve" x="{PAD}" y="{ty:.2f}" fill="{INK}" '
        f'font-size="{font_size:.2f}" textLength="{row_w:.2f}" lengthAdjust="spacing">{safe}</text>'
    )
art_group = "".join(rows_svg)

if STATIC:
    p.append(art_group)
else:
    # single one-shot clip that grows top->bottom, then FREEZES. Because the
    # whole art is one <g> revealed by one clipPath, only ONE animation runs,
    # and after it freezes there is nothing repainting during scroll.
    p.append(f'<clipPath id="artclip"><rect x="{PAD}" y="{art_top:.1f}" width="{ART_W:.0f}" height="0">'
             f'<animate attributeName="height" from="0" to="{ART_H:.0f}" begin="{art_start:.2f}s" '
             f'dur="1.5s" fill="freeze" calcMode="linear"/></rect></clipPath>')
    p.append(f'<g clip-path="url(#artclip)">{art_group}</g>')
    p.append(f'<rect x="{PAD}" y="{art_top:.1f}" width="{ART_W:.0f}" height="2" fill="{CYAN}" opacity="0">'
             f'<animate attributeName="y" from="{art_top:.1f}" to="{art_top+ART_H:.1f}" begin="{art_start:.2f}s" dur="1.5s" fill="freeze" calcMode="linear"/>'
             f'<set attributeName="opacity" to="0.5" begin="{art_start:.2f}s"/>'
             f'<set attributeName="opacity" to="0" begin="{art_start+1.5:.2f}s"/></rect>')

sl_y = art_top + ART_H + PAD * 0.3
sy = sl_y + 17
p.append(f'<line x1="0" y1="{sl_y:.1f}" x2="{CANVAS_W:.0f}" y2="{sl_y:.1f}" stroke="{FRAME}"/>')
p.append(f'<text x="{PAD}" y="{sy:.1f}" fill="{MUTED}" font-size="12">vihaan@github:~$ whoami <tspan fill="{INK}">Vihaan Kola</tspan></text>')

p.append("</svg>")
open(OUT, "w").write("".join(p))
print(f"wrote {OUT}; {COLS}x{ROWS}; canvas {CANVAS_W:.0f}x{CANVAS_H:.0f}")
