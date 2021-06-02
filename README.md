# Path2JSON

Converts **absolute** SVG paths to a simple JSON format.

For now, you can use Inkscape to convert the SVG to the requisite format.

## Using

First, install dependencies in `requirements.txt`

Provide the SVG to read in the first argument and the output filename as the second argument.

For example:

`python path_json.py logo.svg logo.json`

## Possible future works

- Extension to support relative SVG paths.
- Better validation.

# Format

Generates a list of paths contained in the SVG.
Each path is an array of operations.
Each operation has a batch of arguments, similar to an actual SVG file.

Most are just co-ordinates.

Two exceptions are the Arc curve and the closed path notation.

The closed path (Z) is a no-op.

The arc (A) follows this [MDN documentation](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#elliptical_arc_curve). 
