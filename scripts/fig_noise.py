# Thanks to our context.py file, we only need this in the header:
from context import *

# Set up rng
rng = np.random.default_rng(1052)

# Set up gt
V_gt, F_gt = gpy.read_mesh('data/spot.obj')
V_gt = gpy.normalize_points(V_gt)

# Create and abstract SDF function that is the only connection to the shape
sdf = lambda x: gpy.signed_distance(x, V_gt, F_gt)[0]


# Set up a grid and do marching cubes
save_dir = 'results/noise/'
for r in [0., 0.001, 0.0025, 0.005]:
	n = 30
	min_h = 0.015
	gx, gy, gz = np.meshgrid(np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1))
	U = np.vstack((gx.flatten(), gy.flatten(), gz.flatten())).T
	V_mc, F_mc = gpy.marching_cubes(sdf(U), U, n+1, n+1, n+1)

	noise = rng.normal(scale=r, size=U.shape[0])
	noisy_sdf = lambda x: sdf(x) + noise

	V0, F0 = gpy.icosphere(2)
	V,F = gpy.sdf_flow(U, noisy_sdf, V0, F0,
		min_h=min_h,
	    verbose=False, visualize=False)

	gpy.write_mesh(save_dir+f'/final_{r}.obj', V, F)

gpy.write_mesh(save_dir+'/ground_truth.obj', V_gt, F_gt)
