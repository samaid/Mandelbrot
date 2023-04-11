import argparse


def int_tuple(tuple_str):
    return tuple(map(int, tuple_str.split(",")))


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Mandelbrot Set")
    parser.add_argument(
        "--variant",
        help="Implementation variant",
        type=str.casefold,
        choices=["numpy", "numba", "dpnp", "numba-dpex"],
        default="numpy",
    )
    parser.add_argument(
        "--parallel",
        help="Keyword argument parallel= for @njit. Used along with --variant numba. Default --no-parallel",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--frames-count",
        help="Stop game after specified amount of frames (default 0 - no stop frame)",
        type=int,
        default=0,
    )
    parser.add_argument(
        "--gui",
        help="Render the evolution of the grid or do computation only and "
        "print statistics in the end. Default --no-gui",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--stats",
        help="Either display statistics in gui while running or not. Default --no-stats",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    w = 800
    h = 600
    parser.add_argument(
        "--task-size",
        help=f"Size of the grid. E.g. 800,600. Default {w},{h}",
        type=int_tuple,
        default=int_tuple(f"{w},{h}"),
    )

    args, _ = parser.parse_known_args(argv)
    return args
