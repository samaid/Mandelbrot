from mandelbrot_demo.impl.arg_parser import parse_args

RUN_VERSION = parse_args().variant

if RUN_VERSION == "Numba".casefold():
    from mandelbrot_demo.impl.impl_numba import mandelbrot, init_values, asnumpy
elif RUN_VERSION == "NumPy".casefold():
    from mandelbrot_demo.impl.impl_numpy import mandelbrot, init_values, asnumpy
elif RUN_VERSION == "DPNP".casefold():
    from mandelbrot_demo.impl.impl_dpnp import mandelbrot, init_values, asnumpy
elif RUN_VERSION == "Numba-DPEX".casefold():
    from mandelbrot_demo.impl.impl_numba_dpex import mandelbrot, init_values, asnumpy
