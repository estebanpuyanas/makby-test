"""
This is a tool to visualize raw polygon outlines in matplotlib.pyplot
subplots. While not used in official solutions, it can be helpful for 
debugging and understanding the result of polygon operations.
"""
import matplotlib.pyplot as plt
import numpy as np

def visualize_polygons(polygons_dict: dict, title: str = "Exercise 1 polygon visualization") -> None:
  """Render raw polygon outlines in a grid of matplotlib subplots.

  Creates one subplot per entry in ``polygons_dict``, drawing each polygon
  as a closed, lightly filled line. Useful for debugging polygon operations
  before applying fill patterns.

  Args:
      polygons_dict: Dictionary whose keys are display names and whose values
          are either a single polygon (list of (x, y) vertices) or a list of
          such polygons to overlay in the same subplot.
      title: Overall figure title displayed above all subplots. Defaults to
          ``"Exercise 1 polygon visualization"``.
  """
  num_plots = len(polygons_dict)
  fig, axes = plt.subplots(1, num_plots, figsize=(5 * num_plots, 5))
  
  if num_plots == 1:
    axes = [axes]

  for idx, (name, polygons) in enumerate(polygons_dict.items()):
    ax = axes[idx]

    # Handle single polygon vs. list of polygons. 
    if polygons and not isinstance(polygons[0], (list, tuple)):
      polygons = [polygons]

    # Plot each polygon.
    for polygon in polygons:
      if polygon:
        poly_array = np.array(polygon + [polygon[0]])
        ax.plot(poly_array[:, 0], poly_array[:, 1], 'o-', linewidth=2)
        ax.fill(poly_array[:, 0], poly_array[:, 1], alpha=0.3)
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title(name)

  plt.suptitle(title)
  plt.show()