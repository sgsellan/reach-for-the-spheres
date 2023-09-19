# This was run on macOS.

# Thanks to our context.py file, we only need this in the header:
from context import *

# Set up gt
filename = "data/pngs/springer.png"
V_gt = gpy.png2poly(filename)[0]
V_gt = V_gt[::5,:]
V_gt = gpy.normalize_points(V_gt)
F_gt = gpy.edge_indices(V_gt.shape[0],closed=True)

# Create and abstract SDF function that is the only connection to the shape
sdf = lambda x: gpy.signed_distance(x, V_gt, F_gt)[0]


# Set up a grid and do marching squares
n = 30
gx, gy = np.meshgrid(np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1))
U = np.vstack((gx.flatten(), gy.flatten())).T
V_ms, F_ms = gpy.marching_squares(sdf(U), U, n+1, n+1)

V0, F0 = gpy.regular_circle_polyline(12)
V,F = gpy.sdf_flow(U, sdf, V0, F0, min_h=0.03,
    max_t=15.,
    verbose=False, visualize=False)

save_dir = 'results/sharp_2d/'
utility.write_mesh(save_dir+'/initial.npy', V0, F0)
utility.write_mesh(save_dir+'/final.npy', V, F)
utility.write_mesh(save_dir+'/ground_truth.npy', V_gt, F_gt)
utility.write_mesh(save_dir+'/marching_squares.npy', V_ms, F_ms)
