import pyclipper
from utils.clipper_helpers import (
   pc, 
   _ensure_paths,
   _scale_from_clipper,
   _scale_to_clipper,
   _run,
)

def compute_polygon_intersection(poly1: list, poly2: list) -> list:
  pc.Clear()
  paths1 = _scale_to_clipper(_ensure_paths(poly1))
  paths2 = _scale_to_clipper(_ensure_paths(poly2))
  pc.AddPaths(paths1, pyclipper.PT_SUBJECT, True)
  pc.AddPaths(paths2, pyclipper.PT_CLIP, True)
  solution = pc.Execute(pyclipper.CT_INTERSECTION)
  return _scale_from_clipper(solution)

def compute_polygon_difference(poly1: list, poly2: list) -> list:
    pc.Clear()
    paths1 = _scale_to_clipper(_ensure_paths(poly1))
    paths2 = _scale_to_clipper(_ensure_paths(poly2))
    pc.AddPaths(paths1, pyclipper.PT_SUBJECT, True)
    pc.AddPaths(paths2, pyclipper.PT_CLIP, True)
    solution = pc.Execute(pyclipper.CT_DIFFERENCE, True)
    return _scale_from_clipper(solution)

def compute_polygon_union(poly1_subject: list, poly2_clipper: list) -> list:
  pc.Clear()
  paths1 = _scale_to_clipper(_ensure_paths(poly1_subject))
  paths2 = _scale_to_clipper(_ensure_paths(poly2_clipper))
  pc.AddPaths(paths1, pyclipper.PT_SUBJECT, True)
  pc.AddPaths(paths2, pyclipper.PT_SUBJECT, True)
  solution = pc.Execute(pyclipper.CT_UNION, True)
  return _scale_from_clipper(solution)

def compute_multi_poly_ops(start_poly: list, ops: list) -> list:
  result = start_poly

  for op, poly in ops:
    result = op(result, poly)

  return result

"""Clip open polylines (hatch lines) against a closed polygon."""
def clip_open_paths(open_paths: list, clip_poly: list) -> list:
    return _run(open_paths, _ensure_paths(clip_poly), pyclipper.CT_INTERSECTION, subject_closed=False)