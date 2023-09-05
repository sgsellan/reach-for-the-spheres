# Here I import only the functions I need for these functions
import numpy as np
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ext/gpytoolbox/src')))
import gpytoolbox as gpy
from .write_mesh import write_mesh

# Generates a callback that can be used as a mesh exporter in sdf_flow
def mesh_exporter(save_dir,
    save_every=1,
    track_resampling=False):
    def callback(state):
        suffix = ".obj" if state['F'].shape[1]==3 else ".npy"
        if state['its']%save_every == 0:
            if track_resampling:
                msg = f"{state['its']//save_every:06}_resampled_{state['resample_counter']}{suffix}"
            else:
                msg = f"{state['its']//save_every:06}{suffix}"
            if state['V_active'] is not None and state['F_active'] is not None:
                write_mesh(os.path.join(save_dir, f"active_{msg}"), state['V_active'], state['F_active'])
            if state['V_inactive'] is not None and state['F_inactive'] is not None:
                write_mesh(os.path.join(save_dir, f"inactive_{msg}"), state['V_inactive'], state['F_inactive'])
            if state['V'] is not None and state['F'] is not None:
                write_mesh(os.path.join(save_dir, f"full_{msg}"), state['V'], state['F'])
        if state['converged'] or state['its']==state['max_iter']-1:
            write_mesh(os.path.join(save_dir, f"final.obj"), state['V'], state['F'])
    return callback
