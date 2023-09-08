# This replicates Fig. 19 in our paper "Reach for the Spheres: Tangency-Aware Surface Reconstruction of SDFs"

# Thanks to our context.py file, we only need this in the header:
from context import *

# Set up gt
V_gt, F_gt = gpy.read_mesh('data/scorpion.obj')
V_gt = gpy.normalize_points(V_gt)

# Create and abstract SDF function that is the only connection to the shape
sdf = lambda x: gpy.signed_distance(x, V_gt, F_gt)[0]


# Set up a grid and do marching cubes
n = 50
gx, gy, gz = np.meshgrid(np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1))
U = np.vstack((gx.flatten(), gy.flatten(), gz.flatten())).T
V_mc, F_mc = gpy.marching_cubes(sdf(U), U, n+1, n+1, n+1)


# Set up gt
V_gt, F_gt = gpy.read_mesh('data/table/horse.obj')

V_gt = gpy.normalize_points(V_gt)

# Create and abstract SDF function that is the only connection to the shape
sdf = lambda x: gpy.signed_distance(x, V_gt, F_gt)[0]


V_mc, F_mc = gpy.marching_cubes(sdf(U), U, n+1, n+1, n+1)

save_dir = 'results/singularity/horse'
# Check if save_dir exists, if not create it
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

gpy.write_mesh(save_dir+'/ground_truth.obj', V_gt, F_gt)
mesh_exporter_callback = utility.mesh_exporter(save_dir, 1, track_resampling=False)
def callback(state):
    mesh_exporter_callback(state)
V0, F0 = gpy.icosphere(2)
V,F = gpy.sdf_flow(U, sdf, V0, F0, resample=0, callback=callback,
    min_h = 0.02,
    verbose=True, visualize=True, max_t=100, tol=2*1e-3)

# gpy.write_mesh(save_dir+'/final.obj', V, F)
gpy.write_mesh(save_dir+'/ground_truth.obj', V_gt, F_gt)