import math
import numpy as np 

# ──── Functions to map between rectangle and ring coordinates (problem 2.a) ─────────────────────────────
def map_point_to_ring(x: float, y: float, w: float, r_inner: float) -> tuple:
  """
  Map a single (x,y) coordinate point into (x', y') coordinates on the ring:
  """

  theta = (x/w) * 2 * math.pi
  r = r_inner + y
  return (r * math.cos(theta), r * math.sin(theta))

def map_path_to_ring(path: list, w: float, r_inner: float) -> list:
  """
  Maps a polyline, defined by a list of (x,y) coordinate points onto the ring.
  """

  return [map_point_to_ring(x,y,w,r_inner) for x,y in path]

def map_paths_to_ring(paths: list, w: float, r_inner: float) -> list:
  return [map_path_to_ring(path, w, r_inner) for path in paths]

def ring_corner_coordinates(w: float, h: float, r_inner: float) -> dict:
  """
  Returns the mapped (x', y') coordinates of the four rectangle corners.
  Corners:
  BL [Bottom left] -> (0,0)
  BR [Bottom right] -> (w,0)
  TR [Top right] -> (w,h)
  TL [Top left] -> (0,h)
  """

  rectangle_corners = {
    "Bottom left (0,0)": (0,0),
    "Bottom right (w, 0)": (w,0),
    "Top right (w,h)": (w,h),
    "Top left (0,h)": (0,h)
  }

  return {
    name: map_point_to_ring(x,y,w,r_inner)
    for name, (x,y) in rectangle_corners.items()
  }

# ──── Functions for cylindrical mapping (problem 2.b) ─────────────────────────────
def map_point_to_cylinder(x: float, y: float, r: float) -> tuple:
  """
  Map a point (x,y) in the rectangle to a point (x',y',z') in the cylinder.
  """
  theta = (x / r)
  return (r * math.cos(theta), r * math.sin(theta), y)

def map_path_to_cylinder(path: list, r: float) -> list:
  return [map_point_to_cylinder(x,y,r) for x,y in path]

def map_paths_to_cylinder(paths: list, r: float) -> list:
  return [map_path_to_cylinder(path, r) for path in paths]

def cylinder_corner_coordinates(w: float, h: float, r: float) -> list:
  """
  Returns the mapped (x',y',z') coordinates of the four rectangle corners.
  when w = 2 * pi * r, the bottom/top right corners land exactly on the angle of the bottom/top right corners, respectively. 
  """

  corners = {
    "Bottom left (0,0)": (0,0),
    "Bottom right (w, 0)": (w,0),
    "Top right (w,h)": (w,h),
    "Top left (0,h)": (0,h)
  }

  return {
    name: map_point_to_cylinder(x,y,r)
    for name, (x,y) in corners.items()
  }
