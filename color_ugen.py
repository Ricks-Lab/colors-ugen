#!/usr/bin/env python3
""" color-ugen  -  ColorGen Classs

    Copyright (C) 2019  RueiKe

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
__author__ = 'RueiKe'
__copyright__ = 'Copyright (C) 2020 RueiKe'
__credits__ = []
__license__ = 'GNU General Public License'
__program_name__ = 'color-pal'
__version__ = 'v0.0.1'
__maintainer__ = 'RueiKe'
__status__ = 'Development'
__docformat__ = 'reStructuredText'
# pylint: disable=multiple-statements
# pylint: disable=line-too-long

import colorsys


class ColorGen:
    def __init__(self):
        self.colors = {}
        self.counter = 0

    def add_hsv(self, hsv_val, quiet=True):
        rgb_tup = colorsys.hsv_to_rgb(*hsv_val)
        if rgb_tup[0] < 0 or rgb_tup[1] < 0 or rgb_tup[2] < 0:
            print('RGB error: {}'.format(rgb_tup))
            return
        hex_rgb = '#{:02x}{:02x}{:02x}'.format(int(rgb_tup[0]*255), int(rgb_tup[1]*255), int(rgb_tup[2]*255))
        if not quiet:
            print('rgb: {}, hsv: ({:.2f}, {:.2f}, {:.2f})'.format(hex_rgb, *hsv_val))
        self.colors.update({hex_rgb: hsv_val})
        self.counter += 1
        return

    def color_gen_list(self, num_cols):
        #h_params = (0, 360, 15)  # min, max, num_steps
        #s_params = (30, 100, 2)
        #v_params = (50, 100, 3)
        h_params = (0, 360, 15)  # min, max, num_steps
        s_params = (50, 90, 2)
        v_params = (60, 100, 3)
        total_sv_steps = s_params[2] * v_params[2]

        start_hue = h_params[0]
        v_step = int((v_params[1] - v_params[0]) / v_params[2])
        for t_val in range(v_params[1], v_params[0], -v_step):
            hsv_val = t_val / v_params[1]
            s_step = int((t_val - s_params[0]) / s_params[2])
            print('v_step: {}, s_step: {}'.format(v_step, s_step))
            for t_sat in range(t_val, s_params[0], -s_step):
                hsv_sat = t_sat / s_params[1]
                h_step = int((h_params[1] - h_params[0]) / h_params[2])
                for t_hue in range(start_hue, h_params[1], h_step):
                    hsv_hue = float(t_hue) / 360.0
                    self.add_hsv(tuple([hsv_hue, hsv_sat, hsv_val]))
                start_hue += int(h_step / total_sv_steps)
                print('start_hue: {}'.format(start_hue))
        return list(self.colors.keys())

    def print(self):
        print('Added hsv: {}, Resultant rgb: {}'.format(self.counter, len(self.colors)))
        for rgb, hsv in self.colors.items():
            print('rgb: {}, hsv: ({:.2f}, {:.2f}, {:.2f})'.format(rgb, *hsv))
