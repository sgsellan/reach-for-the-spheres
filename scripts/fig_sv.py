# This replicates Fig. 18 in our paper "Reach for the Spheres: Tangency-Aware Surface Reconstruction of SDFs"

# Thanks to our context.py file, we only need this in the header:
from context import *

# Set up gt
V_gt, F_gt = gpy.read_mesh('data/cheburashka.obj')

V_gt, F_gt,_,_ = gpy.decimate(V_gt, F_gt, face_ratio=0.8)

V_gt = 0.8*gpy.normalize_points(V_gt)


save_dir = 'results/sv'

# Check if save_dir exists, if not create it
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


gpy.write_mesh(save_dir+'/ground_truth.obj', V_gt, F_gt)

# Create and abstract SDF function that is the only connection to the shape
P = np.array([[0.0,0.0,0.0],[2.0,0.0,1.0],[4.0,0.0,0.0],[6.0,0.0,1.0]])
P = P/6.0
P = P - 0.5
P = 1.2*P
def sdf(X):
    # gs = 256
    num_samples = 200
    T = np.linspace(0,1,num_samples)
    PT = gpy.catmull_rom_spline(T,P)
    S = np.zeros(X.shape[0]) - 10.0
    for i in range(num_samples):
        th = 2*np.pi*i/num_samples + np.pi/2
        R = np.array([[np.cos(th),0.0,-np.sin(th)],[0,1,0],[np.sin(th),0,np.cos(th)]])
        # print(i)
        displaced_v =  V_gt@R + np.tile(PT[i,:],(V_gt.shape[0],1))
        # print(PT[i,:])
        # S[:,i] =gpytoolbox.signed_distance(GV,displaced_v,f)[0]
        # important = np.where(S < 0.05)[0]
        # print(important)
        S = np.maximum(S,-gpy.signed_distance(X,displaced_v,F_gt,use_cpp=True)[0])
    return -S

# Set up a grid and do marching cubes
n = 20
gx, gy, gz = np.meshgrid(np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1), np.linspace(-1.0, 1.0, n+1))
U = np.vstack((gx.flatten(), gy.flatten(), gz.flatten())).T
S = sdf(U)
np.save(save_dir+'/S.npy', S)
S = np.load(save_dir+'/S.npy')



V_mc, F_mc = gpy.marching_cubes(S, U, n+1, n+1, n+1)
gpy.write_mesh(save_dir+'/mc.obj', V_mc, F_mc)


V0, F0 = gpy.icosphere(2)
V,F = gpy.sdf_flow(U, sdf, V0, F0, S=S, h=0.2, resample=0, callback=None,verbose=True, visualize=True, max_t=10, tol=1e-4, remesh_iterations=10, max_iter=300, sv=True, batch_size=10000, min_h = 0.02)

gpy.write_mesh(save_dir+'/ours.obj', V, F)

ps.init()
ps.register_surface_mesh('ours', V, F)
ps.register_surface_mesh('gt', V_gt, F_gt)
ps.register_surface_mesh('mc', V_mc, F_mc)
ps.show()



    
