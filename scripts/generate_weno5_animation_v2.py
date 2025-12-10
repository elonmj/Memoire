"""
Animation WENO5 avec visualisation du maillage FVM
Inspiré des animations de soutenance FVM avec cellules visibles.

Montre:
1. Le maillage (cellules FVM)
2. Les valeurs moyennes par cellule
3. La reconstruction WENO5 haute résolution
4. La comparaison avec un schéma Upwind diffusif
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.collections import PatchCollection
import os

# Configuration de sortie
output_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'weno5_fvm_animation.gif')

# Palette de couleurs académique
COLORS = {
    'exact': '#2C3E50',        # Gris foncé
    'upwind': '#3498DB',       # Bleu
    'weno5': '#E74C3C',        # Rouge
    'cell_fill': '#ECF0F1',    # Gris clair pour les cellules
    'cell_edge': '#95A5A6',    # Gris moyen pour les bords
    'highlight': '#F39C12',    # Orange pour les highlights
    'flux_arrow': '#27AE60',   # Vert pour les flux
}

# =============================================================================
# Paramètres de simulation
# =============================================================================
N_cells = 40  # Nombre de cellules (visible)
dx = 1.0 / N_cells
x_centers = np.linspace(dx/2, 1 - dx/2, N_cells)
x_edges = np.linspace(0, 1, N_cells + 1)

CFL = 0.4
dt = CFL * dx
T_final = 1.0
n_steps = int(T_final / dt)

# Condition initiale : créneau (square wave)
def initial_condition(x):
    u = np.zeros_like(x)
    u[(x > 0.25) & (x < 0.55)] = 1.0
    return u

# Solution exacte (advection périodique)
def exact_solution(x, t):
    x_shifted = (x - t) % 1.0
    u = np.zeros_like(x)
    u[(x_shifted > 0.25) & (x_shifted < 0.55)] = 1.0
    return u

# =============================================================================
# Schémas numériques
# =============================================================================

def flux_upwind(u):
    """Flux numérique Upwind (1er ordre) - très diffusif"""
    # f_{i+1/2} = u_i (car a = 1 > 0)
    return u.copy()

def flux_weno5(u):
    """
    Reconstruction WENO5 pour le flux à i+1/2.
    Jiang & Shu (1996) - capture les chocs sans oscillations.
    """
    N = len(u)
    f = np.zeros(N)
    
    for i in range(N):
        # Stencils (avec conditions périodiques)
        um2 = u[(i-2) % N]
        um1 = u[(i-1) % N]
        u0  = u[i]
        up1 = u[(i+1) % N]
        up2 = u[(i+2) % N]
        
        # Reconstructions sur chaque stencil
        p0 = (2*um2 - 7*um1 + 11*u0) / 6
        p1 = (-um1 + 5*u0 + 2*up1) / 6
        p2 = (2*u0 + 5*up1 - up2) / 6
        
        # Indicateurs de régularité (smoothness indicators)
        beta0 = 13/12 * (um2 - 2*um1 + u0)**2 + 1/4 * (um2 - 4*um1 + 3*u0)**2
        beta1 = 13/12 * (um1 - 2*u0 + up1)**2 + 1/4 * (um1 - up1)**2
        beta2 = 13/12 * (u0 - 2*up1 + up2)**2 + 1/4 * (3*u0 - 4*up1 + up2)**2
        
        # Poids optimaux
        d0, d1, d2 = 0.1, 0.6, 0.3
        eps = 1e-6
        
        # Poids non-linéaires
        alpha0 = d0 / (eps + beta0)**2
        alpha1 = d1 / (eps + beta1)**2
        alpha2 = d2 / (eps + beta2)**2
        alpha_sum = alpha0 + alpha1 + alpha2
        
        w0 = alpha0 / alpha_sum
        w1 = alpha1 / alpha_sum
        w2 = alpha2 / alpha_sum
        
        # Reconstruction finale
        f[i] = w0*p0 + w1*p1 + w2*p2
    
    return f

def rhs_upwind(u):
    """RHS pour schéma Upwind"""
    f_plus = flux_upwind(u)
    f_minus = np.roll(f_plus, 1)
    return -(f_plus - f_minus) / dx

def rhs_weno5(u):
    """RHS pour schéma WENO5"""
    f_plus = flux_weno5(u)
    f_minus = np.roll(f_plus, 1)
    return -(f_plus - f_minus) / dx

def step_ssprk3(u, rhs_func, dt):
    """Intégration temporelle SSP-RK3 (Strong Stability Preserving)"""
    k1 = rhs_func(u)
    u1 = u + dt * k1
    
    k2 = rhs_func(u1)
    u2 = 0.75*u + 0.25*(u1 + dt*k2)
    
    k3 = rhs_func(u2)
    return u/3 + 2/3*(u2 + dt*k3)

# =============================================================================
# Animation
# =============================================================================

# Initialisation
u_upwind = initial_condition(x_centers)
u_weno = initial_condition(x_centers)

# Figure avec deux sous-graphiques
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
fig.suptitle('Méthode des Volumes Finis (FVM) — Comparaison des Schémas', 
             fontsize=14, fontweight='bold', color='#2C3E50')

# Grille fine pour la solution exacte
x_fine = np.linspace(0, 1, 500)

# Nombre de frames et pas par frame
n_frames = 80
steps_per_frame = max(1, n_steps // n_frames)

def draw_cells(ax, u_values, color_fill, color_edge, alpha=0.3):
    """Dessine les cellules FVM avec leurs valeurs moyennes."""
    patches = []
    for i in range(N_cells):
        rect = Rectangle(
            (x_edges[i], 0), dx, u_values[i],
            facecolor=color_fill, edgecolor=color_edge,
            linewidth=1, alpha=alpha
        )
        patches.append(rect)
    return patches

def init():
    for ax in [ax1, ax2]:
        ax.clear()
    return []

def update(frame):
    global u_upwind, u_weno
    
    # Effacer les axes
    ax1.clear()
    ax2.clear()
    
    # Temps actuel
    current_time = frame * steps_per_frame * dt
    
    # Avancer la simulation
    if frame > 0:
        for _ in range(steps_per_frame):
            u_upwind = step_ssprk3(u_upwind, rhs_upwind, dt)
            u_weno = step_ssprk3(u_weno, rhs_weno5, dt)
    
    # Solution exacte
    u_exact = exact_solution(x_fine, current_time)
    u_exact_cells = exact_solution(x_centers, current_time)
    
    # =========================================================================
    # Graphique 1 : Upwind (1er ordre) - montre la diffusion
    # =========================================================================
    ax1.set_title('Schema Upwind (1er ordre) - Diffusif', fontsize=12, color=COLORS['upwind'])
    
    # Dessiner les cellules FVM
    for i in range(N_cells):
        rect = Rectangle((x_edges[i], 0), dx, max(0, u_upwind[i]),
                         facecolor=COLORS['upwind'], edgecolor='white',
                         linewidth=0.5, alpha=0.6)
        ax1.add_patch(rect)
    
    # Solution exacte
    ax1.plot(x_fine, u_exact, '--', color=COLORS['exact'], linewidth=2, label='Solution exacte', zorder=5)
    
    # Grille du maillage
    for xe in x_edges:
        ax1.axvline(xe, color=COLORS['cell_edge'], linewidth=0.5, alpha=0.5)
    
    ax1.set_xlim(0, 1)
    ax1.set_ylim(-0.1, 1.3)
    ax1.set_ylabel('Densité ρ', fontsize=11)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Annotation
    ax1.text(0.02, 1.15, 'Diffusion numerique visible', fontsize=10, 
             color=COLORS['upwind'], fontweight='bold', transform=ax1.transAxes,
             bbox=dict(boxstyle='round', facecolor='#FDEBD0', edgecolor=COLORS['upwind']))
    
    # =========================================================================
    # Graphique 2 : WENO5 (5e ordre) - haute résolution
    # =========================================================================
    ax2.set_title('Schema WENO5 (5e ordre) - Haute Resolution', fontsize=12, color=COLORS['weno5'])
    
    # Dessiner les cellules FVM
    for i in range(N_cells):
        rect = Rectangle((x_edges[i], 0), dx, max(0, u_weno[i]),
                         facecolor=COLORS['weno5'], edgecolor='white',
                         linewidth=0.5, alpha=0.6)
        ax2.add_patch(rect)
    
    # Solution exacte
    ax2.plot(x_fine, u_exact, '--', color=COLORS['exact'], linewidth=2, label='Solution exacte', zorder=5)
    
    # Grille du maillage
    for xe in x_edges:
        ax2.axvline(xe, color=COLORS['cell_edge'], linewidth=0.5, alpha=0.5)
    
    ax2.set_xlim(0, 1)
    ax2.set_ylim(-0.1, 1.3)
    ax2.set_xlabel('Position x', fontsize=11)
    ax2.set_ylabel('Densité ρ', fontsize=11)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # Annotation
    ax2.text(0.02, 1.15, 'Chocs captures sans oscillation', fontsize=10, 
             color=COLORS['weno5'], fontweight='bold', transform=ax2.transAxes,
             bbox=dict(boxstyle='round', facecolor='#FADBD8', edgecolor=COLORS['weno5']))
    
    # Temps global
    fig.suptitle(f'Methode des Volumes Finis (FVM) - t = {current_time:.2f}', 
                 fontsize=14, fontweight='bold', color='#2C3E50')
    
    plt.tight_layout(rect=(0, 0, 1, 0.95))
    
    return []

print(f"🎬 Génération de l'animation WENO5 avec maillage FVM...")
print(f"   - {N_cells} cellules")
print(f"   - {n_frames} frames")
print(f"   - Temps final T = {T_final}")

ani = animation.FuncAnimation(fig, update, frames=n_frames+1, init_func=init, 
                               blit=False, interval=100)

print(f"💾 Sauvegarde vers {output_path}...")
try:
    ani.save(output_path, writer='pillow', fps=10, dpi=100)
    print(f"✅ Animation sauvegardée avec succès!")
except Exception as e:
    print(f"❌ Erreur: {e}")

plt.close()
