# This replicates Fig. 8 in our paper "Reach for the Spheres: Tangency-Aware Surface Reconstruction of SDFs"

# Thanks to our context.py file, we only need this in the header:
from context import *

save_dir = 'results/hr/'
# Check if save_dir exists, if not create it
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

meshes = ['igea', 'bunny']
for mesh in meshes:
    # Set up gt
    V_gt, F_gt = gpy.read_mesh('data/' + mesh + '.obj')
    # V_gt, F_gt = gpy.read_mesh('data/scorpion.obj')
    V_gt = gpy.normalize_points(V_gt)

    # Create and abstract SDF function that is the only connection to the shape
    sdf = lambda x: gpy.signed_distance(x, V_gt, F_gt)[0]


    # Set up a grid and do marching cubes
    n = 100
    gx, gy, gz = np.meshgrid(np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1))
    U = np.vstack((gx.flatten(), gy.flatten(), gz.flatten())).T
    V_mc, F_mc = gpy.marching_cubes(sdf(U), U, n+1, n+1, n+1)


    
    # mesh_exporter_callback = utility.mesh_exporter(save_dir, 5, track_resampling=False)
    # def callback(state):
    #     mesh_exporter_callback(state)
    V0, F0 = gpy.icosphere(2)
    V,F = gpy.sdf_flow(U, sdf, V0, F0, resample=0, callback=None,
        min_h = 0.008,
        verbose=True, visualize=True, max_t=100, tol=1e-4, remesh_iterations=1, max_iter=300,batch_size=20000)

    # ps.init()
    # ps.register_surface_mesh('ours', V, F)
    # ps.register_surface_mesh('gt', V_gt, F_gt)
    # ps.register_surface_mesh('mc', V_mc, F_mc)
    # ps.show()

    gpy.write_mesh(save_dir+'/initial_' + mesh + '.obj', 0.5*V0, F0)
    gpy.write_mesh(save_dir+'/final_swf_flow_' + mesh + '.obj', V, F)
    gpy.write_mesh(save_dir+'/ground_truth_' + mesh + '.obj', V_gt, F_gt)
    gpy.write_mesh(save_dir+'/marching_cubes_' + mesh + '.obj', V_mc, F_mc)
