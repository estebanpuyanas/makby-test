import pyclipper

from utils.clipper_helpers import (
   pc, 
   _ensure_paths,
   _scale_from_clipper,
   _scale_to_clipper,
   _run,
)

def compute_polygon_intersection(poly1: list, poly2: list) -> list:
  """Compute the geometric intersection of two polygons.

  Returns the region that is covered by both input polygons.

  Args:
      poly1: First polygon as a list of [x, y] vertices, or a list of
          such polygons.
      poly2: Second polygon as a list of [x, y] vertices, or a list of
          such polygons.

  Returns:
      A list of polygons representing the intersection region. Returns an
      empty list if the polygons do not overlap.
  """
  pc.Clear()
  paths1 = _scale_to_clipper(_ensure_paths(poly1))
  paths2 = _scale_to_clipper(_ensure_paths(poly2))
  pc.AddPaths(paths1, pyclipper.PT_SUBJECT, True)
  pc.AddPaths(paths2, pyclipper.PT_CLIP, True)
  solution = pc.Execute(pyclipper.CT_INTERSECTION)
  return _scale_from_clipper(solution)

def compute_polygon_difference(poly1: list, poly2: list) -> list:
    """Compute the geometric difference of two polygons (poly1 minus poly2).

    Returns the region covered by ``poly1`` that is not covered by ``poly2``.

    Args:
        poly1: Subject polygon as a list of [x, y] vertices, or a list of
            such polygons.
        poly2: Clip polygon as a list of [x, y] vertices, or a list of
            such polygons. This region is subtracted from ``poly1``.

    Returns:
        A list of polygons representing the remaining region. Returns an
        empty list if ``poly1`` is entirely covered by ``poly2``.
    """
    pc.Clear()
    paths1 = _scale_to_clipper(_ensure_paths(poly1))
    paths2 = _scale_to_clipper(_ensure_paths(poly2))
    pc.AddPaths(paths1, pyclipper.PT_SUBJECT, True)
    pc.AddPaths(paths2, pyclipper.PT_CLIP, True)
    solution = pc.Execute(pyclipper.CT_DIFFERENCE, True)
    return _scale_from_clipper(solution)

def compute_polygon_union(poly1_subject: list, poly2_clipper: list) -> list:
  """Compute the geometric union of two polygons.

  Returns the region covered by either or both input polygons.

  Args:
      poly1_subject: First polygon as a list of [x, y] vertices, or a list
          of such polygons.
      poly2_clipper: Second polygon as a list of [x, y] vertices, or a list
          of such polygons.

  Returns:
      A list of polygons representing the merged region.
  """
  pc.Clear()
  paths1 = _scale_to_clipper(_ensure_paths(poly1_subject))
  paths2 = _scale_to_clipper(_ensure_paths(poly2_clipper))
  pc.AddPaths(paths1, pyclipper.PT_SUBJECT, True)
  pc.AddPaths(paths2, pyclipper.PT_SUBJECT, True)
  solution = pc.Execute(pyclipper.CT_UNION, True)
  return _scale_from_clipper(solution)

def compute_multi_poly_ops(start_poly: list, ops: list) -> list:
  """Apply a sequence of polygon operations to an initial polygon.

  Chains multiple pairwise polygon operations together, threading the result
  of each step as the first argument into the next.

  Args:
      start_poly: The initial polygon as a list of [x, y] vertices, or a
          list of such polygons.
      ops: An ordered list of ``(operation, polygon)`` tuples. Each
          ``operation`` is a callable that accepts two polygon arguments and
          returns a polygon (e.g. ``compute_polygon_intersection``), and
          ``polygon`` is the second operand for that step.

  Returns:
      The polygon resulting from applying all operations in sequence.
  """
  result = start_poly

  for op, poly in ops:
    result = op(result, poly)

  return result

def clip_open_paths(open_paths: list, clip_poly: list) -> list:
    """Clip open polylines (e.g. hatch lines) against a closed polygon.

    Retains only the segments of each polyline that lie inside the clip
    polygon, discarding everything outside.

    Args:
        open_paths: A list of polylines to clip, where each polyline is a
            list of (x, y) tuples.
        clip_poly: The closed clipping polygon as a list of [x, y] vertices,
            or a list of such polygons.

    Returns:
        A list of clipped open polylines in floating-point millimetre
        coordinates.
    """
    return _run(open_paths, _ensure_paths(clip_poly), pyclipper.CT_INTERSECTION, subject_closed=False)