import numpy as np


def rungeKuttaBound(dydx, x0, y0, x_bound_low, x_bound_high, y_bound, h):
    y = y0

    y_list = [y0]
    x_list = [x0]

    while x_bound_low < x0 < x_bound_high and y < y_bound:
        "Apply Runge Kutta Formulas to find next value of y"
        k1 = h * dydx(x0, y)
        k2 = h * dydx(x0 + 0.5 * h, y + 0.5 * k1)
        k3 = h * dydx(x0 + 0.5 * h, y + 0.5 * k2)
        k4 = h * dydx(x0 + h, y + k3)

        # Update next value of y
        y = y + (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

        # Update next value of x
        x0 = x0 + h

        y_list.append(y)
        x_list.append(x0)

    return np.array(x_list), np.array(y_list)


class FieldLines:
    def __init__(self, fields):
        self.field_dict = fields
        self.Br = fields['Br']
        self.Bz = fields['Bz']

        pass

    def solveFieldLines(self):
        """
        Basic idea is to solve the field lines

        :return:
        """

        pass