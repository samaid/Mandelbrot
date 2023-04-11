import dpnp as np
import numba_dpex as nb
from numba import float32, int32


@nb.func
def color_by_intensity(intensity):
    c1 = nb.private.array(shape=3, dtype=float32)
    c2 = nb.private.array(shape=3, dtype=float32)
    c3 = nb.private.array(shape=3, dtype=float32)
    c1 = nb.asarray([0.0, 0.0, 0.2], mem_type="private", dype=float32)
    c2 = nb.asarray([1.0, 0.7, 0.9])
    c3 = nb.asarray([0.6, 1.0, 0.2])
    if intensity < 0.5:
        return c3 * intensity + c2 * (1.0 - intensity)
    else:
        return c1 * intensity + c2 * (1.0 - intensity)


@nb.func
def mandel(x, y):
    z_real = 0.0
    z_imag = 0.0
    for i in range(MAX_ITER):
        z_real = z_real * z_real - z_imag * z_imag + x
        z_imag = 2 * z_real * z_imag + y
        if (z_real * z_real + z_imag * z_imag) > 4.0:
            return i
    return MAX_ITER


@nb.kernel
def mandel_kernel(values, zoom):
    i = nb.get_global_id(0)
    j = nb.get_global_id(1)
    xx = (i - OFFSET_X) * zoom
    yy = (j - OFFSET_Y) * zoom
    intensity = mandel(xx, yy) / MAX_ITER
    color = color_by_intensity(intensity)
    color = (color * 255.0).astype(int32)
    values[i, j] = color


def mandelbrot(zoom, values):
    mandel_kernel[(DISPLAY_W, DISPLAY_H), (nb.DEFAULT_LOCAL_SIZE, nb.DEFAULT_LOCAL_SIZE)](values, zoom)
    return values
