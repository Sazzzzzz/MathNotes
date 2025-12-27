from numba import njit, float64
from math import pi

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


B1 = 1.133648177811748
B3 = -0.1380717765871921
B5 = 0.004490714246554918
B7 = -0.00006770127584215249
B9 = 5.891295330289313e-7
TWO_OVER_PI = 2 / pi


# def approx_chebyshev_native(x: float) -> float:
#    # This is the original implementation of chebyshev approximation
#    # It uses recurrence formula of chebyshev polynomial with 1 step
#     t = TWO_OVER_PI * x
#     two_t = 2 * t
#     b_next, b_curr = 0.0, 0.0
#     b_next, b_curr = B9 + two_t * b_next - b_curr, b_next
#     b_next, b_curr = two_t * b_next - b_curr, b_next
#     b_next, b_curr = B7 + two_t * b_next - b_curr, b_next
#     b_next, b_curr = two_t * b_next - b_curr, b_next
#     b_next, b_curr = B5 + two_t * b_next - b_curr, b_next
#     b_next, b_curr = two_t * b_next - b_curr, b_next
#     b_next, b_curr = B3 + two_t * b_next - b_curr, b_next
#     b_next, b_curr = two_t * b_next - b_curr, b_next
#     b_next, b_curr = B1 + two_t * b_next - b_curr, b_next

#     return t * b_next - b_curr


def approx_chebyshev_native(x: float) -> float:
    # This is an implementation of chebyshev approximation
    # It uses recurrence formula of chebyshev polynomial with 2 steps
    # And should yield better results when used in higher order of approximations
    # however, the actual difference is negligible with 9 order
    b_next, b_curr = 0.0, 0.0
    t = TWO_OVER_PI * x
    four_t2 = 4 * t * t
    four_t2_minus_two = four_t2 - 2
    b_next, b_curr = B9 + four_t2_minus_two * b_next - b_curr, b_next
    b_next, b_curr = B7 + four_t2_minus_two * b_next - b_curr, b_next
    b_next, b_curr = B5 + four_t2_minus_two * b_next - b_curr, b_next
    b_next, b_curr = B3 + four_t2_minus_two * b_next - b_curr, b_next
    return t * B1 + ((four_t2 - 3) * t) * b_next - t * b_curr


FIVE_PI2 = 5 * pi * pi


def approx_Bhāskara_native(x: float) -> float:
    pi_minus_x = pi - x
    return 16 * x * pi_minus_x / (FIVE_PI2 - 4 * x * pi_minus_x)
