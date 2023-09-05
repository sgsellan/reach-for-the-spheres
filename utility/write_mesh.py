# Here I import only the functions I need for these functions
import numpy as np
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ext/gpytoolbox/src')))
import gpytoolbox as gpy

def write_mesh(path, V, F):
    dim = F.shape[1]
    if dim==2:
        np.save(path,{'V':V, 'F':F})
    elif dim==3:
        gpy.write_mesh(path, V, F)
