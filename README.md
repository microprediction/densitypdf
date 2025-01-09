
# Density PDF 
Evaluation of univariate density functions, and mixtures of the same, defined in the `density` package.


## Install

    pip install densitypdf 


## Usage 

    from densitypdf import density_pdf

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

    val = density_pdf(mixture_spec, x=0.0)

   