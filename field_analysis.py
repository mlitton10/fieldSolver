import numpy as np
from scipy.interpolate import interp2d


def rungeKuttaBound(dydx, x0, y0, x_bound_low, x_bound_high, y_bound, h):
    y = y0

    y_list = [y0]
    x_list = [x0]

    while x_bound_low <= x0 <= x_bound_high and y <= y_bound:
        "Apply Runge Kutta Formulas to find next value of y"
        k1 = h * dydx(x0, y)[0]
        k2 = h * dydx(x0 + 0.5 * h, y + 0.5 * k1)[0]
        k3 = h * dydx(x0 + 0.5 * h, y + 0.5 * k2)[0]
        k4 = h * dydx(x0 + h, y + k3)[0]

        # Update next value of y
        y = y + (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        # Update next value of x
        x0 = x0 + h

        y_list.append(y)
        x_list.append(x0)

    return np.array(x_list), np.array(y_list)


class FieldLines:
    def __init__(self, fields, coordinate_system, n_field_lines, r_wall=0.2, stepsize=0.01):
        self.field_dict = fields
        self.Br = fields['Br']
        self.Bz = fields['Bz']
        print(self.Bz.shape)
        self.coordinate_system = coordinate_system
        self.r_wall = r_wall

        field_ratio = self.Br / self.Bz

        self.ratio_interpolation = interp2d(*coordinate_system, field_ratio.T)
        self.n_field_lines = n_field_lines

        self.spatial_bounds = self._find_spatial_bounds()
        self.initial_conditions = self._pick_initial_points()
        self.stepsize= stepsize

        pass

    def _find_spatial_bounds(self):
        r_bounds = [np.min(self.coordinate_system[1]), np.max(self.coordinate_system[1])]
        z_bounds = [np.min(self.coordinate_system[0]), np.max(self.coordinate_system[0])]

        return [z_bounds, r_bounds]

    def _pick_initial_points(self):
        z_initial = self.spatial_bounds[0][0]
        r_initial = np.linspace(0, self.r_wall, self.n_field_lines)

        return np.array([(z_initial+0.001, r) for r in r_initial])

    def solveFieldLines(self):
        solutions_set = []

        for ic in self.initial_conditions:
            z_sol, r_sol = rungeKuttaBound(self.ratio_interpolation, ic[0], ic[1], self.spatial_bounds[0][0],
                                           self.spatial_bounds[0][1], self.spatial_bounds[1][1], self.stepsize)

            solutions_set.append((z_sol, r_sol))
        return solutions_set
