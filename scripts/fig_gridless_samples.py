# Thanks to our context.py file, we only need this in the header:
from context import *

# Set up gt
V_gt, F_gt = gpy.read_mesh('data/strawberry.obj')
V_gt = gpy.normalize_points(V_gt)

# Create and abstract SDF function that is the only connection to the shape
sdf = lambda x: gpy.signed_distance(x, V_gt, F_gt)[0]


# Set up a grid and do marching cubes
n = 12
gx, gy, gz = np.meshgrid(np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1))
U = np.vstack((gx.flatten(), gy.flatten(), gz.flatten())).T
V_mc, F_mc = gpy.marching_cubes(sdf(U), U, n+1, n+1, n+1)

# Try to do some smarter sampling by sampling around smart sphere
N = gpy.per_face_normals(V_gt,F_gt)
rng = np.random.default_rng(432)
nrand = U.shape[0]
Us,I,_ = gpy.random_points_on_mesh(V_gt, F_gt, nrand, rng=rng, return_indices=True)
Us += 0.1*rng.normal(size=(nrand))[:,None]*N[I,:]
# rng = np.random.default_rng(92)
# nrand = U.shape[0]
# Us = rng.normal(size=(nrand,3))
# Us /= np.linalg.norm(Us, axis=-1)[:,None]
# Us += 0.1*rng.normal(size=(nrand,3))

save_dir = 'results/gridless_samples/'
V0, F0 = gpy.icosphere(2)
V,F = gpy.sdf_flow(U, sdf, V0, F0, min_h=0.06, tol=1e-3, verbose=False, visualize=False)
Vs,Fs = gpy.sdf_flow(Us, sdf, V0, F0, min_h=0.06, tol=1e-3, verbose=False, visualize=False)

gpy.write_mesh(save_dir+'/initial.obj', V0, F0)
gpy.write_mesh(save_dir+'/grid_sdf_flow.obj', V, F)
gpy.write_mesh(save_dir+'/gridless_sdf_flow.obj', Vs, Fs)
gpy.write_mesh(save_dir+'/ground_truth.obj', V_gt, F_gt)
gpy.write_mesh(save_dir+'/marching_cubes.obj', V_mc, F_mc)
np.save(save_dir+'/grid_pts.npy', U)
np.save(save_dir+'/gridless_pts.npy', Us)
