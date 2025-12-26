from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        Extension(
            "approx_cy",
            ["approx_cy.pyx"],
            extra_compile_args=["-O3", "-ffast-math", "-march=native"],
        )
    ),
)
