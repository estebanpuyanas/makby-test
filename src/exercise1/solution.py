# ── Step 0: Imports  ───────────────────────────────────────────────
import os, sys 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import matplotlib
matplotlib.use("Tkagg")
import matplotlib.pyplot as plt
import numpy as np

from utils.shapes import RECT1, RECT2, TRIANGLE

from utils.polygon_operations import (
  compute_polygon_intersection,
  compute_polygon_difference,
  compute_multi_poly_ops,
)

from utils.patterns import (
  generate_linear_hatch_pattern, 
  generate_spiral_pattern,
  generate_honeycomb_pattern, 
)

from utils.gcode_exporter import (
  paths_to_gcode,
  save_gcode,
)

# ── Step 1: Carve Venn regions ───────────────────────────────────────────────

R1_R2  = compute_polygon_intersection(RECT1, RECT2)
R1_T   = compute_polygon_intersection(RECT1, TRIANGLE)
R2_T   = compute_polygon_intersection(RECT2, TRIANGLE)
R1_R2_T = compute_multi_poly_ops(RECT1, [
            (compute_polygon_intersection, RECT2),
            (compute_polygon_intersection, TRIANGLE),
        ])

R1_only   = compute_multi_poly_ops(RECT1,    [(compute_polygon_difference, RECT2),    (compute_polygon_difference, TRIANGLE)])
R2_only   = compute_multi_poly_ops(RECT2,    [(compute_polygon_difference, RECT1),    (compute_polygon_difference, TRIANGLE)])
T_only    = compute_multi_poly_ops(TRIANGLE, [(compute_polygon_difference, RECT1),    (compute_polygon_difference, RECT2)])
R1R2_only = compute_polygon_difference(R1_R2, TRIANGLE)
R1T_only  = compute_polygon_difference(R1_T,  RECT2)
R2T_only  = compute_polygon_difference(R2_T,  RECT1) # no fill

# ── Step 2: Assign patterns ──────────────────────────────────────────────────

SPACING  = 0.4
HEX_SIZE = 0.4

regions = {
    "Rect1 only — 0° rectilinear":       generate_linear_hatch_pattern(R1_only,   SPACING, 0),
    "Rect2 only — honeycomb":            generate_honeycomb_pattern(R2_only,      HEX_SIZE),
    "Triangle only — spiral":            generate_spiral_pattern(T_only,          b=SPACING / (2 * 3.14159)),
    "R1∩R2 — 90° rectilinear":          generate_linear_hatch_pattern(R1R2_only, SPACING, 90),
    "R1∩Triangle — 120° rectilinear":   generate_linear_hatch_pattern(R1T_only,  SPACING, 120),
    "R2∩Triangle — no fill":            [],
    "R1∩R2∩Triangle — 45° rectilinear": generate_linear_hatch_pattern(R1_R2_T,     SPACING, 45),
}

# ── Step 3: Visualise ────────────────────────────────────────────────────────

# Pattern colours (one per region)
REGION_COLORS = {
    "Rect1 only — 0° rectilinear":        "steelblue",
    "Rect2 only — honeycomb":             "darkorange",
    "Triangle only — spiral":             "green",
    "R1∩R2 — 90° rectilinear":           "purple",
    "R1∩Triangle — 120° rectilinear":    "red",
    "R2∩Triangle — no fill":             None,
    "R1∩R2∩Triangle — 45° rectilinear":  "brown",
}

# Shape outline styles — each shape gets its own colour + linestyle
SHAPE_STYLES = {
    "Rect1":    {"color": "royalblue",  "linestyle": "-",  "linewidth": 2.0},
    "Rect2":    {"color": "tomato",     "linestyle": "--", "linewidth": 2.0},
    "Triangle": {"color": "goldenrod",  "linestyle": ":",  "linewidth": 2.5},
}

fig, ax = plt.subplots(figsize=(14, 9))

# Draw fill patterns
for label, paths in regions.items():
    color = REGION_COLORS.get(label)
    if color is None or not paths:
        continue
    first = True
    for path in paths:
        if len(path) < 2:
            continue
        xs, ys = zip(*path)
        ax.plot(xs, ys, color=color, linewidth=0.6,
                label=label if first else None)   # one legend entry per region
        first = False

# Draw shape outlines
for name, poly in {"Rect1": RECT1, "Rect2": RECT2, "Triangle": TRIANGLE}.items():
    arr = np.array(poly + [poly[0]])
    style = SHAPE_STYLES[name]
    ax.plot(arr[:, 0], arr[:, 1],
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=style["linewidth"],
            label=f"[shape] {name}")

# Grid — minor ticks every 1 unit, major every 5
ax.set_aspect("equal")
ax.set_xlim(-5, 65)
ax.set_ylim(-15, 45)

ax.set_xticks(np.arange(-5, 66, 5))          # major gridlines every 5
ax.set_yticks(np.arange(-15, 46, 5))
ax.set_xticks(np.arange(-5, 66, 1), minor=True)  # minor gridlines every 1
ax.set_yticks(np.arange(-15, 46, 1), minor=True)

ax.grid(which="major", color="gray",      linewidth=0.8, alpha=0.5)
ax.grid(which="minor", color="lightgray", linewidth=0.3, alpha=0.4)

ax.tick_params(axis="both", which="major", labelsize=8)

ax.set_title("Exercise 1 — Pattern Regions", fontsize=14, fontweight="bold")
ax.set_xlabel("X (mm)")
ax.set_ylabel("Y (mm)")

# Legend — split into two columns so it's not too tall
ax.legend(
    loc="upper right",
    fontsize=8,
    ncol=2,
    framealpha=0.9,
    title="Regions & Shapes",
    title_fontsize=9,
)

plt.tight_layout()
plt.show()

# ── Step 4: Export G-code ────────────────────────────────────────────────────
gcode = paths_to_gcode(list(regions.values()), labels=list(regions.keys()))
save_gcode(gcode, os.path.join(os.path.dirname(__file__), "exercise1.gcode"))