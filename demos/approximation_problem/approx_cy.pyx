# cython: boundscheck=False, wraparound=False, cdivision=True, fast_math=True, language_level=3

# Module-level constants using hex literals (initialized once at import)
cdef double A1 = float.fromhex("0x1.ffffff6c19e14p-1")
cdef double A3 = float.fromhex("-0x1.555541010e1d1p-3")
cdef double A5 = float.fromhex("0x1.110df7f7ef661p-7")
cdef double A7 = float.fromhex("-0x1.9f55f86c5c0ebp-13")
cdef double A9 = float.fromhex("0x1.5cb66525ec44ap-19")


cdef inline double approx_legrende_cy_impl(double x) nogil:
    """Fast approximation of sin(x) for x in [-pi/2, pi/2]."""
    cdef double x2 = x * x
    return x * (A1 + x2 * (A3 + x2 * (A5 + x2 * (A7 + x2 * A9))))


# Public wrapper for Python
def approx_legrende_cy(double x) -> double:
    """Fast approximation of sin(x) for x in [-pi/2, pi/2]."""
    return approx_legrende_cy_impl(x)
