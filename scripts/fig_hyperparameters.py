# This replicates Fig. 9 in our paper "Reach for the Spheres: Tangency-Aware Surface Reconstruction of SDFs"

# Thanks to our context.py file, we only need this in the header:
from context import *

# Set up gt
V_gt, F_gt = gpy.read_mesh('data/planck.obj')

V_gt = gpy.normalize_points(V_gt)

# Create and abstract SDF function that is the only connection to the shape
sdf = lambda x: gpy.signed_distance(x, V_gt, F_gt)[0]

save_dir = 'results/hyperparameters/'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)


# Set up a grid and do marching cubes
n = 100
gx, gy, gz = np.meshgrid(np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1))
U = np.vstack((gx.flatten(), gy.flatten(), gz.flatten())).T
V_mc, F_mc = gpy.marching_cubes(sdf(U), U, n+1, n+1, n+1)
gpy.write_mesh(save_dir+'/ground_truth.obj', V_gt, F_gt)
gpy.write_mesh(save_dir+'/marching_cubes.obj', V_mc, F_mc)


batch_sizes = [100000]
min_hs = [0.05, 0.02, 0.01, 0.005, 0.001]



V0, F0 = gpy.icosphere(2)
for bs in batch_sizes:
    for min_h in min_hs:
        print('bs: ', bs, ' min_h: ', min_h)
        V,F = gpy.sdf_flow(U, sdf, V0, F0, resample=0, callback=None, min_h = min_h, verbose=True, visualize=False, max_t=100, tol=1e-5, remesh_iterations=1, max_iter=300,batch_size=bs)
        gpy.write_mesh(save_dir+'/final_bs_'+str(bs)+'_mh_'+str(min_h)+'.obj', V, F)

