from magnetSolver import CurrentLoopSolve
import numpy as np
from tqdm import tqdm

if __name__ == "__main__":

    r_space = np.linspace(0.0, 0.4, 500)
    z_space = np.linspace(0, 2, 1000)

    R, Z = np.meshgrid(r_space, z_space)
    coordinate_system = [Z, R]

    coils = {'M1': {'current': 100, 'coordinates': coordinate_system, 'position': (0.1, 0.5)},
             'M2': {'current': 100, 'coordinates': coordinate_system, 'position': (0.5, 0.5)},
             'M3': {'current': 100, 'coordinates': coordinate_system, 'position': (1, 0.5)},
             'M4': {'current': 100, 'coordinates': coordinate_system, 'position': (1.5, 0.5)},
             'M15': {'current': 100, 'coordinates': coordinate_system, 'position': (0.1, 0.5)},
             'M2123': {'current': 100, 'coordinates': coordinate_system, 'position': (0.5, 0.5)},
             'M312': {'current': 100, 'coordinates': coordinate_system, 'position': (1, 0.5)},
             'M4123': {'current': 100, 'coordinates': coordinate_system, 'position': (1.5, 0.5)},
             'M1523': {'current': 100, 'coordinates': coordinate_system, 'position': (0.1, 0.5)},
             'M2723': {'current': 100, 'coordinates': coordinate_system, 'position': (0.5, 0.5)},
             'M31256': {'current': 100, 'coordinates': coordinate_system, 'position': (1, 0.5)},
             'M4772': {'current': 100, 'coordinates': coordinate_system, 'position': (1.5, 0.5)}
             }

    B_r_total = np.zeros(R.shape)
    B_z_total = np.zeros(Z.shape)

    for magnet, magnet_settings in tqdm(coils.items()):
        magnetSolver = CurrentLoopSolve(**magnet_settings)
        B_r, B_z = magnetSolver.solve_field()
        B_r_total += B_r
        B_z_total += B_z