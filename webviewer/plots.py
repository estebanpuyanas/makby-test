"""
Generates matplotlib figures for each exercise and returns PNG bytes.
Uses the Agg (non-interactive) backend so it works inside Flask.
"""
import io, os, sys

# Make sure src/ is importable
SRC = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, SRC)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


# ── Exercise 1 ────────────────────────────────────────────────────────────────

def gen_ex1_plot() -> bytes:
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

    # Venn regions
    R1_R2   = compute_polygon_intersection(RECT1, RECT2)
    R1_T    = compute_polygon_intersection(RECT1, TRIANGLE)
    R2_T    = compute_polygon_intersection(RECT2, TRIANGLE)
    R1_R2_T = compute_multi_poly_ops(RECT1, [
                  (compute_polygon_intersection, RECT2),
                  (compute_polygon_intersection, TRIANGLE),
              ])
    R1_only   = compute_multi_poly_ops(RECT1,    [(compute_polygon_difference, RECT2),    (compute_polygon_difference, TRIANGLE)])
    R2_only   = compute_multi_poly_ops(RECT2,    [(compute_polygon_difference, RECT1),    (compute_polygon_difference, TRIANGLE)])
    T_only    = compute_multi_poly_ops(TRIANGLE, [(compute_polygon_difference, RECT1),    (compute_polygon_difference, RECT2)])
    R1R2_only = compute_polygon_difference(R1_R2, TRIANGLE)
    R1T_only  = compute_polygon_difference(R1_T,  RECT2)

    SPACING  = 0.4
    HEX_SIZE = 0.4

    regions = {
        "Rect1 only — 0° rectilinear":        generate_linear_hatch_pattern(R1_only,   SPACING, 0),
        "Rect2 only — honeycomb":              generate_honeycomb_pattern(R2_only,      HEX_SIZE),
        "Triangle only — spiral":              generate_spiral_pattern(T_only,          b=SPACING / (2 * 3.14159)),
        "R1∩R2 — 90° rectilinear":            generate_linear_hatch_pattern(R1R2_only, SPACING, 90),
        "R1∩Triangle — 120° rectilinear":     generate_linear_hatch_pattern(R1T_only,  SPACING, 120),
        "R2∩Triangle — no fill":              [],
        "R1∩R2∩Triangle — 45° rectilinear":  generate_linear_hatch_pattern(R1_R2_T,   SPACING, 45),
    }

    REGION_COLORS = {
        "Rect1 only — 0° rectilinear":        "steelblue",
        "Rect2 only — honeycomb":             "darkorange",
        "Triangle only — spiral":             "green",
        "R1∩R2 — 90° rectilinear":           "purple",
        "R1∩Triangle — 120° rectilinear":    "red",
        "R2∩Triangle — no fill":             None,
        "R1∩R2∩Triangle — 45° rectilinear":  "brown",
    }
    SHAPE_STYLES = {
        "Rect1":    {"color": "royalblue",  "linestyle": "-",  "linewidth": 2.0},
        "Rect2":    {"color": "tomato",     "linestyle": "--", "linewidth": 2.0},
        "Triangle": {"color": "goldenrod",  "linestyle": ":",  "linewidth": 2.5},
    }

    fig, ax = plt.subplots(figsize=(14, 9))

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
                    label=label if first else None)
            first = False

    for name, poly in {"Rect1": RECT1, "Rect2": RECT2, "Triangle": TRIANGLE}.items():
        arr = np.array(poly + [poly[0]])
        style = SHAPE_STYLES[name]
        ax.plot(arr[:, 0], arr[:, 1],
                color=style["color"], linestyle=style["linestyle"],
                linewidth=style["linewidth"], label=f"[shape] {name}")

    ax.set_aspect("equal")
    ax.set_xlim(-5, 65)
    ax.set_ylim(-15, 45)
    ax.set_xticks(np.arange(-5, 66, 5))
    ax.set_yticks(np.arange(-15, 46, 5))
    ax.set_xticks(np.arange(-5, 66, 1), minor=True)
    ax.set_yticks(np.arange(-15, 46, 1), minor=True)
    ax.grid(which="major", color="gray",      linewidth=0.8, alpha=0.5)
    ax.grid(which="minor", color="lightgray", linewidth=0.3, alpha=0.4)
    ax.tick_params(axis="both", which="major", labelsize=8)
    ax.set_title("Exercise 1 — Pattern Regions", fontsize=14, fontweight="bold")
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.legend(loc="upper right", fontsize=8, ncol=2, framealpha=0.9,
              title="Regions & Shapes", title_fontsize=9)
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0)
    return buf.read()


# ── Exercise 2 ────────────────────────────────────────────────────────────────

