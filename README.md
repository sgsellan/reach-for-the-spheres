# Reach For the Spheres

This is the official code release for the SIGGRAPH Asia 2023 paper [Reach For the Spheres:
Tangency-Aware Surface Reconstruction of SDFs](https://odedstein.com/projects/reach-for-the-spheres/) by Silvia Sellán, Christopher Batty and Oded Stein.

## Important anouncement

This research code is preserved for scientific replication purposes only, meant to replicate the results from our paper. Most likely, this is **not** the version of the code you want to use. If you just want to run the most up-to-date, maintained version of the algorithm described in our paper, **we STRONGLY RECOMMEND that you instead use the [current version of the `reach_for_the_spheres` function in gpytoolbox](https://gpytoolbox.org/0.2.0/reach_for_the_spheres/)**, which you can install easily though `pip`:
```bash
python -m pip install gpytoolbox
```
and then in a python script
```python
# some sdf data in numpy arrays SDF_POSITIONS, SDF_VALUES
# construct initial mesh
V0, F0 = gpy.icosphere(2)
# call our algorithm
Vr,Fr = gpy.reach_for_the_spheres(SDF_POSITIONS, SDF_VALUES, V0, F0)
```

## How to use this frozen version of the code

*Only if your only goal is to exactly replicate the results in our paper*, we recommend you use the code in this repository. To run it, please use Python 3.10 and compile gpytoolbox (as referenced as a submodule) yourself in Release mode. Please use the conda yml environment provided in this repo. Please run it in the root directory. 

We are very grateful to Abhishek Madan, Chenxi Liu, Sarah Kushner, Selena Ling, and Zoë Marschner for making sure this code compiles on as many machines as possible.
