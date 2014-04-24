#
#    Copyright (c) 2013-2014 Evgeny Safronov <division494@gmail.com>
#    Copyright (c) 2011-2014 Other contributors as noted in the AUTHORS file.
#
#    This file is part of Cocaine.
#
#    Cocaine is free software; you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    Cocaine is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import io
import math
import os
import subprocess
import logging
log = logging.getLogger("cocagram")

import Image


__author__ = 'Evgeny Safronov <division494@gmail.com>'


IMAGEMAGICK_PATH = '/usr/bin/convert'


class Filter(object):
    def __init__(self, im=IMAGEMAGICK_PATH, fmt='jpg'):
        self._im = im
        self._fmt = fmt

    def _exec(self, command, stdin, **kwargs):
        im = Image.open(io.BytesIO(stdin))
        options = dict(
            program=self._im,
            width=im.size[0],
            height=im.size[1],
            format=self._fmt
        )
        fmt = dict(options.items() + kwargs.items())

        command = command.format(**fmt)
        log.info(command)
        p = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        stdout, stderr = p.communicate(input=stdin)
        if len(stdout) == 0:
            raise ValueError('output image is empty')
        return stdout

    def _apply(self, data, stages):
        for stage in stages:
            data = self._exec(stage.format(self._im), data)
        return data

    def _border(self, data, color='black', width=20):
        return self._exec(
            "{program} :- "
            "-bordercolor {color} -border {bwidth}x{bwidth} "
            "{format}:-", data, color=color, bwidth=width)

    def _colortone(self, data, color, level, negate=True):
        if negate:
            negate = '-negate'
        else:
            negate = ''

        return self._exec(
            "{program} :- "
            "\( -clone 0 -fill '{color}' -colorize 100% \) "
            "\( -clone 0 -colorspace gray {negate} \) "
            "-compose blend -define compose:args={args} "
            "-composite {format}:-",
            data, color=color, negate=negate,
            args=','.join(map(str, [level, 100 - level])))

    def _frame(self, data, filename):
        im = Image.open(io.BytesIO(data))
        path = os.path.abspath(os.path.join('frames', filename))
        return self._exec(
            "{program} :- "
            "\( '{frame}' -resize {width}x{width}! -unsharp 1.5x1.0+1.5+0.02 \) "
            "-flatten {format}:-".format(**dict(
                program=self._im,
                frame=path,
                width=im.size[0],
                format=self._fmt
            )), data)

    def _vignette(self, data, color1='none', color2='black', crop_factor=1.5):
        im = Image.open(io.BytesIO(data))
        crop_x = math.floor(im.size[0] * crop_factor)
        crop_y = math.floor(im.size[1] * crop_factor)
        return self._exec(
            "{program} \( :- \) "
            "\( -size {crop_x}x{crop_y} radial-gradient:{color1}-{color2} "
            "-gravity center -crop {width}x{height}+0+0 +repage \) "
            "-compose multiply -flatten "
            "{format}:-", data, crop_x=crop_x, crop_y=crop_y,
            color1=color1, color2=color2)


class NashvilleFilter(Filter):
    def apply(self, data):
        data = self._colortone(data, '#330000', 50)
        data = self._colortone(data, '#f7daae', 120, False)
        data = self._exec(
            "{program} :- "
            "-contrast -modulate 100,150,100 -auto-gamma "
            "{format}:-", data)
        data = self._frame(data, 'nashville.jpg')
        return data


class GothamFilter(Filter):
    def apply(self, data):
        data = self._exec(
            "{program} :- "
            "-modulate 120,10,100 -fill '#222b6d' -colorize 20 -gamma 0.5 -contrast -contrast "
            "{format}:-", data)
        data = self._border(data)
        return data


class ToasterFilter(Filter):
    def apply(self, data):
        data = self._colortone(data, '#330000', 50)
        data = self._exec(
            "{program} :- "
            "-modulate 150,80,100 -gamma 1.2 -contrast -contrast "
            "{format}:-", data)
        data = self._vignette(data, 'none', 'LavenderBlush3')
        data = self._vignette(data, '#ff9966', 'none')
        data = self._border(data, 'white')
        return data


class LomoFilter(Filter):
    def apply(self, data):
        data = self._exec(
            "{program} :- "
            "-channel R -level 33% -channel G -level 33% "
            "{format}:-", data)
        data = self._vignette(data)
        return data


class KelvinFilter(Filter):
    def apply(self, data):
        data = self._exec(
            "{program} \( :- -auto-gamma -modulate 120,50,100 \) "
            "\( -size {width}x{height} -fill 'rgba(255,153,0,0.5)' "
            "-draw 'rectangle 0,0 {width},{height}' \) -compose multiply "
            "{format}:-", data)
        data = self._frame(data, "kelvin.jpg")
        return data


# path = os.path.abspath('test.jpg')

# content = ''
# try:
#     with open(path) as fh:
#         content = fh.read()
#         if len(content) == 0:
#             raise ValueError('file content is empty')
# except Exception as err:
#     print(err)

# data = KelvinFilter().apply(content)

# with open('out.jpg', 'w') as fh:
#     fh.write(data)
