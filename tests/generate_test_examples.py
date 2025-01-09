#!/usr/bin/env python3

import random
import numpy as np
import scipy.stats as st

SCIPY_DENSITY_MANIFEST = {
    "norm": {"loc", "scale"},
    "expon": {"loc", "scale"},
    "t": {"df", "loc", "scale"},
    "weibull_min": {"c", "loc", "scale"},
    "gamma": {"a", "loc", "scale"},
    "weibull_max": {"c", "loc", "scale"},
    "beta": {"a", "b", "loc", "scale"},
    "lognorm": {"s", "loc", "scale"},
    "chi": {"df", "loc", "scale"},
    "chi2": {"df", "loc", "scale"},
    "rayleigh": {"loc", "scale"},
    "pareto": {"b", "loc", "scale"},
    "cauchy": {"loc", "scale"},
    "laplace": {"loc", "scale"},
    "f": {"dfn", "dfd", "loc", "scale"}
}


def generate_random_params(dist_name, param_keys):
    """
    Return a dictionary of random-ish valid parameters for the given distribution,
    within some 'reasonable' ranges to avoid zero or negative scale if possible.
    """
    # defaults
    loc = round(random.uniform(-1.0, 1.0), 2)
    scale = round(random.uniform(0.5, 2.0), 2)

    params = {}
    for key in param_keys:
        if key == "loc":
            params["loc"] = loc
        elif key == "scale":
            # ensure scale > 0
            params["scale"] = scale
        elif key in ["a", "b", "c", "df", "dfn", "dfd", "s"]:
            # shape parameters, choose random positive floats
            val = random.uniform(0.5, 3.0)
            # 'dfn'/'dfd' for F distribution must be > 0, we do a modest range
            params[key] = round(val, 2)
        else:
            # fallback
            params[key] = 1.0
    return params


def random_x_for_distribution(dist_name, params):
    """
    Pick an x in some range that is likely relevant for the distribution.
    E.g., if it's 'expon', we might pick x >= loc. For 'weibull_min', etc.
    We'll just do a simple approach: pick x in [loc-1, loc+5].
    """
    loc = params.get("loc", 0.0)
    low = loc - 1.0
    high = loc + 5.0
    x_val = round(random.uniform(low, high), 2)
    return x_val


def main(n=100):
    """
    Generate 'n' examples total across all distributions in the manifest.
    We'll pick random parameter sets for each distribution, compute pdf(x),
    and print out lines for a pytest param list.
    """
    dist_names = list(SCIPY_DENSITY_MANIFEST.keys())
    random.shuffle(dist_names)

    examples = []
    # We won't necessarily get 'n' unique examples per distribution, just total
    # We'll cycle through distributions, but you can adapt as you like
    dist_count = 0
    for _ in range(n):
        dist_name = dist_names[dist_count % len(dist_names)]
        param_keys = SCIPY_DENSITY_MANIFEST[dist_name]
        params = generate_random_params(dist_name, param_keys)
        x_val = random_x_for_distribution(dist_name, params)

        # compute pdf
        dist_class = getattr(st, dist_name, None)
        if dist_class is None:
            continue  # skip unknown
        try:
            dist_obj = dist_class(**params)
            pdf_val = dist_obj.pdf(x_val)
        except Exception as e:
            # If something fails (e.g. invalid params for that dist),
            # skip or handle differently. We'll just skip.
            continue

        examples.append((dist_name, params, x_val, pdf_val))
        dist_count += 1

    # Print them in a format for pytest param
    print("# Here are some random PDF examples for usage in @pytest.mark.parametrize\n")
    for (dname, paramd, xv, pdfv) in examples:
        # Convert params to a python literal
        # paramd might be something like {'loc': 0.12, 'scale': 1.5, 'a':2.3}
        # We'll represent it as a dict in string form
        param_str = ", ".join([f"'{k}': {paramd[k]}" for k in paramd])
        param_str = "{ " + param_str + " }"

        # We'll round pdf for printing
        pdf_str = f"{pdfv:.10g}"
        print(f"('{dname}', {param_str}, {xv}, {pdf_str}),")


if __name__=='__main__':
    main(100)