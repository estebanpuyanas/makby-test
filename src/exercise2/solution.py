# ── Step 0: Imports  ───────────────────────────────────────────────
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np

from utils.patterns import (
  generate_linear_hatch_pattern,
)

from utils.mappings import (
  map_paths_to_ring, 
  ring_corner_coordinates,
  map_paths_to_cylinder,
  cylinder_corner_coordinates,
)
# ── Step 1: Define parameters  ───────────────────────────────────────────────
TEMPLATE_WIDTH = 60.0
TEMPLATE_HEIGHT = 20.0
RADIUS = TEMPLATE_WIDTH / (2 * np.pi)
RING_INNER_RADIUS = 10.0
HATCH_SPACING = 0.5

TEMPLATE_RECTANGLE = [[0,0], 
                      [TEMPLATE_WIDTH, 0], 
                      [TEMPLATE_WIDTH, TEMPLATE_HEIGHT], 
                      [0, TEMPLATE_HEIGHT]]

# ── Step 2: Generate patterns on flat template ───────────────────────────────────────────────
flat_hatch_pattnern = generate_linear_hatch_pattern(TEMPLATE_RECTANGLE, HATCH_SPACING, angle_degrees=0)

# ── Step 3a: Map the pattern to a 2D ring  ───────────────────────────────────────────────
ring_hatch_pattern = map_paths_to_ring(flat_hatch_pattnern, TEMPLATE_WIDTH, RING_INNER_RADIUS)
ring_corners = ring_corner_coordinates(TEMPLATE_WIDTH, TEMPLATE_HEIGHT, RING_INNER_RADIUS)

# ── Step 3b: Map the pattern to the 3D cylinder  ───────────────────────────────────────────────
cylinder_hatch_pattern = map_paths_to_cylinder(flat_hatch_pattnern, RADIUS)
cylinder_corners = cylinder_corner_coordinates(TEMPLATE_WIDTH, TEMPLATE_HEIGHT, RADIUS)

# ── Step 4: Visualize  ───────────────────────────────────────────────
fig = plt.figure(figsize=(18, 6))
fig.suptitle("Exercise 2 — Spatial Mappings of a Rectilinear Pattern",
             fontsize=14, fontweight="bold")

# ── 4a: Flat template (reference) ────────────────────────────────────────────
ax0 = fig.add_subplot(1, 3, 1)

for path in flat_hatch_pattnern:
    if len(path) < 2:
        continue
    xs, ys = zip(*path)
    ax0.plot(xs, ys, color="steelblue", linewidth=0.7)

rect_arr = np.array(TEMPLATE_RECTANGLE + [TEMPLATE_RECTANGLE[0]])
ax0.plot(rect_arr[:, 0], rect_arr[:, 1], "k-", linewidth=2, label="Template boundary")

# Corner labels
for name, (cx, cy) in [("BL", (0,0)), ("BR", (TEMPLATE_WIDTH,0)), ("TR", (TEMPLATE_WIDTH,TEMPLATE_HEIGHT)), ("TL", (0,TEMPLATE_HEIGHT))]:
    ax0.annotate(name, (cx, cy), textcoords="offset points",
                 xytext=(5, 5), fontsize=8, color="darkred")

ax0.set_aspect("equal")
ax0.set_title("Flat Template\n(rectilinear pattern)")
ax0.set_xlabel("x (mm)")
ax0.set_ylabel("y (mm)")
ax0.set_xticks(np.arange(0, TEMPLATE_WIDTH + 1, 10))
ax0.set_yticks(np.arange(0, TEMPLATE_HEIGHT + 1, 5))
ax0.set_xticks(np.arange(0, TEMPLATE_WIDTH + 1, 2), minor=True)
ax0.set_yticks(np.arange(0, TEMPLATE_HEIGHT + 1, 1), minor=True)
ax0.grid(which="major", color="gray",      linewidth=0.7, alpha=0.5)
ax0.grid(which="minor", color="lightgray", linewidth=0.3, alpha=0.4)
ax0.legend(fontsize=8)

# ── 4b: Part A — 2D ring ─────────────────────────────────────────────────────
ax1 = fig.add_subplot(1, 3, 2)

for path in ring_hatch_pattern:
    if len(path) < 2:
        continue
    xs, ys = zip(*path)
    ax1.plot(xs, ys, color="darkorange", linewidth=0.7)

# Draw inner and outer boundary circles
theta_range = np.linspace(0, 2 * np.pi, 500)
for r, style, lbl in [(RING_INNER_RADIUS, "k--", "inner boundary"),
                       (RING_INNER_RADIUS + TEMPLATE_HEIGHT, "k-",  "outer boundary")]:
    ax1.plot(r * np.cos(theta_range), r * np.sin(theta_range),
             style, linewidth=1.5, label=lbl)

# Mapped corner markers
for name, (xp, yp) in ring_corners.items():
    ax1.plot(xp, yp, "ro", markersize=5)
    ax1.annotate(name.split(" ")[0], (xp, yp),
                 textcoords="offset points", xytext=(4, 4), fontsize=7, color="darkred")

ax1.set_aspect("equal")
ax1.set_title(f"Part A — 2D Ring Mapping\n(r_inner={RING_INNER_RADIUS}, r_outer={RING_INNER_RADIUS+TEMPLATE_HEIGHT})")
ax1.set_xlabel("x' (mm)")
ax1.set_ylabel("y' (mm)")
ax1.grid(which="major", color="gray",      linewidth=0.7, alpha=0.5)
ax1.grid(which="minor", color="lightgray", linewidth=0.3, alpha=0.4)
ax1.legend(fontsize=8)

# ── 4c: Part B — 3D cylinder ─────────────────────────────────────────────────
ax2 = fig.add_subplot(1, 3, 3, projection="3d")

for path in cylinder_hatch_pattern:
    if len(path) < 2:
        continue
    xs, ys, zs = zip(*path)
    ax2.plot(xs, ys, zs, color="green", linewidth=0.7)

# Draw cylinder wireframe surface for reference
u = np.linspace(0, 2 * np.pi, 60)
z_cyl = np.linspace(0, TEMPLATE_HEIGHT, 10)
U, Z = np.meshgrid(u, z_cyl)
ax2.plot_surface(RADIUS * np.cos(U), RADIUS * np.sin(U), Z,
                 alpha=0.08, color="gray", linewidth=0)

# Cylinder top and bottom circles
for z_val in [0, TEMPLATE_HEIGHT]:
    ax2.plot(RADIUS * np.cos(u), RADIUS * np.sin(u),
             np.full_like(u, z_val), "k--", linewidth=1.0, alpha=0.6)

# Mapped corner markers
for name, (xp, yp, zp) in cylinder_corners.items():
    ax2.scatter(xp, yp, zp, color="red", s=30, zorder=5)
    ax2.text(xp, yp, zp + 0.5, name.split(" ")[0], fontsize=7, color="darkred")

ax2.set_title(f"Part B — 3D Cylinder Mapping\n(R={RADIUS:.2f} mm, W=2πR ✓)")
ax2.set_xlabel("x' (mm)")
ax2.set_ylabel("y' (mm)")
ax2.set_zlabel("z' (mm)")

plt.tight_layout()
plt.show()