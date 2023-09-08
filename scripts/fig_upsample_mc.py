# This replicates Fig. 12 in our paper "Reach for the Spheres: Tangency-Aware Surface Reconstruction of SDFs"

# Thanks to our context.py file, we only need this in the header:
from context import * 

# Set up gt
v, f = gpy.read_mesh('data/cat-low-resolution.obj')
v = gpy.normalize_points(v)

# Create and abstract SDF function that is the only connection to the shape
sdf = lambda x: gpy.signed_distance(x, v, f)[0]


# Set up a grid and do marching squares for initial guess
n = 20
gx, gy, gz = np.meshgrid(np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1))
h = 2.0/n
GV = np.vstack((gx.flatten(), gy.flatten(), gz.flatten())).T
# V0, E0 = gpy.marching_squares(sdf(GV), GV, n+1, n+1)
sdf_vals = sdf(GV)
V_mc, F_mc = gpy.marching_cubes(sdf_vals, GV, n+1, n+1, n+1)


save_dir = 'results/upsample-mc/'
# Check if save_dir exists, if not create it
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

ns_upsampled = [30,40,50,80,100]
for ns in ns_upsampled:
    print('upsampling to {}'.format(ns))
    gx_2, gy_2, gz_2 = np.meshgrid(np.linspace(-1.0, 1.0, ns+1), np.linspace(-1.0, 1.0, ns+1), np.linspace(-1.0, 1.0, ns+1),indexing='ij')
    GV_2 = np.vstack((gx_2.flatten(order='F'), gy_2.flatten(order='F'), gz_2.flatten(order='F'))).T
    W = gpy.fd_interpolate(GV_2,np.array([n+1,n+1,n+1],dtype=np.int32),h,corner=np.array([-1,-1,-1]))
    sdf_vals_upsampled = W @ sdf_vals
    V_mc_upsampled, F_mc_upsampled = gpy.marching_cubes(sdf_vals_upsampled, GV_2, ns+1, ns+1, ns+1)
    gpy.write_mesh('results/upsample-mc/mc-{}.obj'.format(ns), V_mc_upsampled, F_mc_upsampled)

V0, F0 = gpy.icosphere(2)
U,G = gpy.sdf_flow(GV, sdf, V0, F0, max_iter=2000, h=0.2, tol=1e-3, resample=0, 
                   feature_detection='aggressive',
    inside_outside_test=True, output_sensitive=True, visualize=True, 
    remesh_iterations=1,min_h=0.05)

gpy.write_mesh(save_dir+'/initial.obj', V0, F0)
gpy.write_mesh(save_dir+'/ours.obj', U, G)
gpy.write_mesh(save_dir+'/ground_truth.obj', v, f)
gpy.write_mesh(save_dir+'/marching_cubes.obj', V_mc, F_mc)


ps.init()
ps.register_surface_mesh("ground truth", v, f)
ps.register_surface_mesh("marching cubes", V_mc, F_mc)
ps.register_surface_mesh("initial guess", V0, F0)
ps.register_surface_mesh("ours", U, G)
ps.show()