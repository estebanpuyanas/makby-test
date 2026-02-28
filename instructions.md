# Exercise 1

We would like to print the following group of geometries combining different pattern types. The patterns
should be combined in single G-code file.

The description of the geometries is the following:

- "Rectangle 1":[[5, 12], [53, 12],[53, 24],[5, 24]]
- "Rectangle 2":[[16, 29],[40.213, -9],[54.483, -1],[29, 37]]
- "Triangle":[[8, 4],[43, 4],[27, 21]]

The pattern assigned to each part should be:

- Rectilinear pattern for rectangle 1 (0 -degree rotation)
- Honeycomb pattern for honeycomb for rectangle 2
- Spiral for triangle
- Rectilineal pattern with 90 -degree rotation for the intersection between rectangle 1 and rectangle 2
- Rectilinear pattern with 120 -degree rotation for the intersection between rectangle 1 and the
  triangle.
- No pattern should be assigned to the intersection between rectangle 2 and the triangle.
- Another pattern should be assigned to the intersection between the 3 shapes.

In order to do this, the ClipperLib library should be used either with Python or C++
(https://www.angusj.com/clipper2/Docs/Overview.htm)

Please send back your code as your response to this test.

# Exercise 2

A rectangular template with dimensions W x H is defined in a 2D cartesian plane where 0 <x<W and 0 < y < H.
You are required to perform **two distinct spatial mappings** to transform a rectilinear pattern etched on this
template:

- Part A (2D Circular Mapping): Derive the coordinate transformation equations to map the rectangle
  onto a 2D ring with an inner radius. In this mapping, the x-axis of the pattern must correspond to the
  angular displacement θ ∈[0,2π], and the y-axis must correspond to the radial distance. Calculate the
  resulting Cartesian coordinates (x′,y′) for the four corners of the rectangle.
- Part B (3D Cylindrical Mapping): Apply a transformation to "wrap" the same rectangular template
  around a vertical cylinder of radius. The x-axis of the rectangle must represent the arc length along the
  cylinder's circumference, while the y-axis represents the vertical height z. Provide the general
  transformation function and determine the 3D coordinates of the corner points if W=2πR.

Calculate the pattern for the 2 cases and represent them in a plot.

# Exercise 3

Articular cartilage is a non-homogeneous tissue composed of three distinct zones: superficial, middle, and
deep, which vary significantly in their cellular organization, collagen fiber orientation, and mechanical
stiffness. Your task is to propose a design for a 3D biomodel that replicates these three layers. You must take
into consideration the specific biomechanical properties (such as Young’s Modulus and permeability) for each
zone to ensure the model functions replicates real tissue. In your response, explain the manufacturing
techniques you would use to create these distinct layers, how you would ensure a seamless interface between
them to prevent delamination, and which professional profiles you would collaborate with to validate the
model's performance against human physiological data.
