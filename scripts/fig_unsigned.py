# This replicates Fig. 16 in our paper "Reach for the Spheres: Tangency-Aware Surface Reconstruction of SDFs"


# Thanks to our context.py file, we only need this in the header:
from context import *

# Set up gt
V_gt, F_gt = gpy.read_mesh('data/gollum.obj')
V_gt, F_gt, _, _ = gpy.decimate(V_gt, F_gt, face_ratio=0.5)
V_gt = gpy.normalize_points(V_gt)

# Create and abstract SDF function that is the only connection to the shape
sdf = lambda x: np.sqrt(gpy.squared_distance(x, V_gt, F_gt, use_cpp=True)[0])



save_dir = 'results/unsigned'
# Check if save_dir exists, if not create it
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

gpy.write_mesh(save_dir+'ground_truth.obj', V_gt, F_gt)

ns = [10, 20, 40, 80, 100]
bs = [None, None, None, 10000, 10000] # use batch sizes for larger n for efficiency

for (i,n) in enumerate(ns):
    # Set up a grid and do marching cubes
    # n = 10
    gx, gy, gz = np.meshgrid(np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1))
    U = np.vstack((gx.flatten(), gy.flatten(), gz.flatten())).T
    V_mc, F_mc = gpy.marching_cubes(sdf(U), U, n+1, n+1, n+1)

    V0, F0 = gpy.icosphere(2)
    V0 = 0.8*V0 # Need to make it tighter since it's unsigned

    V,F = gpy.sdf_flow(U, sdf, V0, F0, resample=0, callback=None,
        verbose=True, visualize=True, max_t=10.0, tol=1e-5, inside_outside_test=False, batch_size=bs[i], min_h = 1.0/n )
    
    gpy.write_mesh(save_dir+'/ours_'+str(n)+'.obj', V, F)


# Uncomment to visualize
# ps.init()
# ps.register_surface_mesh('ours', V, F)
# ps.register_surface_mesh('gt', V_gt, F_gt)
# ps.register_surface_mesh('mc', V_mc, F_mc)
# ps.show()


