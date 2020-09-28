import numpy as np
import numba as nb
from Tools import Types, Functionals


@nb.jit("f8[:](f8[:],f8)", nopython=True, nogil=True)
def gaussian_kernel(x: Types.ndarray, h: float):
    return np.exp(-0.5 * np.power(x, 2.0) / h) / np.sqrt(2.0 * np.pi * h)


@nb.jit("f8[:](f8[:],f8)", nopython=True, nogil=True)
def quartic_kernel(x: Types.ndarray, h: float):
    no_x = len(x)
    output = np.zeros(no_x)

    for i in range(0, no_x):
        z = x[i] / h
        if np.abs(z) < 1.0:
            output[i] = (15.0 / (16.0 * h)) * np.power(1.0 - np.power(x[i] / h, 2.0), 2.0)

    return output


@nb.jit("f8[:](f8[:],f8[:],f8[:],f8)", nopython=True, nogil=True)
def gaussian_kernel_estimator_slv(v_t: Types.ndarray, x_t: Types.ndarray, x: Types.ndarray, h: float):
    no_x = len(x)
    estimator = np.zeros(no_x)

    for i in range(0, no_x):
        k_x_i = gaussian_kernel(x_t - x[i], h)
        estimator[i] = Functionals.scalar_product(v_t, k_x_i) / np.sum(k_x_i)

    return estimator


@nb.jit("f8[:](f8[:],f8[:],f8[:],f8)", nopython=True, nogil=True)
def quartic_kernel_estimator_slv(v_t: Types.ndarray, x_t: Types.ndarray, x: Types.ndarray, h: float):
    no_x = len(x)
    estimator = np.zeros(no_x)

    for i in range(0, no_x):
        k_x_i = quartic_kernel(x_t - x[i], h)
        estimator[i] = Functionals.scalar_product(v_t, k_x_i) / np.sum(k_x_i)

    return estimator