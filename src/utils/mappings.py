import math

# ──── Functions to map between rectangle and ring coordinates (problem 2.a) ─────────────────────────────
def map_point_to_ring(x: float, y: float, w: float, r_inner: float) -> tuple:
  """Map a single flat-template point to its 2D position on a ring.

  The x-axis of the template wraps around the ring circumference (one full
  revolution = w), while the y-axis becomes the radial distance from the
  inner radius.

  Args:
      x: Horizontal position on the flat template in mm.
      y: Vertical position on the flat template in mm.
      w: Total width of the flat template in mm, corresponding to one full
          revolution (2π) of the ring.
      r_inner: Inner radius of the ring in mm.

  Returns:
      A tuple (x', y') of Cartesian coordinates on the ring plane in mm.
  """

  theta = (x/w) * 2 * math.pi
  r = r_inner + y
  return (r * math.cos(theta), r * math.sin(theta))

def map_path_to_ring(path: list, w: float, r_inner: float) -> list:
  """Map a polyline from flat-template coordinates to ring coordinates.

  Applies ``map_point_to_ring`` to every point in the polyline.

  Args:
      path: A polyline as a list of (x, y) tuples in flat-template coordinates.
      w: Total width of the flat template in mm.
      r_inner: Inner radius of the ring in mm.

  Returns:
      A list of (x', y') tuples representing the polyline on the ring.
  """

  return [map_point_to_ring(x,y,w,r_inner) for x,y in path]

def map_paths_to_ring(paths: list, w: float, r_inner: float) -> list:
  """Map a collection of polylines from flat-template coordinates to ring coordinates.

  Args:
      paths: A list of polylines in flat-template coordinates.
      w: Total width of the flat template in mm.
      r_inner: Inner radius of the ring in mm.

  Returns:
      A list of polylines mapped onto the ring.
  """
  return [map_path_to_ring(path, w, r_inner) for path in paths]

def ring_corner_coordinates(w: float, h: float, r_inner: float) -> dict:
  """Return the ring-mapped coordinates of the four rectangle corners.

  Args:
      w: Width of the flat template in mm (BL→BR or TL→TR distance).
      h: Height of the flat template in mm (BL→TL or BR→TR distance).
      r_inner: Inner radius of the ring in mm.

  Returns:
      A dictionary mapping each corner name to its (x', y') position on
      the ring. Keys: ``"Bottom left (0,0)"``, ``"Bottom right (w, 0)"``,
      ``"Top right (w,h)"``, ``"Top left (0,h)"``.
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
  """Map a single flat-template point to its position on a 3D cylinder surface.

  The x-axis of the template wraps around the cylinder circumference
  (θ = x / r), while the y-axis becomes the height along z.

  Args:
      x: Horizontal position on the flat template in mm.
      y: Vertical position on the flat template in mm, mapped to the z-axis.
      r: Radius of the cylinder in mm.

  Returns:
      A tuple (x', y', z') of Cartesian coordinates on the cylinder surface
      in mm.
  """
  theta = (x / r)
  return (r * math.cos(theta), r * math.sin(theta), y)

def map_path_to_cylinder(path: list, r: float) -> list:
  """Map a polyline from flat-template coordinates to cylinder surface coordinates.

  Applies ``map_point_to_cylinder`` to every point in the polyline.

  Args:
      path: A polyline as a list of (x, y) tuples in flat-template coordinates.
      r: Radius of the cylinder in mm.

  Returns:
      A list of (x', y', z') tuples representing the polyline on the
      cylinder surface.
  """
  return [map_point_to_cylinder(x,y,r) for x,y in path]

def map_paths_to_cylinder(paths: list, r: float) -> list:
  """Map a collection of polylines from flat-template coordinates to cylinder surface coordinates.

  Args:
      paths: A list of polylines in flat-template coordinates.
      r: Radius of the cylinder in mm.

  Returns:
      A list of polylines mapped onto the cylinder surface, each point
      expressed as an (x', y', z') tuple.
  """
  return [map_path_to_cylinder(path, r) for path in paths]

def cylinder_corner_coordinates(w: float, h: float, r: float) -> dict:
  """Return the cylinder-mapped coordinates of the four rectangle corners.

  When ``w == 2 * π * r``, the left and right edges of the template wrap
  exactly once around the cylinder, landing at the same angular position.

  Args:
      w: Width of the flat template in mm.
      h: Height of the flat template in mm, mapped to the cylinder height.
      r: Radius of the cylinder in mm.

  Returns:
      A dictionary mapping each corner name to its (x', y', z') position on
      the cylinder surface. Keys: ``"Bottom left (0,0)"``,
      ``"Bottom right (w, 0)"``, ``"Top right (w,h)"``, ``"Top left (0,h)"``.
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
