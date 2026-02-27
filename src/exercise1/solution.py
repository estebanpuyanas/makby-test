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
R1R_2T = compute_multi_poly_ops(RECT1, [
            (compute_polygon_intersection, RECT2),
            (compute_polygon_intersection, TRIANGLE),
        ])

R1_only   = compute_multi_poly_ops(RECT1,    [(compute_polygon_difference, RECT2),    (compute_polygon_difference, TRIANGLE)])
R2_only   = compute_multi_poly_ops(RECT2,    [(compute_polygon_difference, RECT1),    (compute_polygon_difference, TRIANGLE)])
T_only    = compute_multi_poly_ops(TRIANGLE, [(compute_polygon_difference, RECT1),    (compute_polygon_difference, RECT2)])
R1R2_only = compute_polygon_difference(R1_R2, TRIANGLE)
R1T_only  = compute_polygon_difference(R1_T,  RECT2)
R2T_only  = compute_polygon_difference(R2_T,  RECT1)   # no fill

# ── Step 2: Assign patterns ──────────────────────────────────────────────────

SPACING  = 0.4
HEX_SIZE = 1.5

regions = {
    "Rect1 only — 0° rectilinear":       generate_linear_hatch_pattern(R1_only,   SPACING, 0),
    "Rect2 only — honeycomb":            generate_honeycomb_pattern(R2_only,      HEX_SIZE),
    "Triangle only — spiral":            generate_spiral_pattern(T_only,          b=SPACING / (2 * 3.14159)),
    "R1∩R2 — 90° rectilinear":          generate_linear_hatch_pattern(R1R2_only, SPACING, 90),
    "R1∩Triangle — 120° rectilinear":   generate_linear_hatch_pattern(R1T_only,  SPACING, 120),
    "R2∩Triangle — no fill":            [],
    "R1∩R2∩Triangle — 45° rectilinear": generate_linear_hatch_pattern(R1R_2T,     SPACING, 45),
}

# ── Step 3: Visualise ────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(12, 8))
COLORS = ["steelblue","darkorange","green","purple","red","gray","brown"]

for (label, paths), color in zip(regions.items(), COLORS):
    for path in paths:
        if len(path) < 2:
            continue
        xs, ys = zip(*path)
        ax.plot(xs, ys, color=color, linewidth=0.6)

for name, poly in {"Rect1": RECT1, "Rect2": RECT2, "Triangle": TRIANGLE}.items():
    arr = np.array(poly + [poly[0]])
    ax.plot(arr[:, 0], arr[:, 1], "k--", linewidth=1.5, label=name)

ax.set_aspect("equal")
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_title("Exercise 1 — Pattern Regions")
plt.tight_layout()
plt.show()

# ── Step 4: Export G-code ────────────────────────────────────────────────────
gcode = paths_to_gcode(list(regions.values()), labels=list(regions.keys()))
save_gcode(gcode, os.path.join(os.path.dirname(__file__), "exercise1.gcode"))






