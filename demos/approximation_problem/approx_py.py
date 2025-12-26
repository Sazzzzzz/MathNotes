from numba import njit, float64

# A1 = 0.99999998278230118213
A1 = float.fromhex("0x1.ffffff6c19e14p-1")
# A3 = -0.16666651520223622156
A3 = float.fromhex("-0x1.555541010e1d1p-3")
# A5 = 0.0083329640182185384478
A5 = float.fromhex("0x1.110df7f7ef661p-7")
# A7 = -0.00019804755300923485525
A7 = float.fromhex("-0x1.9f55f86c5c0ebp-13")
# A9 = 2.5981104440843880716e-6
A9 = float.fromhex("0x1.5cb66525ec44ap-19")


def approx_legrende_native(x: float) -> float:
    x2 = x * x
    return x * (A1 + x2 * (A3 + x2 * (A5 + x2 * (A7 + x2 * A9))))


@njit(
    float64(float64),
    fastmath=True,
)
def approx_legrende_jit(x: float) -> float:
    x2 = x * x
    return x * (A1 + x2 * (A3 + x2 * (A5 + x2 * (A7 + x2 * A9))))
