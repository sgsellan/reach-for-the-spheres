# Thanks to our context.py file, we only need this in the header:
from context import *

# Set up gt
V_gt, F_gt = gpy.read_mesh('data/koala.obj')
V_gt = gpy.normalize_points(V_gt)

# Create and abstract SDF function that is the only connection to the shape
sdf = lambda x: gpy.signed_distance(x, V_gt, F_gt)[0]


# Set up a grid and do marching cubes
save_dir = 'results/koala/'
ns = [10, 50]
min_hs = [0.02, 0.01]
for n,min_h in zip(ns, min_hs):
	print(f"n: {n}")
	gx, gy, gz = np.meshgrid(np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1))
	U = np.vstack((gx.flatten(), gy.flatten(), gz.flatten())).T
	V_mc, F_mc = gpy.marching_cubes(sdf(U), U, n+1, n+1, n+1)

	V0, F0 = gpy.icosphere(2)
	V,F = gpy.sdf_flow(U, sdf, V0, F0,
	    min_h=min_h,
	    remesh_iterations=3,
	    verbose=False, visualize=False,
	    tol=1e-4)

	gpy.write_mesh(save_dir+f'/initial_{n}.obj', V0, F0)
	gpy.write_mesh(save_dir+f'/final_{n}.obj', V, F)
	gpy.write_mesh(save_dir+f'/marching_cubes_{n}.obj', V_mc, F_mc)

gpy.write_mesh(save_dir+'/ground_truth.obj', V_gt, F_gt)
