use pyo3::prelude::*;

const A1: f64 = 0.999_999_982_782_301_2;
const A3: f64 = -0.166_666_515_202_236_22;
const A5: f64 = 0.008_332_964_018_218_538;
const A7: f64 = -0.000_198_047_553_009_234_86;
const A9: f64 = 2.598_110_444_084_388e-6;

/// Approximates Legendre using Horner's method.
#[pyfunction]
fn approx_legrende_rust(x: f64) -> PyResult<f64> {
    let x2 = x * x;
    Ok(x * (A1 + x2 * (A3 + x2 * (A5 + x2 * (A7 + x2 * A9)))))
}

/// A Python module implemented in Rust.
#[pymodule]
fn approx_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(approx_legrende_rust, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::approx_legrende_rust;
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
}
