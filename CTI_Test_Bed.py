import numpy as np
import matplotlib.pyplot as plt
from magnetSolver import MagnetSolve
from coil_geometry import CoilGeometry

rc_dict = {"figure.autolayout": True, "font.family": 'serif', 'font.size': 18.0, 'lines.linewidth': 2.5,
           'axes.titlepad': 8.0,
           'xtick.minor.visible': True, 'ytick.minor.visible': True, 'axes.linewidth': 2.0, 'xtick.major.width': 2.0,
           'xtick.direction': 'in',
           'ytick.direction': 'in', 'ytick.major.width': 2.3, 'xtick.minor.width': 1.0, 'ytick.minor.width': 1.0,
           'xtick.major.size': 8.0, 'ytick.major.size': 8.0,
           'xtick.minor.size': 4.0, 'ytick.minor.size': 4.0, 'savefig.pad_inches': 0.05}

plt.rcParams.update(rc_dict)

if __name__ == "__main__":

    # define the spatial extent over which to compute the magnetic field
    r_space = np.linspace(0, 0.3, 500)
    z_space = np.linspace(0, 3, 1000)

    R, Z = np.meshgrid(r_space, z_space)
    coordinate_system = [Z, R]

    # Define the currents in each magnet coil section
    I_1 = 10.0
    I_2 = 10.0
    I_3 = 10.0

    # radius of the wall for some plotting features
    r_wall = 0.22

    # Magnet Coil parameters for each section of the machine
    section_1_coils = {
        'M1_1': {'current': I_1, 'position': (0.0, 0.308), 'width': 0.05715, 'depth': 0.0889, 'n_turns': 305},
        'M1_2': {'current': I_1, 'position': (0.1, 0.308), 'width': 0.05715, 'depth': 0.0889, 'n_turns': 305},
        'M1_3': {'current': I_1, 'position': (.385, 0.308), 'width': 0.05715, 'depth': 0.0889, 'n_turns': 305},
        'M1_4': {'current': I_1, 'position': (0.59, 0.308), 'width': 0.05715, 'depth': 0.0889, 'n_turns': 305},
        'M1_5': {'current': I_1, 'position': (0.8, 0.308), 'width': 0.05715, 'depth': 0.0889, 'n_turns': 305},
        'M1_6': {'current': I_1, 'position': (1.0, 0.308), 'width': 0.05715, 'depth': 0.0889, 'n_turns': 305},
        'M1_7': {'current': I_1, 'position': (1.2, 0.308), 'width': 0.05715, 'depth': 0.0889, 'n_turns': 305}}

    section_2_coils = {
        'M2_1': {'current': I_2, 'position': (1.27 + .095, 0.297), 'width': 0.05715, 'depth': 0.06985,
                 'n_turns': 31},
        'M2_2': {'current': I_2, 'position': (1.27 + .36, 0.297), 'width': 0.05715, 'depth': 0.06985,
                 'n_turns': 31},
        'M2_3': {'current': I_2, 'position': (1.27 + .585, 0.297), 'width': 0.05715, 'depth': 0.06985,
                 'n_turns': 31},
        'M2_4': {'current': I_2, 'position': (1.27 + .785, 0.297), 'width': 0.05715, 'depth': 0.06985,
                 'n_turns': 31},
        'M2_5': {'current': I_2, 'position': (1.27 + .99, 0.297), 'width': 0.05715, 'depth': 0.06985,
                 'n_turns': 31},
        'M2_6': {'current': I_2, 'position': (1.27 + 1.21, 0.297), 'width': 0.05715, 'depth': 0.06985,
                 'n_turns': 31},
        'M2_7': {'current': I_2, 'position': (1.27 + 1.305, 0.297), 'width': 0.05715, 'depth': 0.06985,
                 'n_turns': 31},
        'M2_8': {'current': I_2, 'position': (1.27 + 1.415, 0.297), 'width': 0.05715, 'depth': 0.06985,
                 'n_turns': 31}}

    section_3_coils = {
        'M3_1': {'current': I_3, 'position': (1.27 + 1.245 + 0.30 + .025, 0.355), 'width': 0.01905, 'depth': 0.0889,
                 'n_turns': 18},
        'M3_2': {'current': I_3, 'position': (1.27 + 1.245 + 0.30 + .076, 0.355), 'width': 0.01905, 'depth': 0.0889,
                 'n_turns': 18},
        'M3_3': {'current': I_3, 'position': (1.27 + 1.245 + 0.30 + .14, 0.355), 'width': 0.01905, 'depth': 0.0889,
                 'n_turns': 18},
        'M3_4': {'current': I_3, 'position': (1.27 + 1.245 + 0.30 + .203, 0.355), 'width': 0.01905, 'depth': 0.0889,
                 'n_turns': 18},
        'M3_5': {'current': I_3, 'position': (1.27 + 1.245 + 0.30 + .343, 0.355), 'width': 0.01905, 'depth': 0.0889,
                 'n_turns': 18},
        'M3_6': {'current': I_3, 'position': (1.27 + 1.245 + 0.3 + .451, 0.355), 'width': 0.01905, 'depth': 0.0889,
                 'n_turns': 18}
    }

    CTI_test_bed_coils = {'section_1': section_1_coils, 'section_2': section_2_coils, 'section_3': section_3_coils}

    # Take the magnet coil parameters and generate an estimated number of turns/ number of layers styled magnet
    # This isn't strictly necessary and will have a small impact on the field on axis, but its doable
    # Also an estimate based on coil geometry information I have available, not exact
    section_1_coil_geometry = CoilGeometry(section_1_coils)
    section_2_coil_geometry = CoilGeometry(section_2_coils)
    section_3_coil_geometry = CoilGeometry(section_3_coils)

    # Compute the field of each magnet coil
    section_1_fields = MagnetSolve(section_1_coil_geometry.magnet_settings, coordinate_system)
    section_2_fields = MagnetSolve(section_2_coil_geometry.magnet_settings, coordinate_system)
    section_3_fields = MagnetSolve(section_3_coil_geometry.magnet_settings, coordinate_system)

    # Sum up the fields from each section
    total_field = {'Br': section_1_fields.magnet_fields['total']['Br'] + section_2_fields.magnet_fields['total']['Br'] +
                         section_3_fields.magnet_fields['total']['Br'],
                   'Bz': section_1_fields.magnet_fields['total']['Bz'] + section_2_fields.magnet_fields['total']['Bz'] +
                         section_3_fields.magnet_fields['total']['Bz']}

    # Some plotting
    f, a = plt.subplots(1, 1)

    im = a.imshow(total_field['Bz'].T, origin='lower', aspect='auto',
                  extent=[np.min(z_space), np.max(z_space), np.min(r_space), np.max(r_space)])
    f.colorbar(im)
    plt.show()

    f, a = plt.subplots(1, 1)

    a.plot(z_space, total_field['Bz'][:, 0] * 1e4, label=r'$r={}$'.format(r_space[0]))
    a.plot(z_space, total_field['Bz'][:, 250] * 1e4, label=r'$r={}$'.format(r_space[250]))
    a.plot(z_space, total_field['Bz'][:, 400] * 1e4, label=r'$r={}$'.format(r_space[400]))

    a.legend()
    plt.show()

    f, a = plt.subplots(1, 1)

    a.plot(z_space, total_field['Bz'][:, 0] * 1e4, label=r'$r={}$'.format(r_space[0]))

    a.set_title("Axial Field Profile")
    a.set_xlabel('$z$ [m]')
    a.set_ylabel(r"$B_z$ [G]")
    a.text(0.6, 70, r'$I=10 \; A$', size=20)
    a.legend()

    f.savefig('estimated_axial_field_profile.png')
    f.savefig('estimated_axial_field_profile.pdf')
    plt.show()