def gen_ex2_plot() -> bytes:
    from utils.patterns import generate_linear_hatch_pattern
    from utils.mappings import (
        map_paths_to_ring,
        ring_corner_coordinates,
        map_paths_to_cylinder,
        cylinder_corner_coordinates,
    )

    TEMPLATE_WIDTH  = 60.0
    TEMPLATE_HEIGHT = 20.0
    RADIUS          = TEMPLATE_WIDTH / (2 * np.pi)
    RING_INNER_RADIUS = 10.0
    HATCH_SPACING   = 0.5

    TEMPLATE_RECTANGLE = [[0, 0], [TEMPLATE_WIDTH, 0],
                           [TEMPLATE_WIDTH, TEMPLATE_HEIGHT], [0, TEMPLATE_HEIGHT]]

    flat_hatch = generate_linear_hatch_pattern(TEMPLATE_RECTANGLE, HATCH_SPACING, angle_degrees=0)
    ring_hatch  = map_paths_to_ring(flat_hatch, TEMPLATE_WIDTH, RING_INNER_RADIUS)
    ring_corners = ring_corner_coordinates(TEMPLATE_WIDTH, TEMPLATE_HEIGHT, RING_INNER_RADIUS)
    cyl_hatch   = map_paths_to_cylinder(flat_hatch, RADIUS)
    cyl_corners = cylinder_corner_coordinates(TEMPLATE_WIDTH, TEMPLATE_HEIGHT, RADIUS)

    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    fig = plt.figure(figsize=(18, 6))
    fig.suptitle("Exercise 2 — Spatial Mappings of a Rectilinear Pattern",
                 fontsize=14, fontweight="bold")

    # 4a Flat template
    ax0 = fig.add_subplot(1, 3, 1)
    for path in flat_hatch:
        if len(path) < 2:
            continue
        xs, ys = zip(*path)
        ax0.plot(xs, ys, color="steelblue", linewidth=0.7)
    rect_arr = np.array(TEMPLATE_RECTANGLE + [TEMPLATE_RECTANGLE[0]])
    ax0.plot(rect_arr[:, 0], rect_arr[:, 1], "k-", linewidth=2, label="Template boundary")
    for name, (cx, cy) in [("BL",(0,0)),("BR",(TEMPLATE_WIDTH,0)),
                             ("TR",(TEMPLATE_WIDTH,TEMPLATE_HEIGHT)),("TL",(0,TEMPLATE_HEIGHT))]:
        ax0.annotate(name, (cx, cy), textcoords="offset points",
                     xytext=(5, 5), fontsize=8, color="darkred")
    ax0.set_aspect("equal")
    ax0.set_title("Flat Template\n(rectilinear pattern)")
    ax0.set_xlabel("x (mm)"); ax0.set_ylabel("y (mm)")
    ax0.set_xticks(np.arange(0, TEMPLATE_WIDTH  + 1, 10))
    ax0.set_yticks(np.arange(0, TEMPLATE_HEIGHT + 1,  5))
    ax0.set_xticks(np.arange(0, TEMPLATE_WIDTH  + 1,  2), minor=True)
    ax0.set_yticks(np.arange(0, TEMPLATE_HEIGHT + 1,  1), minor=True)
    ax0.grid(which="major", color="gray",      linewidth=0.7, alpha=0.5)
    ax0.grid(which="minor", color="lightgray", linewidth=0.3, alpha=0.4)
    ax0.legend(fontsize=8)

    # 4b 2D ring
    ax1 = fig.add_subplot(1, 3, 2)
    for path in ring_hatch:
        if len(path) < 2:
            continue
        xs, ys = zip(*path)
        ax1.plot(xs, ys, color="darkorange", linewidth=0.7)
    theta_range = np.linspace(0, 2 * np.pi, 500)
    for r, style, lbl in [(RING_INNER_RADIUS, "k--", "inner boundary"),
                           (RING_INNER_RADIUS + TEMPLATE_HEIGHT, "k-", "outer boundary")]:
        ax1.plot(r * np.cos(theta_range), r * np.sin(theta_range),
                 style, linewidth=1.5, label=lbl)
    for name, (xp, yp) in ring_corners.items():
        ax1.plot(xp, yp, "ro", markersize=5)
        ax1.annotate(name.split(" ")[0], (xp, yp),
                     textcoords="offset points", xytext=(4, 4), fontsize=7, color="darkred")
    ax1.set_aspect("equal")
    ax1.set_title(f"Part A — 2D Ring Mapping\n(r_inner={RING_INNER_RADIUS}, r_outer={RING_INNER_RADIUS+TEMPLATE_HEIGHT})")
    ax1.set_xlabel("x' (mm)"); ax1.set_ylabel("y' (mm)")
    ax1.grid(which="major", color="gray",      linewidth=0.7, alpha=0.5)
    ax1.grid(which="minor", color="lightgray", linewidth=0.3, alpha=0.4)
    ax1.legend(fontsize=8)

    # 4c 3D cylinder
    ax2 = fig.add_subplot(1, 3, 3, projection="3d")
    for path in cyl_hatch:
        if len(path) < 2:
            continue
        xs, ys, zs = zip(*path)
        ax2.plot(xs, ys, zs, color="green", linewidth=0.7)
    u = np.linspace(0, 2 * np.pi, 60)
    z_cyl = np.linspace(0, TEMPLATE_HEIGHT, 10)
    U, Z = np.meshgrid(u, z_cyl)
    ax2.plot_surface(RADIUS * np.cos(U), RADIUS * np.sin(U), Z,
                     alpha=0.08, color="gray", linewidth=0)
    for z_val in [0, TEMPLATE_HEIGHT]:
        ax2.plot(RADIUS * np.cos(u), RADIUS * np.sin(u),
                 np.full_like(u, z_val), "k--", linewidth=1.0, alpha=0.6)
    for name, (xp, yp, zp) in cyl_corners.items():
        ax2.scatter(xp, yp, zp, color="red", s=30, zorder=5)
        ax2.text(xp, yp, zp + 0.5, name.split(" ")[0], fontsize=7, color="darkred")
    ax2.set_title(f"Part B — 3D Cylinder Mapping\n(R={RADIUS:.2f} mm, W=2πR ✓)")
    ax2.set_xlabel("x' (mm)"); ax2.set_ylabel("y' (mm)"); ax2.set_zlabel("z' (mm)")

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=110)
    plt.close(fig)
    buf.seek(0)
    return buf.read()
