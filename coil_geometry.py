import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class CoilGeometry:
    def __init__(self, magnet_settings):

        self.input_settings = magnet_settings
        self.magnet_settings = {}
        for magnet, settings in magnet_settings.items():
            self.magnet_settings[magnet] = self._compute_coil_geometry(settings)

        pass

    def _compute_coil_geometry(self, coil_settings):
        num_depth = int(np.ceil(np.sqrt(coil_settings['n_turns'] * (coil_settings['depth'] / coil_settings['width']))))
        num_width = int(np.ceil(np.sqrt(coil_settings['n_turns'] * (coil_settings['width'] / coil_settings['depth']))))

        sub_width = coil_settings['width'] / (num_width + 2)
        sub_depth = coil_settings['depth'] / (num_depth + 2)

        sub_coil_settings_list = []
        for i in range(num_width):
            for j in range(num_depth):
                sub_coil = {}
                coil_position = (coil_settings['position'][0] - coil_settings['width'] / 2 + i * sub_width,
                                 coil_settings['position'][1] - coil_settings['depth'] / 2 + j * sub_depth)
                sub_coil['position'] = coil_position
                sub_coil['current'] = coil_settings['current']
                sub_coil_settings_list.append(sub_coil)
        return sub_coil_settings_list

    def plot_coils(self, f, a):
        for magnet, setting in self.input_settings.items():
            rect = patches.Rectangle((setting['position'][0] - setting['width']/2,setting['position'][1] - setting['depth']/2),
                        setting['width'], setting['depth'], linewidth=1, edgecolor='r', facecolor='r')

            # Add the patch to the Axes
            a.add_patch(rect)
            #a.Rectangle((setting['position'][0] - setting['width']/2,setting['position'][1] - setting['depth']/2),
             #           setting['depth'], setting['width'], color='r')

        return f, a



if __name__ == "__main__":
    I_1 = 1
    section_1_coils = {
        'M1_1': {'current': I_1, 'position': (0.0, 0.355), 'width': 0.05715, 'depth': 0.0889, 'n_turns': 191},
    }

    section_1_coil_geometry = CoilGeometry(section_1_coils)

    print(len(section_1_coil_geometry.magnet_settings['M1_1']))

    r_list = [values['position'][1] for values in section_1_coil_geometry.magnet_settings['M1_1']]
    z_list = [values['position'][0] for values in section_1_coil_geometry.magnet_settings['M1_1']]

    f, a = plt.subplots(1, 1)

    a.scatter([section_1_coils['M1_1']['position'][0]], [section_1_coils['M1_1']['position'][1]], color='k')
    a.scatter(z_list, r_list)
    plt.show()
