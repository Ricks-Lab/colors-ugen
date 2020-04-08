#!/usr/bin/env python3
""" color-ugen  -  ColorUgen Class

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
import math


class ColorUgen:
    def __init__(self):
        self.colors = {}
        self.counter = 0

    def add_rgb(self, add_val, color_space='hsv', quiet=True):
        if color_space == 'yiq':
            rgb_tup = colorsys.yiq_to_rgb(*add_val)
        else:
            rgb_tup = colorsys.hsv_to_rgb(*add_val)
        if rgb_tup[0] < 0 or rgb_tup[1] < 0 or rgb_tup[2] < 0:
            print('RGB error: {}'.format(rgb_tup))
            return
        hex_rgb = '#{:02x}{:02x}{:02x}'.format(int(rgb_tup[0]*255), int(rgb_tup[1]*255), int(rgb_tup[2]*255))
        if not quiet:
            print('rgb: {}, hsv: ({:.2f}, {:.2f}, {:.2f})'.format(hex_rgb, *add_val))
        self.colors.update({hex_rgb: add_val})
        self.counter += 1
        return

    def color_gen_list(self, num_cols, color_space='hsv', debug=False):
        if color_space == 'yiq':
            #return self.color_gen_list_from_yiq(num_cols, debug)[:num_cols]
            return self.color_gen_list_from_yiq(num_cols, debug)
        else:
            #return self.color_gen_list_from_hsv(num_cols, debug)[:num_cols]
            return self.color_gen_list_from_hsv(num_cols, debug)

    def color_gen_list_from_yiq(self, num_cols, debug=False):

        # Calculate optimal number of steps for num_cols distinct colors
        num_iqx = 7
        num_iqy = 7
        num_y = int(num_cols / (num_iqx * num_iqy))
        if debug: print('loops: y={}, iqx={}, iqy={}'.format(num_y, num_iqx, num_iqy))

        # Calculate range parameters, start, stop, index.  Subtract from hue stop, to allow drifting start
        y_params = (10, 90, num_y)  # min, max, num_steps
        iqx_params = (-100, 100, num_iqx)
        iqy_params = (-100, 100, num_iqy)
        if debug: print('params: y={}, iqx={}, iqy={}'.format(y_params, iqx_params, iqy_params))

        # Set parameters for jittering iqx and iqy values between y steps.

        # Set step sizes, always round up
        y_step = int(((y_params[1] - y_params[0]) / y_params[2]) // 1) + 1
        iqx_step = int(((iqx_params[1] - iqx_params[0]) / iqx_params[2]) // 1) + 1
        iqy_step = int(((iqy_params[1] - iqy_params[0]) / iqy_params[2]) // 1) + 1
        if debug: print('y_step: {}, iqx_step: {}, iqy_step: {}'.format(y_step, iqx_step, iqy_step))

        # This doesn't work, as the color cube is rotated -33deg about the y axis and scaled.
        # https://hbfs.wordpress.com/2018/05/08/yuv-and-yiq-colorspaces-v/
        # Step from brightest to darkest
        for t_y in range(y_params[1], y_params[0], -y_step):
            yiq_y = t_y / 100

            # Step from lowest to highest iqx
            for t_iqx in range(iqx_params[0], iqx_params[1], iqx_step):
                yiq_iqx = t_iqx / 100

                # Step from lowest to highest iqy
                for t_iqy in range(iqy_params[0], iqy_params[1], iqy_step):
                    yiq_iqy = t_iqy / 100
                    self.add_rgb(tuple([yiq_y, yiq_iqx, yiq_iqy]), color_space='yiq')

        return list(self.colors.keys())

    def color_gen_list_from_hsv(self, num_cols, debug=False):

        # Calculate optimal number of steps for num_cols distinct colors
        num_hues = 14
        num_sats = int((math.sqrt(num_cols/num_hues)) // 1) + 1
        num_vals = int((num_cols / (num_hues + num_sats)) // 1) - 2
        if debug: print('loops: h={}, s={}, v={}'.format(num_hues, num_sats, num_vals))

        # Calculate range parameters, start, stop, index.  Subtract from hue stop, to allow drifting start
        max_hue = 360 - int(360/num_hues)
        h_params = (0, max_hue, num_hues)  # min, max, num_steps
        s_params = (60, 95, num_sats)
        v_params = (30, 90, num_vals)
        if debug: print('params: h={}, s={}, v={}'.format(h_params, s_params, v_params))

        # Set parameters for drifting hue
        total_sv_steps = s_params[2] * v_params[2]
        start_hue = h_params[0]

        # Set step sizes, always round up
        v_step = int(((v_params[1] - v_params[0]) / v_params[2]) // 1) + 1
        s_step = int(((s_params[1] - s_params[0]) / s_params[2]) // 1) + 1
        h_step = int(((h_params[1] - h_params[0]) / h_params[2]) // 1) + 1
        if debug: print('h_step: {}, v_step: {}, s_step: {}'.format(h_step, v_step, s_step))

        # Step from brightest to darkest
        for t_val in range(v_params[1], v_params[0], -v_step):
            hsv_val = t_val / 100

            # Step from highest saturation to lowest
            for t_sat in range(s_params[1], s_params[0], -s_step):
                hsv_sat = t_sat / 100

                # Step from red to one step before red again
                for t_hue in range(h_params[0] + start_hue, h_params[1] + start_hue, h_step):
                    # Green correct
                    if 80 < t_hue < 130: continue
                    if hsv_val > 0.90: m_hsv_val = hsv_val * 0.85 if 85 < t_hue < 140 else hsv_val
                    else: m_hsv_val = hsv_val
                    hsv_hue = float(t_hue) / 360.0
                    self.add_rgb(tuple([hsv_hue, hsv_sat, m_hsv_val]), color_space='hsv')
                start_hue += int(h_step / total_sv_steps)
                if debug: print('start_hue: {}'.format(start_hue))
        return list(self.colors.keys())

    def print(self):
        print('Added hsv: {}, Resultant rgb: {}'.format(self.counter, len(self.colors)))
        for rgb, hsv in self.colors.items():
            print('rgb: {}, hsv: ({:.2f}, {:.2f}, {:.2f})'.format(rgb, *hsv))
