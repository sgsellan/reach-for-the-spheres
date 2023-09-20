# ran on macOS

# Thanks to our context.py file, we only need this in the header:
from context import *

# Set up gt
V_gt, F_gt = gpy.read_mesh('data/tower.obj')
V_gt = gpy.normalize_points(V_gt)

# Create and abstract SDF function that is the only connection to the shape
sdf = lambda x: gpy.signed_distance(x, V_gt, F_gt)[0]


# Set up a grid and do marching cubes
n = 70
gx, gy, gz = np.meshgrid(np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1))
U = np.vstack((gx.flatten(), gy.flatten(), gz.flatten())).T
V_mc, F_mc = gpy.marching_cubes(sdf(U), U, n+1, n+1, n+1)


save_dir = 'results/frame_by_frame_flow_3d/'
mesh_exporter_callback = utility.mesh_exporter(save_dir, 1, track_resampling=True)
def callback(state):
    mesh_exporter_callback(state)
V0, F0 = gpy.icosphere(2)
V,F = gpy.sdf_flow(U, sdf, V0, F0, callback=callback,
    batch_size=0.,
    min_h = 0.02,
    verbose=False, visualize=False)

gpy.write_mesh(save_dir+'/initial.obj', V0, F0)
gpy.write_mesh(save_dir+'/final_swf_flow.obj', V, F)
gpy.write_mesh(save_dir+'/ground_truth.obj', V_gt, F_gt)
gpy.write_mesh(save_dir+'/marching_cubes.obj', V_mc, F_mc)
