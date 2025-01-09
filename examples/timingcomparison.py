
from densitypdf import density_pdf
import time


def time_me(spec):
    start_time = time.perf_counter()

    n_iterations = 10000
    for _ in range(n_iterations):
        _ = density_pdf(builtin_spec, x=0.0)
    end_time = time.perf_counter()
    elapsed = end_time - start_time

    print(f"Avg time per call: {1000 * elapsed / n_iterations:.8f} ms.")


if __name__ == "__main__":

    scipy_spec = {
                    "type": "scipy",
                    "name": "norm",
                    "params": {"loc": 2.0, "scale": 1.0}
                }

    builtin_spec = {
                    "type": "builtin",
                    "name": "norm",
                    "params": {"loc": 2.0, "scale": 1.0}
                }

    time_me(scipy_spec)
    time_me(builtin_spec)



