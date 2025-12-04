import numpy as np
from scipy.special import ellipk, ellipe
import matplotlib.pyplot as plt
from tqdm import tqdm


# The following functions are geometric/ elliptical functions used in calculating the fields
def alpha(r, R):
    return r / R


def beta(z, R):
    return z / R


def gamma(z, r):
    return z / r


def Q(z, r, R):
    return (1 + alpha(r, R)) ** 2 + beta(z, R) ** 2


def k(z, r, R):
    return np.sqrt(4 * alpha(r, R) / Q(z, r, R))


def K(k):
    return ellipk(k ** 2)


def E(k):
    return ellipe(k ** 2)


# This class finds the field of a given electromagnet, accounting for each subwinding
class MagnetSolve:
    def __init__(self, magnet_settings, coordinates):
        self.magnet_settings = magnet_settings
        self.space = coordinates

        self.magnet_fields = {}

        B_r_total = np.zeros(self.space[1].shape)
        B_z_total = np.zeros(self.space[0].shape)

        for magnet, settings in self.magnet_settings.items():
            B_r_magnet = np.zeros(self.space[1].shape)
            B_z_magnet = np.zeros(self.space[0].shape)

            for setting in tqdm(settings):
                magnetSolver = CurrentLoopSolve(**setting, coordinates=self.space)
                B_r, B_z = magnetSolver.solve_field()
                B_r_magnet += B_r
                B_z_magnet += B_z
            self.magnet_fields[magnet] = {'Br': B_r_magnet, 'Bz': B_z_magnet}
            B_r_total += B_r_magnet
            B_z_total += B_z_magnet
        self.magnet_fields['total'] = {'Br': B_r_total, 'Bz': B_z_total}


# This calculates the field of a single current loop in space
class CurrentLoopSolve:
    def __init__(self, current=1,
                 coordinates=None,
                 position=(0, 0.5)):

        self.R = position[1]
        self.Z = position[0]
        self.I = current
        self.space = coordinates  # (r,z)

        pass

    def solve_field(self):
        m_0 = 4 * np.pi * 1e-7
        B_0 = self.I * m_0 / (2 * self.R)

        def Baxial(R, z):
            if R == 0:
                if z == 0:
                    return np.nan
                else:
                    return 0.0
            else:
                return (m_0 * self.I * R ** 2) / 2.0 / (R ** 2 + z ** 2) ** 1.5

        # Axial field component = f(current and radius of loop, r and x of meas. point)
        def Bz(R, z, r):
            zero_mask = (r == 0)

            B_nonzero = B_0 * \
                        (E(k(z, r, R)) * (
                                (1.0 - alpha(r, R) ** 2 - beta(z, R) ** 2) / (
                                Q(z, r, R) - 4 * alpha(r, R))) + K(
                            k(z, r, R))) \
                        / np.pi / np.sqrt(Q(z, r, R))

            B = B_nonzero.copy()

            np.putmask(B, zero_mask, Baxial(R, z))

            return B

        # Radial field component = f(current and radius of loop, r and x of meas. point)
        def Br(R, z, r):
            zero_mask = (r == 0)

            B_nonzero = B_0 * gamma(z, r) * \
                        (E(k(z, r, R)) * (
                                (1.0 + alpha(r, R) ** 2 + beta(z, R) ** 2) / (
                                Q(z, r, R) - 4 * alpha(r, R))) - K(
                            k(z, r, R))) \
                        / np.pi / np.sqrt(Q(z, r, R))

            B = B_nonzero.copy()

            np.putmask(B, zero_mask, 0.0)

            return B

        B_r = Br(self.R, self.space[0] - self.R, self.space[1])
        B_z = Bz(self.R, self.space[0] - self.Z, self.space[1])

        return B_r, B_z


if __name__ == "__main__":
    r_space = np.linspace(0, 0.3, 500)
    z_space = np.linspace(0, 2, 1000)
    # theta_space = np.linspace(0, 2 * np.pi, 100)

    R, Z = np.meshgrid(r_space, z_space)
    coordinate_system = [Z, R]

    coils = {'M1': {'current': 10 * 191, 'coordinates': coordinate_system, 'position': (1, 0.35)}}

    B_r_total = np.zeros(R.shape)
    B_z_total = np.zeros(Z.shape)

    for magnet, magnet_settings in coils.items():
        magnetSolver = CurrentLoopSolve(**magnet_settings)
        B_r, B_z = magnetSolver.solve_field()
        B_r_total += B_r
        B_z_total += B_z

    f, a = plt.subplots(1, 1)

    a.imshow(B_z_total.T, origin='lower', aspect='auto',
             extent=[np.min(z_space), np.max(z_space), np.min(r_space), np.max(r_space)])

    f, a = plt.subplots(1, 1)

    a.plot(z_space, B_z_total[:, 0] * 1e4, label=r'$r={}$'.format(r_space[0]))

    a.set_title("Axial Field Profile")
    a.set_xlabel('$z$ [m]')
    a.set_ylabel(r"$B_z$ [G]")
    a.legend()
    plt.show()

    plt.show()
