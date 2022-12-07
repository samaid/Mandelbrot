from settings import *

VERSION = 'numba-dpex'

if VERSION == 'numba-dpex':
    import dpnp as np
    import numba_dpex as nb
    from numba import float32, int32

    @nb.func
    def color_by_intensity(intensity):
        c1 = nb.private.array(shape=3, dtype=float32)
        c2 = nb.private.array(shape=3, dtype=float32)
        c3 = nb.private.array(shape=3, dtype=float32)
        c1 = nb.asarray([0.0, 0.0, 0.2])
        c2 = nb.asarray([1.0, 0.7, 0.9])
        c3 = nb.asarray([0.6, 1.0, 0.2])
        if intensity < 0.5:
            return c3*intensity + c2*(1.0-intensity)
        else:
            return c1*intensity + c2*(1.0-intensity)

    @nb.func
    def mandel(x, y):
        z_real = 0.0
        z_imag = 0.0
        for i in range(MAX_ITER):
            z_real = z_real*z_real - z_imag*z_imag + x
            z_imag = 2*z_real*z_imag + y
            if (z_real * z_real + z_imag * z_imag) > 4.0:
                return i
        return MAX_ITER

    @nb.kernel
    def mandel_kernel(values, zoom):
        i = nb.get_global_id(0)
        j = nb.get_global_id(1)
        xx = (i - OFFSET_X)*zoom
        yy = (j - OFFSET_Y)*zoom
        intensity = mandel(xx, yy)/MAX_ITER
        color = color_by_intensity(intensity)
        color = (color * 255.0).astype(int32)
        values[i,j] = color


    def mandelbrot(zoom, values):
        mandel_kernel[(DISPLAY_W, DISPLAY_H), (nb.DEFAULT_LOCAL_SIZE, nb.DEFAULT_LOCAL_SIZE)](values, zoom)
        return values


if VERSION == 'dpnp':
    import dpnp as np

    def color_by_intensity(intensity):
        c1 = np.asarray([0.0, 0.0, 0.2])
        c2 = np.asarray([1.0, 0.7, 0.9])
        c3 = np.asarray([0.6, 1.0, 0.2])
        intensity = np.broadcast_to(intensity[:, :, np.newaxis], intensity.shape + (3,))
        return np.where(intensity < 0.5, c3*intensity + c2*(1.0-intensity), c1*intensity + c2*(1.0-intensity))

    def mandelbrot(x, y, zoom):
        xx = (x - OFFSET_X) * zoom
        yy = (y - OFFSET_Y) * zoom
        c = xx + 1j * yy[:, np.newaxis]

        n_iter = np.full(c.shape, 0)  # 2d array
        z = np.empty(c.shape, np.csingle)  # 2d array too
        mask = (n_iter < MAX_ITER)  # Initialize with True
        for i in range(MAX_ITER):
            z[mask] = z[mask]**2 + c[mask]
            mask = mask & (np.abs(z) <= 2.0)
            n_iter[mask] = i

        intensity = n_iter.T / MAX_ITER
        values = (color_by_intensity(intensity)*255).astype(np.int32)
        return values


if VERSION == 'numba':
    import numpy as np
    import numba as nb


    @nb.jit(fastmath=True, nopython=True, inline='always')
    def color_by_intensity(intensity):
        c1 = np.asarray([0.0, 0.0, 0.2])
        c2 = np.asarray([1.0, 0.7, 0.9])
        c3 = np.asarray([0.6, 1.0, 0.2])
        if intensity < 0.5:
            return c3*intensity + c2*(1.0-intensity)
        else:
            return c1*intensity + c2*(1.0-intensity)


    @nb.jit(fastmath=True, nopython=True, inline='always')
    def mandel(x, y):
        c = complex(x, y)
        z = 0.0j
        for i in range(MAX_ITER):
            z = z*z + c
            if (z.real * z.real + z.imag * z.imag) > 4.0:
                return i
        return MAX_ITER


    @nb.jit(fastmath=True, parallel=True, nopython=True)
    def mandelbrot(zoom, values):
        for x in nb.prange(DISPLAY_W):
            for y in range(DISPLAY_H):
                xx = (x - OFFSET_X)*zoom
                yy = (y - OFFSET_Y)*zoom
                intensity = mandel(xx, yy)/MAX_ITER
                color = color_by_intensity(intensity)
                color = (color*255.0).astype(np.int32)
                values[x, y] = color
        return values

if VERSION == 'numpy':
    import numpy as np

    def color_by_intensity(intensity):
        c1 = np.asarray([0.0, 0.0, 0.2])
        c2 = np.asarray([1.0, 0.7, 0.9])
        c3 = np.asarray([0.6, 1.0, 0.2])
        intensity = np.broadcast_to(intensity[:, :, np.newaxis], intensity.shape + (3,))
        return np.where(intensity < 0.5, c3*intensity + c2*(1.0-intensity), c1*intensity + c2*(1.0-intensity))

    def mandelbrot(x, y, zoom):
        xx = (x - OFFSET_X) * zoom
        yy = (y - OFFSET_Y) * zoom
        c = xx + 1j * yy[:, np.newaxis]

        n_iter = np.full(c.shape, 0)  # 2d array
        z = np.empty(c.shape, np.csingle)  # 2d array too
        mask = (n_iter < MAX_ITER)  # Initialize with True
        for i in range(MAX_ITER):
            z[mask] = z[mask]**2 + c[mask]
            mask = mask & (np.abs(z) <= 2.0)
            n_iter[mask] = i

        intensity = n_iter.T / MAX_ITER
        values = (color_by_intensity(intensity)*255).astype(np.int32)
        return values


class Fractal:
    def __init__(self, zoom):
        self.values = np.full((DISPLAY_W, DISPLAY_H, 3), 0, dtype=np.int32)
        self.zoom = zoom
        self.need_recalculate = True
        self.x = np.linspace(0, DISPLAY_W, num=DISPLAY_W, dtype=np.float32)
        self.y = np.linspace(0, DISPLAY_H, num=DISPLAY_H, dtype=np.float32)

    def set_zoom(self, zoom):
        old_zoom = self.zoom
        if self.zoom != zoom:
            self.need_recalculate = True
            self.zoom = zoom
        return old_zoom

    def calculate(self):
        if VERSION == 'numba':
            self.values = mandelbrot(self.zoom, self.values)

        if VERSION == 'numba-dpex':
            mandelbrot(self.values, self.zoom)

        if VERSION == 'numpy' or VERSION == 'dpnp':
            self.values = mandelbrot(self.x, self.y, self.zoom)
        #self.need_recalculate = False

    def draw(self, surface):
        if VERSION == 'dpnp' or VERSION == 'numba-dpex':
            cpu_values = np.asnumpy(self.values)
            pg.surfarray.blit_array(surface, cpu_values)
        else:
            pg.surfarray.blit_array(surface, self.values)

    def update(self):
        if self.need_recalculate:
            self.calculate()


def main():
    ds, clk = initialize()

    fractal = Fractal(ZOOM)

    do_game = True
    while do_game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                do_game = False

        # Draw objects
        ds.fill(pg.Color('black'))
        fractal.draw(ds)

        # Perform updates
        fractal.update()
        # pg.display.set_caption(f'FPS: {clk.get_fps()}')
        pg.display.set_caption("FPS: {:2.1f}".format(clk.get_fps()))

        # Prepare for next frame
        pg.display.flip()
        clk.tick(FPS)


if __name__ == "__main__":
    main()
