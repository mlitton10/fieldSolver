import numpy as np
import matplotlib.pyplot as plt


def plot_machine_boundary(f,a, r_wall, z_wall):
    z_range = np.linspace(z_wall[0], z_wall[1], 10, endpoint=True)
    r_range = np.linspace(0, r_wall, 10, endpoint=True)

    a.plot([z_wall[0]]*10, r_range, color='k')
    a.plot([z_wall[1]] * 10, r_range, color='k')
    a.plot(z_range, [r_wall]*10, color='k')
    return f,a