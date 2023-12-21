Installing the virtualenv and creating one virtual env

```
python -m pip install virtualenv
python -m virtualenv hydrant-env
```

After the environment is created we can activate this virtual environment and check its information:

```
source hydrant-env/bin/activate
```

We can then install packages from PyPI or from GitHub repositories:

```
python -m pip install numpy pandas xarray networkx geopandas matplotlib shapely
python -m pip install git+https://github.com/kasra-keshavarz/hydrant
python -m pip install git+https://github.com/ShervanGharari/EASYMORE.git@develop_2.0.0
```

In order to be able to run the examples with jupyter notebook, we need to install jupyter and ipykernel and link it to the virtual environment.

```
python -m pip install jupyter
python -m pip install ipykernel
python -m ipykernel install --name=hydrant-env # Add the new virtual environment to Jupyter
jupyter kernelspec list # list existing Jupyter virtual environments
```
