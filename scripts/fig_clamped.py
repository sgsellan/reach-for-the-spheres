# This replicates Fig. 17 in our paper "Reach for the Spheres: Tangency-Aware Surface Reconstruction of SDFs"

# Thanks to our context.py file, we only need this in the header:
from context import *

# Set up gt
V_gt, F_gt = gpy.read_mesh('data/squirrel.obj')
V_gt = gpy.normalize_points(V_gt)


save_dir = 'results/clamped/'
# Check if save_dir exists, if not create it
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
gpy.write_mesh(save_dir+'/ground_truth.obj', V_gt, F_gt)

clamps = [1.0, 0.5, 0.25, 0.1, 0.05, 0.01, 0.025]

for clamp in clamps:
    # Create and abstract SDF function that is the only connection to the shape
    sdf = lambda x:  np.clip(gpy.signed_distance(x, V_gt, F_gt)[0],-clamp,+clamp)


    # Set up a grid and do marching cubes
    n = 30
    gx, gy, gz = np.meshgrid(np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1))
    U = np.vstack((gx.flatten(), gy.flatten(), gz.flatten())).T
    V_mc, F_mc =gpy.marching_cubes(sdf(U), U, n+1, n+1, n+1)


    # Call our method, using an icosphere as inigial guess
    V0, F0 = gpy.icosphere(2)
    V,F = gpy.sdf_flow(U, sdf, V0, F0, resample=0, callback=None,verbose=True, visualize=False, max_t=100, tol=1e-4, remesh_iterations=1, max_iter=300, clamp=clamp, min_h = 0.033)

    # Write outputs
    gpy.write_mesh(save_dir+'mc.obj', V_mc, F_mc)
    gpy.write_mesh(save_dir+'final'+str(clamp)+'.obj', V, F)
    