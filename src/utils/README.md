# Utils Folder

The `utils/` folder in this repository contains several python files with utilities that are either:

- Code that gets re-used multiple times across the codebase.
- Boiler plate code, such as any setup required as part of ClipperLib.

Below is a more detaile breakdown of each utility file and the purpose it serves.

## [`clipper_helpers.py`](/src/utils/clipper_helpers.py):

- Defines a clipper scaling factor and the pyclipper object to plot shapes.

- the scaler is useful since both PyClipper and ClipperLib use [integers instead of floats](https://www.angusj.com/delphi/clipper/documentation/Docs/Overview/FAQ.htm) to perform operations. Therefore, when operating with decimals, we can scale the numbers up, operate, and then scale down before returning the final result.

- Some of these functions were taken from a [pracitce repository I worked on](https://github.com/estebanpuyanas/makby-practice) leading up to the release of the assessment.

- The isintance function is a utility to handle single polygons and lists of polygons in a consistent way. If the passed in input is a single polygon (i.e. a list of points) it is wrapped in an additional list to turn it into a list of polygons.

## [`gcode_exporter.py`](/src/utils/gcode_exporter.py):

- Defines header and footer functions which are fed into the top/bottom of a gcode file respectively. It then turns a list of PyClipper paths into G-Code moves. Assumes milimeters for units.

**Note: This file was entirely reproduced with AI, while [the root README](/README.md) outlines sources that were used to understanding the general syntax of G-Code, the following prompt was used to generate the file: "Generate a file that given a list of (x,y) points from PyClipper polygons will convert into G-Code moves that can be used by a CNC machine. Then have a function that will save the file to the directory where exercise 1 is solved. Explain the decisions you make in designing this functionality so I can understand and write proper documentation"**

## [`mappings.py`](/src/utils/mappings.py):

- Defines several boilerplate functions to transform coordinate mappings for exercise 2.

## [`patterns.py`](/src/utils/mappings.py):

- Defines functions for generating patterns used throughout exercises 1 and 2. For example, there is a utility to rotato polygon points about an origin and then perform that operation through a list of paths.

- Similarly, the `compute_bounding_box` function, as the name suggests, allows for easier computation of the polygon's bounding box, making it simpler to clip the specified pattern against the polygon.

- Some of the functions for pattern generation were also taken from the afformentioned [practice repository](https://github.com/estebanpuyanas/makby-practice).

## [`shapes.py`](/src/utils.shapes.py):

- Simple declaration of shapes used in [exercise 1](/src/exercise1/solution.py)
