import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# Ensure output directory exists
output_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'weno5_comparison.gif')

# Parameters
N = 200
dx = 1.0 / N
x = np.linspace(0, 1, N, endpoint=False)
CFL = 0.4
dt = CFL * dx
T = 1.0
nsteps = int(T / dt)

# Initial Condition: Square Wave
u0 = np.zeros(N)
mask = (x > 0.3) & (x < 0.7)
u0[mask] = 1.0

# Exact Solution (Periodic)
def get_exact(t):
    u_exact = np.zeros(N)
    # Shift x by -t (since wave moves right with speed 1)
    # x_shifted = (x - t) % 1.0
    # But since we want u(x,t) = u0(x-t)
    x_shifted = (x - t) % 1.0
    mask_exact = (x_shifted > 0.3) & (x_shifted < 0.7)
    u_exact[mask_exact] = 1.0
    return u_exact

# --- Upwind Scheme (1st Order) ---
def rhs_upwind(u):
    # u_t + u_x = 0  => u_t = -u_x
    # Backward difference: (u_i - u_{i-1})/dx
    du_dx = (u - np.roll(u, 1)) / dx
    return -du_dx

# --- WENO5 Scheme (5th Order) ---
def weno5_reconstruction(u):
    """
    WENO5 reconstruction of u_{i+1/2} from the left (positive velocity).
    """
    # Stencils for u_{i+1/2}:
    # S0: i-2, i-1, i
    # S1: i-1, i, i+1
    # S2: i, i+1, i+2
    
    # Shifted arrays for vectorization
    # um2 = u_{i-2}, um1 = u_{i-1}, up1 = u_{i+1}, up2 = u_{i+2}
    um2 = np.roll(u, 2)
    um1 = np.roll(u, 1)
    up1 = np.roll(u, -1)
    up2 = np.roll(u, -2)
    
    # Polynomial approximations
    p0 = (2*um2 - 7*um1 + 11*u)/6
    p1 = (-um1 + 5*u + 2*up1)/6
    p2 = (2*u + 5*up1 - up2)/6
    
    # Smoothness indicators (Jiang & Shu)
    beta0 = 13/12 * (um2 - 2*um1 + u)**2 + 1/4 * (um2 - 4*um1 + 3*u)**2
    beta1 = 13/12 * (um1 - 2*u + up1)**2 + 1/4 * (um1 - up1)**2
    beta2 = 13/12 * (u - 2*up1 + up2)**2 + 1/4 * (3*u - 4*up1 + up2)**2
    
    # Weights
    epsilon = 1e-6
    d0 = 0.1
    d1 = 0.6
    d2 = 0.3
    
    alpha0 = d0 / (epsilon + beta0)**2
    alpha1 = d1 / (epsilon + beta1)**2
    alpha2 = d2 / (epsilon + beta2)**2
    
    alpha_sum = alpha0 + alpha1 + alpha2
    w0 = alpha0 / alpha_sum
    w1 = alpha1 / alpha_sum
    w2 = alpha2 / alpha_sum
    
    # Reconstruction
    u_plus_half = w0*p0 + w1*p1 + w2*p2
    return u_plus_half

def rhs_weno5(u):
    # Flux f(u) = u. Since a=1 > 0, we use the reconstruction from the left.
    # Flux at interface i+1/2
    f_plus = weno5_reconstruction(u)
    # Flux at interface i-1/2 is just f_plus shifted right by 1 index
    f_minus = np.roll(f_plus, 1)
    
    # Conservative difference
    return -(f_plus - f_minus) / dx

# --- Time Integration (RK3) ---
def step_rk3(u, rhs_func, dt):
    # Stage 1
    k1 = rhs_func(u)
    u1 = u + dt * k1
    
    # Stage 2
    k2 = rhs_func(u1)
    u2 = 3/4 * u + 1/4 * (u1 + dt * k2)
    
    # Stage 3
    k3 = rhs_func(u2)
    u_new = 1/3 * u + 2/3 * (u2 + dt * k3)
    return u_new

# --- Simulation & Animation ---
u_upwind = u0.copy()
u_weno = u0.copy()

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 1)
ax.set_ylim(-0.2, 1.2)
ax.set_title("Linear Advection: Upwind (1st Order) vs WENO5")
ax.set_xlabel("x")
ax.set_ylabel("u")
ax.grid(True, alpha=0.3)

line_exact, = ax.plot([], [], 'k--', label='Exact', alpha=0.6)
line_upwind, = ax.plot([], [], 'b-', label='Upwind (1st Order)', linewidth=2)
line_weno, = ax.plot([], [], 'r-', label='WENO5', linewidth=2)
ax.legend(loc='upper right')

text_time = ax.text(0.02, 0.95, '', transform=ax.transAxes)

# Pre-compute frames to speed up animation saving
frames = 100
steps_per_frame = nsteps // frames

def init():
    line_exact.set_data([], [])
    line_upwind.set_data([], [])
    line_weno.set_data([], [])
    text_time.set_text('')
    return line_exact, line_upwind, line_weno, text_time

def update(frame):
    global u_upwind, u_weno
    
    current_time = frame * steps_per_frame * dt
    
    # Update solution
    # We do multiple steps per frame to make the animation faster
    if frame > 0:
        for _ in range(steps_per_frame):
            u_upwind = step_rk3(u_upwind, rhs_upwind, dt)
            u_weno = step_rk3(u_weno, rhs_weno5, dt)
    
    # Exact solution
    u_ex = get_exact(current_time)
    
    line_exact.set_data(x, u_ex)
    line_upwind.set_data(x, u_upwind)
    line_weno.set_data(x, u_weno)
    text_time.set_text(f't = {current_time:.2f}')
    
    return line_exact, line_upwind, line_weno, text_time

print(f"Generating animation with {frames} frames...")
ani = animation.FuncAnimation(fig, update, frames=frames+1, init_func=init, blit=True)

print(f"Saving to {output_path}...")
try:
    ani.save(output_path, writer='pillow', fps=15)
    print("Done.")
except Exception as e:
    print(f"Error saving animation: {e}")
