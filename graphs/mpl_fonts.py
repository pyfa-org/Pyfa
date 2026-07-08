# =============================================================================
# Copyright (C) 2026 Du Yifeng
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
"""
Configures Matplotlib font fallback stack to include available system CJK fonts.
This ensures Chinese, Japanese, and Korean characters render correctly in graphs.
"""

import platform


def configure_matplotlib_font():
    """
    Configure matplotlib to use fonts that can render CJK text.
    """
    try:
        import matplotlib as mpl
        from matplotlib import font_manager
    except ImportError:
        return

    candidates = []

    try:
        # noinspection PyPackageRequirements
        import wx
        gui_face = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT).GetFaceName()
        if gui_face:
            candidates.append(gui_face)
    except Exception:
        pass

    candidates.extend([
        'Noto Sans CJK KR', 'Noto Sans CJK JP', 'Noto Sans CJK SC', 'Noto Sans CJK TC',
        'Source Han Sans KR', 'Source Han Sans JP', 'Source Han Sans CN', 'Source Han Sans TW',
    ])

    system = platform.system()
    if system == 'Windows':
        candidates.extend([
            'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', 'SimSun',
            'Malgun Gothic', 'Gulim', 'Dotum', 'Batang',
            'Yu Gothic', 'Meiryo', 'Arial Unicode MS',
        ])
    elif system == 'Darwin':
        candidates.extend([
            'Apple SD Gothic Neo', 'AppleGothic', 'PingFang SC', 'PingFang TC',
            'Hiragino Sans GB', 'Hiragino Sans', 'Heiti SC', 'Arial Unicode MS',
        ])
    else:
        candidates.extend([
            'NanumGothic', 'UnDotum', 'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei',
            'Droid Sans Fallback',
        ])

    candidates.append('DejaVu Sans')

    # Filter out unavailable fonts to prevent Matplotlib warnings
    available = {f.name for f in font_manager.fontManager.ttflist}
    
    resolved = []
    for name in candidates:
        if name in available and name not in resolved:
            resolved.append(name)

    if resolved:
        mpl.rcParams['font.family'] = resolved

    mpl.rcParams['axes.unicode_minus'] = False
