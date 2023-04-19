# Mandelbrot Set
Mandelbrot set demo implemented using NumPy, Numba, DPNP, and Numba-DPEx.

## What it is
The Mandelbrot set is the set of complex numbers $c$ for which the function 
$f_{c}(z)=z^{2}+c$ does not diverge to infinity when iterated from  $z=0$, i.e., 
for which the sequence $f_{c}(0)$, $f_{c}(f_{c}(0))$, etc., remains bounded in absolute value.

Images of the Mandelbrot set exhibit an elaborate and infinitely complicated boundary 
that reveals progressively ever-finer recursive detail at increasing magnifications

For further details please visit respective [Wikipedia article](https://en.wikipedia.org/wiki/Mandelbrot_set).

## Installation

`conda install -c pycoddiy/label/dev mandelbrot-demo`

## Running demo

From command line type:
`mandelbrot  [command line options]`

* `--variant [numba, numpy, dpnp, numba-dpex]` (default `numpy`) - implementation variant
* `--frames-count` - stop rendering after a specified amount of frames. Default 0 meaning that the demo
  does not stop until user action, e.g. close window
* `--gui` (default) or `--no-gui` - render the evolution of the grid or do the computation only and
  print performance statistics in the end.
* `--task-size` - window size WIDTH, HEIGHT. Example: 1024,800 (default)
