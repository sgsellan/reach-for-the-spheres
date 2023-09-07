# Thanks to our context.py file, we only need this in the header:
from context import * 

# Set up grountruth mesh
v, f = gpy.read_mesh('data/bob_tri.obj')
v = gpy.normalize_points(v)

# Create and abstract SDF function that is the only connection to the shape
sdf = lambda x: gpy.signed_distance(x, v, f)[0]


# Set up a grid and do marching squares for initial guess
n = 11
gx, gy, gz = np.meshgrid(np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1))
GV = np.vstack((gx.flatten(), gy.flatten(), gz.flatten())).T
V_mc, F_mc = gpy.marching_cubes(sdf(GV), GV, n+1, n+1, n+1)


# Using marching cubes as initial guess
V0 = V_mc.copy()
F0 = F_mc.copy()

# Run it through a remesh is once
V0, F0 = gpy.remesh_botsch(V0, F0, h=0.2, i=10)

# This is to save the results
save_dir = 'results/genus/'
# Check if save_dir exists, if not create it
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
mesh_exporter_callback = utility.mesh_exporter(save_dir, 1)
def callback(state):
    mesh_exporter_callback(state)

# Call main function
U,G = gpy.sdf_flow(GV, sdf, V0, F0, max_iter=2000, h=0.2, tol=1e-3, resample=0, 
    feature_detection='aggressive',
    inside_outside_test=True, output_sensitive=True, 
    visualize = False,  # make this true if you want to watch it run in realtime
    remesh_iterations=1,min_h=0.05, callback=callback)

# Save results
gpy.write_mesh(save_dir+'initial.obj', V0, F0)
gpy.write_mesh(save_dir+'final_swf_flow.obj', U, G)
gpy.write_mesh(save_dir+'ground_truth.obj', v, f)
gpy.write_mesh(save_dir+'marching_cubes.obj', V_mc, F_mc)


# Plot everything
ps.init()
ps.register_surface_mesh("ground truth", v, f)
ps.register_surface_mesh("marching cubes", V_mc, F_mc)
ps.register_surface_mesh("initial guess", V0, F0)
ps.register_surface_mesh("ours", U, G)
ps.show()