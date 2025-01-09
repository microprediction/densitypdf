
from densitypdf import density_pdf
import time

if __name__ == "__main__":

    # Example mixture with one scipy normal and one builtin normal
    mixture_spec = {
        "type": "mixture",
        "components": [
            {
                "density": {
                    "type": "scipy",
                    "name": "norm",
                    "params": {"loc": 0, "scale": 1}
                },
                "weight": 0.6
            },
            {
                "density": {
                    "type": "builtin",
                    "name": "normal",
                    "params": {"mu": 2.0, "sigma": 1.0}
                },
                "weight": 0.4
            }
        ]
    }

    # Evaluate the mixture 10,000 times at x=0.0
    # to measure performance
    start_time = time.perf_counter()

    n_iterations = 10000
    for _ in range(n_iterations):
        val = density_pdf(mixture_spec, x=0.0)

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    print(f"Evaluated mixture {n_iterations} times.")
    print(f"Last PDF value at x=0.0: {val}")
    print(f"Total time: {elapsed:.5f} seconds.")
    print(f"Avg time per call: {1000*elapsed / n_iterations:.8f} ms.")
