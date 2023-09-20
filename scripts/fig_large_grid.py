# Thanks to our context.py file, we only need this in the header:
from context import *

# Set up gt
v, f = gpy.read_mesh('data/turtle.obj')
v = gpy.normalize_points(v)


save_dir = 'results/large_grid/'
gpy.write_mesh(save_dir+'/ground_truth.obj', v, f)

# Create and abstract SDF function that is the only connection to the shape
sdf = lambda x: gpy.signed_distance(x, v, f)[0]


# Set up a grid and do marching cubes for initial guess
ns = [20,50,100,200,500]
for n in ns:
    gx, gy, gz = np.meshgrid(np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1))
    GV = np.vstack((gx.flatten(), gy.flatten(), gz.flatten())).T
    V_mc, F_mc = gpy.marching_cubes(sdf(GV), GV, n+1, n+1, n+1)
    gpy.write_mesh(save_dir+'/marching_cubes_'+str(n)+'.obj', V_mc, F_mc)

    V0, F0 = gpy.icosphere(2)
    min_h = 2./n
    tol = 1e-2/n

    mesh_exporter_callback = utility.mesh_exporter(save_dir, 20)
    def callback(state):
        mesh_exporter_callback(state)
    V,F = gpy.sdf_flow(GV, sdf, V0, F0, max_iter=1000000,
        min_h = min_h,
        tol=tol,
        verbose=False, visualize=False)
    gpy.write_mesh(save_dir+'/ours_'+str(n)+'.obj', V, F)
