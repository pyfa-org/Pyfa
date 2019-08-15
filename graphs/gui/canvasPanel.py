# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================


import itertools
import os
import traceback


# noinspection PyPackageRequirements
import wx
from logbook import Logger


from graphs.style import BASE_COLORS, LIGHTNESSES, STYLES, hsl_to_hsv


pyfalog = Logger(__name__)


try:
    import matplotlib as mpl

    mpl_version = int(mpl.__version__[0]) or -1
    if mpl_version >= 2:
        mpl.use('wxagg')
        graphFrame_enabled = True
    else:
        graphFrame_enabled = False

    from matplotlib.lines import Line2D
    from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
    from matplotlib.figure import Figure
    from matplotlib.colors import hsv_to_rgb
except ImportError as e:
    pyfalog.warning('Matplotlib failed to import.  Likely missing or incompatible version.')
    graphFrame_enabled = False
except Exception:
    # We can get exceptions deep within matplotlib. Catch those.  See GH #1046
    tb = traceback.format_exc()
    pyfalog.critical('Exception when importing Matplotlib. Continuing without importing.')
    pyfalog.critical(tb)
    graphFrame_enabled = False


class GraphCanvasPanel(wx.Panel):

    def __init__(self, graphFrame, parent):
        super().__init__(parent)
        self.graphFrame = graphFrame

        # Remove matplotlib font cache, see #234
        try:
            cache_dir = mpl._get_cachedir()
        except:
            cache_dir = os.path.expanduser(os.path.join('~', '.matplotlib'))
        cache_file = os.path.join(cache_dir, 'fontList.cache')
        if os.access(cache_dir, os.W_OK | os.X_OK) and os.path.isfile(cache_file):
            os.remove(cache_file)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.figure = Figure(figsize=(5, 3), tight_layout={'pad': 1.08})
        rgbtuple = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE).Get()
        clr = [c / 255. for c in rgbtuple]
        self.figure.set_facecolor(clr)
        self.figure.set_edgecolor(clr)
        self.canvas = Canvas(self, -1, self.figure)
        self.canvas.SetBackgroundColour(wx.Colour(*rgbtuple))
        self.subplot = self.figure.add_subplot(111)
        self.subplot.grid(True)
        mainSizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(mainSizer)

    def draw(self):
        self.subplot.clear()
        self.subplot.grid(True)
        lineData = []

        min_y = 0 if self.graphFrame.ctrlPanel.showY0 else None
        max_y = 0 if self.graphFrame.ctrlPanel.showY0 else None

        chosenX = self.graphFrame.ctrlPanel.xType
        chosenY = self.graphFrame.ctrlPanel.yType
        self.subplot.set(xlabel=self.graphFrame.ctrlPanel.formatLabel(chosenX), ylabel=self.graphFrame.ctrlPanel.formatLabel(chosenY))

        mainInput, miscInputs = self.graphFrame.ctrlPanel.getValues()
        view = self.graphFrame.getView()
        sources = self.graphFrame.ctrlPanel.sources
        if view.hasTargets:
            iterList = tuple(itertools.product(sources, self.graphFrame.ctrlPanel.targets))
        else:
            iterList = tuple((f, None) for f in sources)
        for source, target in iterList:
            # Get line style data
            try:
                colorData = BASE_COLORS[source.colorID]
            except KeyError:
                pyfalog.warning('Invalid color "{}" for "{}"'.format(source.colorID, source.name))
                continue
            color = colorData.hsl
            lineStyle = 'solid'
            if target is not None:
                try:
                    lightnessData = LIGHTNESSES[target.lightnessID]
                except KeyError:
                    pyfalog.warning('Invalid lightness "{}" for "{}"'.format(target.lightnessID, target.name))
                    continue
                color = lightnessData.func(color)
                try:
                    lineStyleData = STYLES[target.lineStyleID]
                except KeyError:
                    pyfalog.warning('Invalid line style "{}" for "{}"'.format(target.lightnessID, target.name))
                    continue
                lineStyle = lineStyleData.mplSpec
            color = hsv_to_rgb(hsl_to_hsv(color))

            # Get point data
            try:
                xs, ys = view.getPlotPoints(
                    mainInput=mainInput,
                    miscInputs=miscInputs,
                    xSpec=chosenX,
                    ySpec=chosenY,
                    src=source,
                    tgt=target)

                # Figure out min and max Y
                min_y_this = min(ys, default=None)
                if min_y is None:
                    min_y = min_y_this
                elif min_y_this is not None:
                    min_y = min(min_y, min_y_this)
                max_y_this = max(ys, default=None)
                if max_y is None:
                    max_y = max_y_this
                elif max_y_this is not None:
                    max_y = max(max_y, max_y_this)

                # If we have single data point, show marker - otherwise line won't be shown
                if len(xs) == 1 and len(ys) == 1:
                    self.subplot.plot(xs, ys, color=color, linestyle=lineStyle, marker='.')
                else:
                    self.subplot.plot(xs, ys, color=color, linestyle=lineStyle)

                if target is None:
                    lineData.append((color, lineStyle, source.shortName))
                else:
                    lineData.append((color, lineStyle, '{} vs {}'.format(source.shortName, target.shortName)))
            except Exception as ex:
                pyfalog.warning('Invalid values in "{0}"', source.name)
                self.canvas.draw()
                self.Refresh()
                return

        # Special case for when we do not show Y = 0 and have no fits
        if min_y is None:
            min_y = 0
        if max_y is None:
            max_y = 0
        # Extend range a little for some visual space
        y_range = max_y - min_y
        min_y -= y_range * 0.05
        max_y += y_range * 0.05
        if min_y == max_y:
            min_y -= min_y * 0.05
            max_y += min_y * 0.05
        if min_y == max_y:
            min_y -= 5
            max_y += 5
        self.subplot.set_ylim(bottom=min_y, top=max_y)

        legendLines = []
        for i, iData in enumerate(lineData):
            color, lineStyle, label = iData
            legendLines.append(Line2D([0], [0], color=color, linestyle=lineStyle, label=label.replace('$', '\$')))

        if len(legendLines) > 0 and self.graphFrame.ctrlPanel.showLegend:
            legend = self.subplot.legend(handles=legendLines)
            for t in legend.get_texts():
                t.set_fontsize('small')
            for l in legend.get_lines():
                l.set_linewidth(1)

        self.canvas.draw()
        self.Refresh()
