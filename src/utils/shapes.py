



def create_rectangle(x1: int, x2: int, y1: int, y2: int) -> list:

  """
  According to the clipper docs:
  Simple polygons are formed by single closed paths that don't intersect. Paths themselves are closed when their ends join 
  with an implicit line segment between the first and last vertices. Closed path segments can be thought of as edges.
  """

  return [(x1, y1), 
          (x2, y1), 
          (x2, y2), 
          (x1, y2)]

"""
This function will create a 90 degree triangle
"""
def create_right_triangle(x1: int, x2: int, y1: int) -> list:
    return [
        (x1, y1),
        (x2, y1),
        (x1, x2),
    ]

def create_equilateral_triangle(x1: int, x2: int, y1: int) -> list:

  side_length = x2 - x1
  triangle_height = side_length * ((np.sqrt(3)) / 2)
  mid_point_x = (x1 + x2) / 2

  return [
    (x1, y1),
    (x2, y1), 
    (mid_point_x, y1 + triangle_height)
  ]

def create_circle(radius: int, num_vertices: int) -> list:
  """
  To create a circle, we can use the parametric equations of a circle:
  x = r * cos(theta)
  y = r * sin(theta)

  where r is the radius and theta is the angle that ranges from 0 to 2*pi.

  We can generate num_vertices points around the circle by varying theta from 0 to 2*pi in equal increments.
  """
  vertices = []
  for i in range(num_vertices):
    theta = (2 * np.pi / num_vertices) * i
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    vertices.append((x, y))
  
  return vertices