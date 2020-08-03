# ===============================================================================
# Copyright (C) 2014 Ryan Holmes
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
# ===============================================================================

import math
import re
from collections import OrderedDict

from logbook import Logger
from sqlalchemy.orm import reconstructor

import eos.db

pyfalog = Logger(__name__)


def _t(x):
    return x


def _c(x):
    return '[' + x + ']'


BUILTINS = OrderedDict([
    # 0 is taken by ideal target profile, composed manually in one of TargetProfile methods
    (-1, (_t('Uniform (25%)'), 0.25, 0.25, 0.25, 0.25)),
    (-2, (_t('Uniform (50%)'), 0.50, 0.50, 0.50, 0.50)),
    (-3, (_t('Uniform (75%)'), 0.75, 0.75, 0.75, 0.75)),
    (-4, (_t('Uniform (90%)'), 0.90, 0.90, 0.90, 0.90)),
    (-5, (_c(_t('T1 Resist')) + _t('Shield'), 0.0, 0.20, 0.40, 0.50)),
    (-6, (_c(_t('T1 Resist')) + _t('Armor'), 0.50, 0.45, 0.25, 0.10)),
    (-7, (_c(_t('T1 Resist')) + _t('Hull'), 0.33, 0.33, 0.33, 0.33)),
    (-8, (_c(_t('T1 Resist')) + _t('Shield (+T2 DCU)'), 0.125, 0.30, 0.475, 0.562)),
    (-9, (_c(_t('T1 Resist')) + _t('Armor (+T2 DCU)'), 0.575, 0.532, 0.363, 0.235)),
    (-10, (_c(_t('T1 Resist')) + _t('Hull (+T2 DCU)'), 0.598, 0.598, 0.598, 0.598)),
    (-11, (_c(_t('T2 Resist')) + _t('Amarr (Shield)'), 0.0, 0.20, 0.70, 0.875)),
    (-12, (_c(_t('T2 Resist')) + _t('Amarr (Armor)'), 0.50, 0.35, 0.625, 0.80)),
    (-13, (_c(_t('T2 Resist')) + _t('Caldari (Shield)'), 0.20, 0.84, 0.76, 0.60)),
    (-14, (_c(_t('T2 Resist')) + _t('Caldari (Armor)'), 0.50, 0.8625, 0.625, 0.10)),
    (-15, (_c(_t('T2 Resist')) + _t('Gallente (Shield)'), 0.0, 0.60, 0.85, 0.50)),
    (-16, (_c(_t('T2 Resist')) + _t('Gallente (Armor)'), 0.50, 0.675, 0.8375, 0.10)),
    (-17, (_c(_t('T2 Resist')) + _t('Minmatar (Shield)'), 0.75, 0.60, 0.40, 0.50)),
    (-18, (_c(_t('T2 Resist')) + _t('Minmatar (Armor)'), 0.90, 0.675, 0.25, 0.10)),
    (-19, (_c(_t('NPC')) + _c(_t('Asteroid')) + _t('Angel Cartel'), 0.54, 0.42, 0.37, 0.32)),
    (-20, (_c(_t('NPC')) + _c(_t('Asteroid')) + _t('Blood Raiders'), 0.34, 0.39, 0.45, 0.52)),
    (-21, (_c(_t('NPC')) + _c(_t('Asteroid')) + _t('Guristas'), 0.55, 0.35, 0.3, 0.48)),
    (-22, (_c(_t('NPC')) + _c(_t('Asteroid')) + _t('Rogue Drones'), 0.35, 0.38, 0.44, 0.49)),
    (-23, (_c(_t('NPC')) + _c(_t('Asteroid')) + _t('Sanshas Nation'), 0.35, 0.4, 0.47, 0.53)),
    (-24, (_c(_t('NPC')) + _c(_t('Asteroid')) + _t('Serpentis'), 0.49, 0.38, 0.29, 0.51)),
    (-25, (_c(_t('NPC')) + _c(_t('Deadspace')) + _t('Angel Cartel'), 0.59, 0.48, 0.4, 0.32)),
    (-26, (_c(_t('NPC')) + _c(_t('Deadspace')) + _t('Blood Raiders'), 0.31, 0.39, 0.47, 0.56)),
    (-27, (_c(_t('NPC')) + _c(_t('Deadspace')) + _t('Guristas'), 0.57, 0.39, 0.31, 0.5)),
    (-28, (_c(_t('NPC')) + _c(_t('Deadspace')) + _t('Rogue Drones'), 0.42, 0.42, 0.47, 0.49)),
    (-29, (_c(_t('NPC')) + _c(_t('Deadspace')) + _t('Sanshas Nation'), 0.31, 0.39, 0.47, 0.56)),
    (-30, (_c(_t('NPC')) + _c(_t('Deadspace')) + _t('Serpentis'), 0.49, 0.38, 0.29, 0.56)),
    (-31, (_c(_t('NPC')) + _c(_t('Mission')) + _t('Amarr Empire'), 0.34, 0.38, 0.42, 0.46)),
    (-32, (_c(_t('NPC')) + _c(_t('Mission')) + _t('Caldari State'), 0.51, 0.38, 0.3, 0.51)),
    (-33, (_c(_t('NPC')) + _c(_t('Mission')) + _t('CONCORD'), 0.47, 0.46, 0.47, 0.47)),
    (-34, (_c(_t('NPC')) + _c(_t('Mission')) + _t('Gallente Federation'), 0.51, 0.38, 0.31, 0.52)),
    (-35, (_c(_t('NPC')) + _c(_t('Mission')) + _t('Khanid'), 0.51, 0.42, 0.36, 0.4)),
    (-36, (_c(_t('NPC')) + _c(_t('Mission')) + _t('Minmatar Republic'), 0.51, 0.46, 0.41, 0.35)),
    (-37, (_c(_t('NPC')) + _c(_t('Mission')) + _t('Mordus Legion'), 0.32, 0.48, 0.4, 0.62)),
    (-38, (_c(_t('NPC')) + _c(_t('Other')) + _t('Sleeper'), 0.61, 0.61, 0.61, 0.61)),
    (-39, (_c(_t('NPC')) + _c(_t('Other')) + _t('Sansha Incursion'), 0.65, 0.63, 0.64, 0.65)),
    (-40, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Cruor (Blood Raiders)'), 0.8, 0.73, 0.69, 0.67)),
    (-41, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Dramiel (Angel)'), 0.35, 0.48, 0.61, 0.68)),
    (-42, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Daredevil (Serpentis)'), 0.69, 0.59, 0.59, 0.43)),
    (-43, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Succubus (Sanshas Nation)'), 0.35, 0.48, 0.61, 0.68)),
    (-44, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Worm (Guristas)'), 0.48, 0.58, 0.69, 0.74)),
    (-45, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Enyo'), 0.58, 0.72, 0.86, 0.24)),
    (-46, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Hawk'), 0.3, 0.86, 0.79, 0.65)),
    (-47, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Jaguar'), 0.78, 0.65, 0.48, 0.56)),
    (-48, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Vengeance'), 0.66, 0.56, 0.75, 0.86)),
    (-49, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Ashimmu (Blood Raiders)'), 0.8, 0.76, 0.68, 0.7)),
    (-50, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Talos'), 0.68, 0.59, 0.59, 0.43)),
    (-51, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Sentinel'), 0.58, 0.45, 0.52, 0.66)),
    # Source: ticket #2067
    (-52, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Invading Precursor Entities'), 0.422, 0.367, 0.453, 0.411)),
    (-53, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Retaliating Amarr Entities'), 0.360, 0.310, 0.441, 0.602)),
    (-54, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Retaliating Caldari Entities'), 0.287, 0.610, 0.487, 0.401)),
    (-55, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Retaliating Gallente Entities'), 0.383, 0.414, 0.578, 0.513)),
    (-56, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Retaliating Minmatar Entities'), 0.620, 0.422, 0.355, 0.399)),
    (-57, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('Drones'), 0.439, 0.522, 0.529, 0.435)),
    (-58, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('Overmind'), 0.626, 0.576, 0.612, 0.624)),
    (-59, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('Seeker'), 0.082, 0.082, 0.082, 0.082)),
    (-60, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('Triglavian'), 0.477, 0.401, 0.449, 0.37)),
    (-61, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('Drifter'), 0.403, 0.403, 0.403, 0.403)),
    (-62, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('Sleeper'), 0.435, 0.435, 0.435, 0.435)),
    (-63, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('All'), 0.507, 0.477, 0.502, 0.493)),
    (-64, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T1/T2')) + _t('Drones'), 0.323, 0.522, 0.529, 0.435)),
    (-65, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T1/T2')) + _t('Overmind'), 0.521, 0.576, 0.612, 0.624)),
    (-66, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T1/T2')) + _t('Seeker'), 0, 0.082, 0.082, 0.082)),
    (-67, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T1/T2')) + _t('Triglavian'), 0.333, 0.401, 0.449, 0.37)),
    (-68, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T1/T2')) + _t('Drifter'), 0.267, 0.403, 0.403, 0.403)),
    (-69, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T1/T2')) + _t('Sleeper'), 0.329, 0.435, 0.435, 0.435)),
    (-70, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T1/T2')) + _t('All'), 0.385, 0.477, 0.502, 0.493)),
    (-71, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('Drones'), 0.255, 0.522, 0.529, 0.435)),
    (-72, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('Overmind'), 0.457, 0.576, 0.612, 0.624)),
    (-73, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('Seeker'), 0, 0.082, 0.082, 0.082)),
    (-74, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('Triglavian'), 0.241, 0.401, 0.449, 0.37)),
    (-75, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('Drifter'), 0.184, 0.403, 0.403, 0.403)),
    (-76, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('Sleeper'), 0.268, 0.435, 0.435, 0.435)),
    (-77, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('All'), 0.313, 0.477, 0.502, 0.493)),
    (-78, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5')) + _t('Drones'), 0.193, 0.522, 0.529, 0.435)),
    (-79, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5')) + _t('Overmind'), 0.398, 0.576, 0.612, 0.624)),
    (-80, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5')) + _t('Seeker'), 0, 0.082, 0.082, 0.082)),
    (-81, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5')) + _t('Triglavian'), 0.183, 0.401, 0.449, 0.37)),
    (-82, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5')) + _t('Drifter'), 0.107, 0.403, 0.403, 0.403)),
    (-83, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5')) + _t('Sleeper'), 0.215, 0.435, 0.435, 0.435)),
    (-84, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5')) + _t('All'), 0.25, 0.477, 0.502, 0.493)),
    (-85, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T1/T2')) + _t('Drones'), 0.461, 0.425, 0.541, 0.443)),
    (-86, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T1/T2')) + _t('Overmind'), 0.65, 0.469, 0.625, 0.633)),
    (-87, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T1/T2')) + _t('Seeker'), 0.084, 0, 0.084, 0.084)),
    (-88, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T1/T2')) + _t('Triglavian'), 0.534, 0.266, 0.484, 0.366)),
    (-89, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T1/T2')) + _t('Drifter'), 0.422, 0.282, 0.422, 0.422)),
    (-90, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T1/T2')) + _t('Sleeper'), 0.512, 0.402, 0.512, 0.512)),
    (-91, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T1/T2')) + _t('All'), 0.541, 0.365, 0.524, 0.504)),
    (-92, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('Drones'), 0.461, 0.36, 0.541, 0.443)),
    (-93, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('Overmind'), 0.65, 0.391, 0.625, 0.633)),
    (-94, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('Seeker'), 0.084, 0, 0.084, 0.084)),
    (-95, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('Triglavian'), 0.534, 0.161, 0.484, 0.366)),
    (-96, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('Drifter'), 0.422, 0.196, 0.422, 0.422)),
    (-97, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('Sleeper'), 0.512, 0.337, 0.512, 0.512)),
    (-98, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('All'), 0.541, 0.284, 0.524, 0.504)),
    (-99, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5')) + _t('Drones'), 0.461, 0.305, 0.541, 0.443)),
    (-100, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5')) + _t('Overmind'), 0.65, 0.323, 0.625, 0.633)),
    (-101, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5')) + _t('Seeker'), 0.084, 0, 0.084, 0.084)),
    (-102, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5')) + _t('Triglavian'), 0.534, 0.082, 0.484, 0.366)),
    (-103, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5')) + _t('Drifter'), 0.422, 0.114, 0.422, 0.422)),
    (-104, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5')) + _t('Sleeper'), 0.512, 0.276, 0.512, 0.512)),
    (-105, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5')) + _t('All'), 0.541, 0.214, 0.524, 0.504)),
    (-106, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T1/T2')) + _t('Drones'), 0.439, 0.522, 0.417, 0.435)),
    (-107, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T1/T2')) + _t('Overmind'), 0.626, 0.576, 0.496, 0.624)),
    (-108, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T1/T2')) + _t('Seeker'), 0.082, 0.082, 0, 0.082)),
    (-109, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T1/T2')) + _t('Triglavian'), 0.477, 0.401, 0.284, 0.37)),
    (-110, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T1/T2')) + _t('Drifter'), 0.403, 0.403, 0.267, 0.403)),
    (-111, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T1/T2')) + _t('Sleeper'), 0.435, 0.435, 0.329, 0.435)),
    (-112, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T1/T2')) + _t('All'), 0.507, 0.477, 0.373, 0.493)),
    (-113, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('Drones'), 0.439, 0.522, 0.351, 0.435)),
    (-114, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('Overmind'), 0.626, 0.576, 0.419, 0.624)),
    (-115, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('Seeker'), 0.082, 0.082, 0, 0.082)),
    (-116, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('Triglavian'), 0.477, 0.401, 0.176, 0.37)),
    (-117, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('Drifter'), 0.403, 0.403, 0.184, 0.403)),
    (-118, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('Sleeper'), 0.435, 0.435, 0.268, 0.435)),
    (-119, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('All'), 0.507, 0.477, 0.293, 0.493)),
    (-120, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5')) + _t('Drones'), 0.439, 0.522, 0.293, 0.435)),
    (-121, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5')) + _t('Overmind'), 0.626, 0.576, 0.344, 0.624)),
    (-122, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5')) + _t('Seeker'), 0.082, 0.082, 0, 0.082)),
    (-123, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5')) + _t('Triglavian'), 0.477, 0.401, 0.107, 0.37)),
    (-124, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5')) + _t('Drifter'), 0.403, 0.403, 0.107, 0.403)),
    (-125, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5')) + _t('Sleeper'), 0.435, 0.435, 0.215, 0.435)),
    (-126, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5')) + _t('All'), 0.507, 0.477, 0.223, 0.493)),
    (-127, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T1/T2')) + _t('Drones'), 0.449, 0.54, 0.549, 0.336)),
    (-128, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T1/T2')) + _t('Overmind'), 0.6, 0.557, 0.601, 0.504)),
    (-129, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T1/T2')) + _t('Seeker'), 0.085, 0.085, 0.085, 0)),
    (-130, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T1/T2')) + _t('Triglavian'), 0.463, 0.392, 0.447, 0.193)),
    (-131, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T1/T2')) + _t('Drifter'), 0.428, 0.428, 0.428, 0.287)),
    (-132, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T1/T2')) + _t('Sleeper'), 0.435, 0.435, 0.435, 0.329)),
    (-133, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T1/T2')) + _t('All'), 0.493, 0.472, 0.5, 0.362)),
    (-134, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('Drones'), 0.449, 0.54, 0.549, 0.264)),
    (-135, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('Overmind'), 0.6, 0.557, 0.601, 0.428)),
    (-136, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('Seeker'), 0.085, 0.085, 0.085, 0)),
    (-137, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('Triglavian'), 0.463, 0.392, 0.447, 0.071)),
    (-138, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('Drifter'), 0.428, 0.428, 0.428, 0.2)),
    (-139, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('Sleeper'), 0.435, 0.435, 0.435, 0.268)),
    (-140, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('All'), 0.493, 0.472, 0.5, 0.28)),
    (-141, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5')) + _t('Drones'), 0.449, 0.54, 0.549, 0.197)),
    (-142, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5')) + _t('Overmind'), 0.6, 0.557, 0.601, 0.356)),
    (-143, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5')) + _t('Seeker'), 0.085, 0.085, 0.085, 0)),
    (-144, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5')) + _t('Triglavian'), 0.463, 0.392, 0.447, 0.029)),
    (-145, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5')) + _t('Drifter'), 0.428, 0.428, 0.428, 0.117)),
    (-146, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5')) + _t('Sleeper'), 0.435, 0.435, 0.435, 0.215)),
    (-147, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5')) + _t('All'), 0.493, 0.472, 0.5, 0.21))])


class TargetProfile:
    # also determined import/export order - VERY IMPORTANT
    DAMAGE_TYPES = ('em', 'thermal', 'kinetic', 'explosive')
    _idealTarget = None
    _builtins = None

    def __init__(self, *args, **kwargs):
        self.builtin = False
        self.update(*args, **kwargs)

    @reconstructor
    def init(self):
        self.builtin = False

    def update(self, emAmount=0, thermalAmount=0, kineticAmount=0, explosiveAmount=0, maxVelocity=None, signatureRadius=None, radius=None):
        self.emAmount = emAmount
        self.thermalAmount = thermalAmount
        self.kineticAmount = kineticAmount
        self.explosiveAmount = explosiveAmount
        self._maxVelocity = maxVelocity
        self._signatureRadius = signatureRadius
        self._radius = radius

    @classmethod
    def getBuiltinList(cls):
        if cls._builtins is None:
            cls.__generateBuiltins()
        return list(cls._builtins.values())

    @classmethod
    def getBuiltinById(cls, id):
        if cls._builtins is None:
            cls.__generateBuiltins()
        return cls._builtins.get(id)

    @classmethod
    def __generateBuiltins(cls):
        cls._builtins = OrderedDict()
        for id, data in BUILTINS.items():
            rawName = data[0]
            data = data[1:]
            profile = TargetProfile(*data)
            profile.ID = id
            profile.rawName = rawName
            profile.builtin = True
            cls._builtins[id] = profile

    @classmethod
    def getIdeal(cls):
        if cls._idealTarget is None:
            cls._idealTarget = cls(
                    emAmount=0,
                    thermalAmount=0,
                    kineticAmount=0,
                    explosiveAmount=0,
                    maxVelocity=0,
                    signatureRadius=None,
                    radius=0)
            cls._idealTarget.rawName = _t('Ideal Target')
            cls._idealTarget.ID = 0
            cls._idealTarget.builtin = True
        return cls._idealTarget

    @property
    def maxVelocity(self):
        return self._maxVelocity or 0

    @maxVelocity.setter
    def maxVelocity(self, val):
        self._maxVelocity = val

    @property
    def signatureRadius(self):
        if self._signatureRadius is None or self._signatureRadius == -1:
            return math.inf
        return self._signatureRadius

    @signatureRadius.setter
    def signatureRadius(self, val):
        if val is not None and math.isinf(val):
            val = None
        self._signatureRadius = val

    @property
    def radius(self):
        return self._radius or 0

    @radius.setter
    def radius(self, val):
        self._radius = val

    @classmethod
    def importPatterns(cls, text):
        lines = re.split('[\n\r]+', text)
        patterns = []
        numPatterns = 0

        # When we import damage profiles, we create new ones and update old ones. To do this, get a list of current
        # patterns to allow lookup
        lookup = {}
        current = eos.db.getTargetProfileList()
        for pattern in current:
            lookup[pattern.rawName] = pattern

        for line in lines:
            try:
                if line.strip()[0] == "#":  # comments
                    continue
                line = line.split('#', 1)[0]  # allows for comments
                type, data = line.rsplit('=', 1)
                type, data = type.strip(), [d.strip() for d in data.split(',')]
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                pyfalog.warning("Data isn't in correct format, continue to next line.")
                continue

            if type not in ("TargetProfile", "TargetResists"):
                continue

            numPatterns += 1
            name, dataRes, dataMisc = data[0], data[1:5], data[5:8]
            fields = {}

            for index, val in enumerate(dataRes):
                val = float(val) if val else 0
                if math.isinf(val):
                    val = 0
                try:
                    assert 0 <= val <= 100
                    fields["%sAmount" % cls.DAMAGE_TYPES[index]] = val / 100
                except (KeyboardInterrupt, SystemExit):
                    raise
                except:
                    pyfalog.warning("Caught unhandled exception in import patterns.")
                    continue

            if len(dataMisc) == 3:
                for index, val in enumerate(dataMisc):
                    try:
                        fieldName = ("maxVelocity", "signatureRadius", "radius")[index]
                    except IndexError:
                        break
                    val = float(val) if val else 0
                    if fieldName != "signatureRadius" and math.isinf(val):
                        val = 0
                    fields[fieldName] = val

            if len(fields) in (4, 7):  # Avoid possible blank lines
                if name.strip() in lookup:
                    pattern = lookup[name.strip()]
                    pattern.update(**fields)
                    eos.db.save(pattern)
                else:
                    pattern = TargetProfile(**fields)
                    pattern.rawName = name.strip()
                    eos.db.save(pattern)
                patterns.append(pattern)

        eos.db.commit()

        return patterns, numPatterns

    EXPORT_FORMAT = "TargetProfile = %s,%.1f,%.1f,%.1f,%.1f,%.1f,%.1f,%.1f\n"

    @classmethod
    def exportPatterns(cls, *patterns):
        out = "# Exported from pyfa\n#\n"
        out += "# Values are in following format:\n"
        out += "# TargetProfile = [name],[EM %],[Thermal %],[Kinetic %],[Explosive %],[Max velocity m/s],[Signature radius m],[Radius m]\n\n"
        for dp in patterns:
            out += cls.EXPORT_FORMAT % (
                dp.rawName,
                dp.emAmount * 100,
                dp.thermalAmount * 100,
                dp.kineticAmount * 100,
                dp.explosiveAmount * 100,
                dp.maxVelocity,
                dp.signatureRadius,
                dp.radius
            )

        return out.strip()

    @property
    def name(self):
        return self.rawName

    @property
    def fullName(self):
        categories, tail = self.__parseRawName()
        return '{}{}'.format(''.join('[{}]'.format(c) for c in categories), tail)

    @property
    def shortName(self):
        return self.__parseRawName()[1]

    @property
    def hierarchy(self):
        return self.__parseRawName()[0]

    def __parseRawName(self):
        hierarchy = []
        remainingName = self.rawName.strip() if self.rawName else ''
        while True:
            start, end = remainingName.find('['), remainingName.find(']')
            if start == -1 or end == -1:
                return hierarchy, remainingName
            splitter = remainingName.find('|')
            if splitter != -1 and splitter == start - 1:
                return hierarchy, remainingName[1:]
            hierarchy.append(remainingName[start + 1:end])
            remainingName = remainingName[end + 1:].strip()

    def __deepcopy__(self, memo):
        p = TargetProfile(
                self.emAmount, self.thermalAmount, self.kineticAmount, self.explosiveAmount,
                self._maxVelocity, self._signatureRadius, self._radius)
        p.rawName = "%s copy" % self.rawName
        return p
