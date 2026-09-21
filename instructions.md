### Text & Typographic Settings
## Banner Text (text): The exact text string rendered onto the plate.   
## Style (style):

* Solid: Generates filled 2D letter geometry and extrudes it directly.

* Outline: Takes the outer boundary of each glyph, expands it outward by outline_width using a 2D offset operation, and then subtracts the original letter interior. This produces hollow/stencil-style raised walls.

* Outline (mm) (outline_width): Used only when Style is set to Outline. It specifies the radial thickness of the outline wall in millimetres before extrusion.   
Unknown

## Pre-installed Font (selected_font): 
Selects any .ttf or .otf file sitting inside your container's ./fonts/ directory.   

Or Upload TTF/OTF Font (custom_font_file): Accepts an uploaded font file from your computer. The backend streams this into a temporary file on the container filesystem so the OpenCASCADE font engine can parse the Bezier curves directly.   

* Font Size (pt/mm) (font_size): The nominal typographical cap-height of the letters in millimetres. Increasing this scales the entire text string proportionally along both the X and Y axes.   

* Relief / Height (mm) (text_relief): How far the text projects vertically upwards from the surface of the baseplate along the Z-axis. For dual-colour or manual filament-swap 3D prints, this determines how many layers of the second colour will be printed.   

* Baseplate & Boundary Settings
Plate Thickness (mm) (plate_thickness): The vertical Z-height (depth) of the backing plate beneath the text.   

* Padding X (mm) (padding_x): The horizontal margin added to both the left and right sides beyond the measured bounding box of the text.

Total Plate Width=Text Bounding Box Width+(2×padding_x)
Padding Y (mm) (padding_y): The vertical margin added to both the top and bottom edges beyond the measured bounding box of the text.

Total Plate Height=Text Bounding Box Height+(2×padding_y)
Corner Radius (mm) (corner_radius): The fillet radius applied to the four vertical corners of the baseplate. Setting this to 0 gives sharp 90 
∘ corners. The backend includes a safety clamp:   

Python
max_rad = min(plate_w, plate_h) / 2.1
This ensures the corner radius can never exceed half the shortest plate dimension, preventing the geometric engine from crashing if a radius larger than the plate is entered.

Viewport HUD (Heads-Up Display)
Dimensions: The real-world bounding-box dimensions of the generated STL (X×Y×Z in millimetres).   
Unknown

Triangles: The total polygon count (facet count) of the raw binary triangular mesh.   
Unknown
