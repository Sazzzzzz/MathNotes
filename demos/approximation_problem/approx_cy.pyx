# cython: boundscheck=False, wraparound=False, cdivision=True, fast_math=True, language_level=3

from libc.math cimport M_PI, sin

# Module-level constants using hex literals (initialized once at import)
cdef double A1 = <double>float.fromhex("0x1.ffffff6c19e14p-1")
cdef double A3 = <double>float.fromhex("-0x1.555541010e1d1p-3")
cdef double A5 = <double>float.fromhex("0x1.110df7f7ef661p-7")
cdef double A7 = <double>float.fromhex("-0x1.9f55f86c5c0ebp-13")
cdef double A9 = <double>float.fromhex("0x1.5cb66525ec44ap-19")
cdef double TWO_OVER_PI = 2.0 / M_PI

cdef inline double approx_legrende_cy_impl(double x) nogil:
    """Fast approximation of sin(x) for x in [-pi/2, pi/2]."""
    cdef double x2 = x * x
    return x * (A1 + x2 * (A3 + x2 * (A5 + x2 * (A7 + x2 * A9))))


cdef double B1 = <double>1.133648177811748
cdef double B3 = <double>-0.1380717765871921
cdef double B5 = <double>0.004490714246554918
cdef double B7 = <double>-0.00006770127584215249
cdef double B9 = <double>5.891295330289313e-7

cdef inline double approx_chebyshev_cy_impl(double x) nogil:
    cdef double t = TWO_OVER_PI * x
    """Fast Chebyshev approximation of sin(x) for x in [-pi/2, pi/2]."""
    cdef double two_t = 2.0 * t
    cdef double b_next = 0.0
    cdef double b_curr = 0.0
    cdef double temp
    
    b_next, b_curr = B9 + two_t * b_next - b_curr, b_next
    temp = b_next
    b_next = two_t * b_next - b_curr
    b_curr = temp
    
    temp = b_next
    b_next = B7 + two_t * b_next - b_curr
    b_curr = temp
    
    temp = b_next
    b_next = two_t * b_next - b_curr
    b_curr = temp
    
    temp = b_next
    b_next = B5 + two_t * b_next - b_curr
    b_curr = temp
    
    temp = b_next
    b_next = two_t * b_next - b_curr
    b_curr = temp
    
    temp = b_next
    b_next = B3 + two_t * b_next - b_curr
    b_curr = temp
    
    temp = b_next
    b_next = two_t * b_next - b_curr
    b_curr = temp
    
    temp = b_next
    b_next = B1 + two_t * b_next - b_curr
    b_curr = temp
    
    return t * b_next - b_curr

cdef double C3 = <double>-0.1450618133068681
cdef double C1 = <double>0.9887922330533080
cdef inline double approx_legrende_cy_3ord_impl(double x) nogil:
    cdef double x2 = x * x
    return x * (C1 + x2 * C3)

# Public wrapper for Python
def approx_legrende_cy(double x) -> double:
    """Fast approximation of sin(x) for x in [-pi/2, pi/2]."""
    return approx_legrende_cy_impl(x)


def approx_chebyshev_cy(double x) -> double:
    """Fast Chebyshev approximation of sin(x) for x in [-pi/2, pi/2]."""
    return approx_chebyshev_cy_impl(x)

def approx_legrende_cy_3ord(double x) -> double:
    """Fast 3rd order Legendre approximation of sin(x) for x in [-pi/2, pi/2]."""
    return approx_legrende_cy_3ord_impl(x)

# Lookup table configuration
DEF TABLE_SIZE = 8192

cdef double MIN_X = -M_PI / 2.0
cdef double MAX_X = M_PI / 2.0
cdef double RANGE = M_PI
cdef double STEP = RANGE / (TABLE_SIZE - 1)
cdef double INV_STEP = (TABLE_SIZE - 1) / RANGE

# Pre-compute lookup tables at module initialization
cdef double[TABLE_SIZE] LOOKUP_TABLE

cdef int _initialized = 0

cdef void _init_tables() noexcept nogil:
    """Initialize lookup tables (called once)."""
    cdef int i
    for i in range(TABLE_SIZE):
        LOOKUP_TABLE[i] = sin(MIN_X + i * STEP)


def init_lut():
    """Initialize lookup tables (called from Python)."""
    global _initialized
    if not _initialized:
        _init_tables()
        _initialized = 1


cdef inline double approx_lut_cy_impl(double x) nogil:
    """
    Fast lookup table approximation with linear interpolation.
    
    The magic:
    - Pre-computed table eliminates sin() computation
    - Linear interpolation between nearest points
    - All operations are simple arithmetic (fast!)
    """
    # Map x to table index
    cdef double idx_float = (x - MIN_X) * INV_STEP
    cdef int idx_low = <int>idx_float
    cdef double fraction = idx_float - idx_low
    
    # Bounds check
    if idx_low < 0:
        return LOOKUP_TABLE[0]
    if idx_low >= TABLE_SIZE - 1:
        return LOOKUP_TABLE[TABLE_SIZE - 1]
    
    # Linear interpolation: y = y0 + t * (y1 - y0)
    cdef double y0 = LOOKUP_TABLE[idx_low]
    cdef double y1 = LOOKUP_TABLE[idx_low + 1]
    
    return y0 + fraction * (y1 - y0)


# Python wrappers
def approx_lut_cy(double x):
    """Lookup table with linear interpolation (1024 entries)."""
    return approx_lut_cy_impl(x)


# Initialize tables when module is imported
init_lut()