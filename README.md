# subspace

A cadCAD Design Digital Twin for Subspace Network Economic Dynamics.


*A stock and flow description on the tokeconomics of Subspace. This model uses this as the departure point for the dynamics being simulated.*

## How to run it

- Option 1 (CLI): Just pass `python -m subspace_model`
This will generate an pickled file at `data/simulations/` using the default single run
system parameters & initial state.
    - To perform a multiple run, pass `python -m subspace_model -e`
- Option 2 (cadCAD-tools easy run method): Import the objects at `subspace_model/__init__.py`
and use them as arguments to the `cadCAD_tools.execution.easy_run` method. Refer to `subspace_model/__main__.py` to an example.

## File structure

```
.
├── LICENSE
├── README.md
├── SPEC.md
├── app: The `streamlit` app
│   ├── assets
│   │   ├── icon.png
│   │   └── logo.png
│   ├── chart.py
│   ├── const.yaml
│   ├── description.py
│   ├── glossary.py
│   ├── main.py
│   ├── model.py
│   └── utils.py
├── subspace_model: the `cadCAD` model as encapsulated by a Python Module
│   ├── __init__.py
│   ├── __main__.py
│   ├── experiment.py: Code for running experiments
│   ├── logic.py: All logic for substeps
│   ├── params.py: System parameters
│   ├── structure.py: The PSUB structure
│   └── types.py: Types used in model
├── notebooks: Notebooks for aiding in development
├── profiling
│   ├── output.png
│   ├── output.pstats
│   └── profile_default_run.sh
├── requirements-dev.txt: Dev requirements
├── requirements.txt: Production requirements
└── tests: Test scenarios
    ├── __init__.py
    └── test_scenario.py
```

## What is cadCAD
## Installing cadCAD for running this repo

### 1. Pre-installation Virtual Environments with [`venv`](https://docs.python.org/3/library/venv.html) (Optional):
It's a good package managing practice to create an easy to use virtual environment to install cadCAD. You can use the built in `venv` package.

***Create** a virtual environment:*
```bash
$ python3 -m venv ~/cadcad
```

***Activate** an existing virtual environment:*
```bash
$ source ~/cadcad/bin/activate
(cadcad) $
```

***Deactivate** virtual environment:*
```bash
(cadcad) $ deactivate
$
```

### 2. Installation: 
Requires [>= Python 3.6](https://www.python.org/downloads/) 

**Install Using [pip](https://pypi.org/project/cadCAD/)** 
```bash
$ pip3 install cadcad==0.4.28
```

**Install all packages with requirement.txt**
```bash
$ pip3 install -r requirements.txt
