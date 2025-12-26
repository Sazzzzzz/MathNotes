use pyo3::prelude::*;
use std::f64::consts::PI;

const A1: f64 = 0.999_999_982_782_301_2;
const A3: f64 = -0.166_666_515_202_236_22;
const A5: f64 = 0.008_332_964_018_218_538;
const A7: f64 = -0.000_198_047_553_009_234_86;
const A9: f64 = 2.598_110_444_084_388e-6;

const B1: f64 = 1.133_648_177_811_748;
const B3: f64 = -0.138_071_776_587_192_1;
const B5: f64 = 0.004_490_714_246_554_918;
const B7: f64 = -0.000_067_701_275_842_152_49;
const B9: f64 = 5.891_295_330_289_313e-7;

const TWO_OVER_PI: f64 = 2.0 / PI;

/// Approximates Legendre using Horner's method.
#[pyfunction]
#[inline(always)]
fn approx_legrende_rust(x: f64) -> PyResult<f64> {
    let x2 = x * x;
    Ok(x * (A1 + x2 * (A3 + x2 * (A5 + x2 * (A7 + x2 * A9)))))
}

/// Fast Chebyshev approximation of sin(x) for x in [-pi/2, pi/2].
#[pyfunction]
#[inline(always)]
fn approx_chebyshev_rust(x: f64) -> PyResult<f64> {
    let t = TWO_OVER_PI * x;
    let two_t = 2.0 * t;
    let mut b_next = 0.0;
    let mut b_curr = 0.0;

    (b_next, b_curr) = (B9 + two_t * b_next - b_curr, b_next);
    (b_next, b_curr) = (two_t * b_next - b_curr, b_next);
    (b_next, b_curr) = (B7 + two_t * b_next - b_curr, b_next);
    (b_next, b_curr) = (two_t * b_next - b_curr, b_next);
    (b_next, b_curr) = (B5 + two_t * b_next - b_curr, b_next);
    (b_next, b_curr) = (two_t * b_next - b_curr, b_next);
    (b_next, b_curr) = (B3 + two_t * b_next - b_curr, b_next);
    (b_next, b_curr) = (two_t * b_next - b_curr, b_next);
    (b_next, b_curr) = (B1 + two_t * b_next - b_curr, b_next);

    Ok(t * b_next - b_curr)
}

/// A Python module implemented in Rust.
#[pymodule]
fn approx_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(approx_legrende_rust, m)?)?;
    m.add_function(wrap_pyfunction!(approx_chebyshev_rust, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::{approx_chebyshev_rust, approx_legrende_rust};
    use approx::assert_relative_eq;

    #[test]
    fn test_approx_legrende_rust() {
        let test_values = [1.0];
        let expected_values = [0.8414709848078965];
        for (&input, &expected) in test_values.iter().zip(expected_values.iter()) {
            let result = approx_legrende_rust(input).unwrap();
            assert_relative_eq!(result, expected, epsilon = 1e-6);
        }
    }

    #[test]
    fn test_approx_chebyshev_rust() {
        let test_values = [1.0];
        let expected_values = [0.8414709848078965];
        for (&input, &expected) in test_values.iter().zip(expected_values.iter()) {
            let result = approx_chebyshev_rust(input).unwrap();
            assert_relative_eq!(result, expected, epsilon = 1e-6);
        }
    }
}
