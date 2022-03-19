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
    # Anomic Team, source: client data dump
    (-40, (_c(_t('NPC')) + _c(_t('Burner')) + _c(_t('Team')) + _t('Enyo'), 0.575, 0.724, 0.862, 0.235, 1020, 37, 39)),
    (-41, (_c(_t('NPC')) + _c(_t('Burner')) + _c(_t('Team')) + _t('Navitas'), 0.681, 0.586, 0.522, 0.49, 870, 30, 35)),
    (-42, (_c(_t('NPC')) + _c(_t('Burner')) + _c(_t('Team')) + _t('Hawk'), 0.3, 0.86, 0.79, 0.65, 1122, 48, 39)),
    (-43, (_c(_t('NPC')) + _c(_t('Burner')) + _c(_t('Team')) + _t('Bantam'), 0.344, 0.475, 0.606, 0.672, 1016, 45, 27)),
    (-44, (_c(_t('NPC')) + _c(_t('Burner')) + _c(_t('Team')) + _t('Jaguar'), 0.781, 0.65, 0.475, 0.563, 1400, 42, 31)),
    (-45, (_c(_t('NPC')) + _c(_t('Burner')) + _c(_t('Team')) + _t('Burst'), 0.344, 0.475, 0.606, 0.672, 1174, 39, 31)),
    (-46, (_c(_t('NPC')) + _c(_t('Burner')) + _c(_t('Team')) + _t('Vengeance'), 0.66, 0.558, 0.745, 0.864, 1050, 37, 40)),
    (-47, (_c(_t('NPC')) + _c(_t('Burner')) + _c(_t('Team')) + _t('Inquisitor'), 0.681, 0.586, 0.522, 0.49, 920, 29, 20.5)),
    # Anomic Agent & Base, source: client data dump
    (-48, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Cruor'), 0.795, 0.734, 0.693, 0.672, 900, 18, 20.5)),
    (-49, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Dramiel'), 0.351, 0.481, 0.611, 0.676, 2100, 11, 25)),
    (-50, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Daredevil'), 0.685, 0.59, 0.59, 0.433, 1200, 18, 25)),
    (-51, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Succubus'), 0.351, 0.481, 0.611, 0.676, 4750, 30, 59)),
    (-52, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Worm'), 0.475, 0.58, 0.685, 0.738, 360, 70, 39)),
    (-53, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Ashimmu'), 0.8, 0.76, 0.68, 0.7, 500, 120, 137)),
    (-54, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Sentinel'), 0.575, 0.448, 0.522, 0.66, 500, 50, 39)),
    (-55, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Talos'), 0.681, 0.586, 0.586, 0.426, 150, 125, 266)),
    (-56, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Dragonfly'), 0.35, 0.72, 0.70, 0.55, 1200, 15, 35)),
    (-57, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Mantis'), 0.60, 0.52, 0.71, 0.71, 900, 25, 35)),
    # Source: ticket #2067
    (-58, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Triglavian Entities'), 0.422, 0.367, 0.453, 0.411)),
    (-59, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Amarr EDENCOM Entities'), 0.360, 0.310, 0.441, 0.602)),
    (-60, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Caldari EDENCOM Entities'), 0.303, 0.610, 0.487, 0.401)),
    (-61, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Gallente EDENCOM Entities'), 0.383, 0.414, 0.578, 0.513)),
    (-62, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Minmatar EDENCOM Entities'), 0.620, 0.422, 0.355, 0.399)),
    (-63, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('Drones'), 0.439, 0.522, 0.529, 0.435)),
    (-64, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('Overmind'), 0.643, 0.593, 0.624, 0.639)),
    (-65, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('Seeker'), 0.082, 0.082, 0.082, 0.082)),
    (-66, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('Triglavian'), 0.494, 0.41, 0.464, 0.376)),
    (-67, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('Drifter'), 0.415, 0.415, 0.415, 0.415)),
    (-68, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('Sleeper'), 0.435, 0.435, 0.435, 0.435)),
    (-69, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('All'), 0.508, 0.474, 0.495, 0.488)),
    (-70, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T0/T1/T2')) + _t('Drones'), 0.323, 0.522, 0.529, 0.435)),
    (-71, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T0/T1/T2')) + _t('Overmind'), 0.542, 0.593, 0.624, 0.639)),
    (-72, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T0/T1/T2')) + _t('Seeker'), 0, 0.082, 0.082, 0.082)),
    (-73, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T0/T1/T2')) + _t('Triglavian'), 0.356, 0.41, 0.464, 0.376)),
    (-74, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T0/T1/T2')) + _t('Drifter'), 0.277, 0.415, 0.415, 0.415)),
    (-75, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T0/T1/T2')) + _t('Sleeper'), 0.329, 0.435, 0.435, 0.435)),
    (-76, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T0/T1/T2')) + _t('All'), 0.381, 0.474, 0.495, 0.488)),
    (-77, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('Drones'), 0.255, 0.522, 0.529, 0.435)),
    (-78, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('Overmind'), 0.48, 0.593, 0.624, 0.639)),
    (-79, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('Seeker'), 0, 0.082, 0.082, 0.0822)),
    (-80, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('Triglavian'), 0.268, 0.41, 0.464, 0.376)),
    (-81, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('Drifter'), 0.191, 0.415, 0.415, 0.415)),
    (-82, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('Sleeper'), 0.268, 0.435, 0.435, 0.435)),
    (-83, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('All'), 0.308, 0.474, 0.495, 0.488)),
    (-84, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5/T6')) + _t('Drones'), 0.193, 0.522, 0.529, 0.435)),
    (-85, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5/T6')) + _t('Overmind'), 0.423, 0.593, 0.624, 0.639)),
    (-86, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5/T6')) + _t('Seeker'), 0, 0.082, 0.082, 0.082)),
    (-87, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5/T6')) + _t('Triglavian'), 0.206, 0.41, 0.464, 0.376)),
    (-88, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5/T6')) + _t('Drifter'), 0.111, 0.415, 0.415, 0.415)),
    (-89, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5/T6')) + _t('Sleeper'), 0.215, 0.435, 0.435, 0.435)),
    (-90, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5/T6')) + _t('All'), 0.247, 0.474, 0.495, 0.488)),
    (-91, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T0/T1/T2')) + _t('Drones'), 0.461, 0.425, 0.541, 0.443)),
    (-92, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T0/T1/T2')) + _t('Overmind'), 0.666, 0.489, 0.634, 0.646)),
    (-93, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T0/T1/T2')) + _t('Seeker'), 0.084, 0, 0.084, 0.084)),
    (-94, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T0/T1/T2')) + _t('Triglavian'), 0.537, 0.269, 0.489, 0.371)),
    (-95, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T0/T1/T2')) + _t('Drifter'), 0.43, 0.289, 0.43, 0.43)),
    (-96, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T0/T1/T2')) + _t('Sleeper'), 0.512, 0.402, 0.512, 0.512)),
    (-97, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T0/T1/T2')) + _t('All'), 0.537, 0.352, 0.512, 0.495)),
    (-98, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('Drones'), 0.461, 0.36, 0.541, 0.443)),
    (-99, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('Overmind'), 0.666, 0.413, 0.634, 0.646)),
    (-100, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('Seeker'), 0.084, 0, 0.084, 0.084)),
    (-101, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('Triglavian'), 0.537, 0.166, 0.489, 0.371)),
    (-102, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('Drifter'), 0.43, 0.201, 0.43, 0.43)),
    (-103, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('Sleeper'), 0.512, 0.337, 0.512, 0.512)),
    (-104, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('All'), 0.537, 0.269, 0.512, 0.495)),
    (-105, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5/T6')) + _t('Drones'), 0.461, 0.305, 0.541, 0.443)),
    (-106, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5/T6')) + _t('Overmind'), 0.666, 0.345, 0.634, 0.646)),
    (-107, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5/T6')) + _t('Seeker'), 0.084, 0, 0.084, 0.084)),
    (-108, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5/T6')) + _t('Triglavian'), 0.537, 0.085, 0.489, 0.371)),
    (-109, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5/T6')) + _t('Drifter'), 0.43, 0.117, 0.43, 0.43)),
    (-110, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5/T6')) + _t('Sleeper'), 0.512, 0.276, 0.512, 0.512)),
    (-111, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5/T6')) + _t('All'), 0.537, 0.201, 0.512, 0.495)),
    (-112, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T0/T1/T2')) + _t('Drones'), 0.439, 0.522, 0.417, 0.435)),
    (-113, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T0/T1/T2')) + _t('Overmind'), 0.643, 0.593, 0.511, 0.639)),
    (-114, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T0/T1/T2')) + _t('Seeker'), 0.082, 0.082, 0, 0.082)),
    (-115, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T0/T1/T2')) + _t('Triglavian'), 0.494, 0.41, 0.304, 0.376)),
    (-116, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T0/T1/T2')) + _t('Drifter'), 0.415, 0.415, 0.277, 0.415)),
    (-117, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T0/T1/T2')) + _t('Sleeper'), 0.435, 0.435, 0.329, 0.435)),
    (-118, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T0/T1/T2')) + _t('All'), 0.508, 0.474, 0.359, 0.488)),
    (-119, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('Drones'), 0.439, 0.522, 0.351, 0.435)),
    (-120, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('Overmind'), 0.643, 0.593, 0.435, 0.639)),
    (-121, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('Seeker'), 0.082, 0.082, 0, 0.082)),
    (-122, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('Triglavian'), 0.494, 0.41, 0.198, 0.376)),
    (-123, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('Drifter'), 0.415, 0.415, 0.191, 0.415)),
    (-124, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('Sleeper'), 0.435, 0.435, 0.268, 0.435)),
    (-125, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('All'), 0.508, 0.474, 0.276, 0.488)),
    (-126, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5/T6')) + _t('Drones'), 0.439, 0.522, 0.293, 0.435)),
    (-127, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5/T6')) + _t('Overmind'), 0.643, 0.593, 0.362, 0.639)),
    (-128, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5/T6')) + _t('Seeker'), 0.082, 0.082, 0, 0.082)),
    (-129, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5/T6')) + _t('Triglavian'), 0.494, 0.41, 0.122, 0.376)),
    (-130, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5/T6')) + _t('Drifter'), 0.415, 0.415, 0.111, 0.415)),
    (-131, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5/T6')) + _t('Sleeper'), 0.435, 0.435, 0.215, 0.435)),
    (-132, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5/T6')) + _t('All'), 0.508, 0.474, 0.208, 0.488)),
    (-133, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T0/T1/T2')) + _t('Drones'), 0.449, 0.54, 0.549, 0.336)),
    (-134, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T0/T1/T2')) + _t('Overmind'), 0.619, 0.574, 0.612, 0.522)),
    (-135, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T0/T1/T2')) + _t('Seeker'), 0.085, 0.085, 0.085, 0)),
    (-136, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T0/T1/T2')) + _t('Triglavian'), 0.477, 0.4, 0.461, 0.202)),
    (-137, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T0/T1/T2')) + _t('Drifter'), 0.437, 0.437, 0.437, 0.295)),
    (-138, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T0/T1/T2')) + _t('Sleeper'), 0.435, 0.435, 0.435, 0.329)),
    (-139, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T0/T1/T2')) + _t('All'), 0.493, 0.468, 0.492, 0.35)),
    (-140, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('Drones'), 0.449, 0.54, 0.549, 0.264)),
    (-141, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('Overmind'), 0.619, 0.574, 0.612, 0.449)),
    (-142, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('Seeker'), 0.085, 0.085, 0.085, 0)),
    (-143, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('Triglavian'), 0.477, 0.4, 0.461, 0.081)),
    (-144, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('Drifter'), 0.437, 0.437, 0.437, 0.206)),
    (-145, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('Sleeper'), 0.435, 0.435, 0.435, 0.268)),
    (-146, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('All'), 0.493, 0.468, 0.492, 0.264)),
    (-147, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5/T6')) + _t('Drones'), 0.449, 0.54, 0.549, 0.197)),
    (-148, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5/T6')) + _t('Overmind'), 0.619, 0.574, 0.612, 0.379)),
    (-149, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5/T6')) + _t('Seeker'), 0.085, 0.085, 0.085, 0)),
    (-150, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5/T6')) + _t('Triglavian'), 0.477, 0.4, 0.461, 0.034)),
    (-151, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5/T6')) + _t('Drifter'), 0.437, 0.437, 0.437, 0.121)),
    (-152, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5/T6')) + _t('Sleeper'), 0.435, 0.435, 0.435, 0.215)),
    (-153, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5/T6')) + _t('All'), 0.493, 0.468, 0.492, 0.196)),
    # Source: ticket #2265
    (-154, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('Concord'), 0.324, 0.318, 0.369, 0.372)),
    (-155, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('Sansha'), 0.137, 0.331, 0.332, 0.322)),
    (-156, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Dark Matter All Tiers')) + _t('Angel'), 0.582, 0.508, 0.457, 0.416)),
    (-157, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T0/T1/T2')) + _t('Concord'), 0.121, 0.318, 0.369, 0.372)),
    (-158, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T0/T1/T2')) + _t('Sansha'), 0.034, 0.331, 0.332, 0.322)),
    (-159, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T0/T1/T2')) + _t('Angel'), 0.456, 0.508, 0.457, 0.416)),
    (-160, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('Concord'), 0.025, 0.318, 0.369, 0.372)),
    (-161, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('Sansha'), 0.018, 0.331, 0.332, 0.322)),
    (-162, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T3 (Some T5 Rooms)')) + _t('Angel'), 0.373, 0.508, 0.457, 0.416)),
    (-163, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5/T6')) + _t('Concord'), 0.008, 0.318, 0.369, 0.372)),
    (-164, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5/T6')) + _t('Sansha'), 0.009, 0.331, 0.332, 0.322)),
    (-165, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Electrical T4/T5/T6')) + _t('Angel'), 0.3, 0.508, 0.457, 0.416)),
    (-166, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T0/T1/T2')) + _t('Concord'), 0.324, 0.107, 0.369, 0.372)),
    (-167, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T0/T1/T2')) + _t('Sansha'), 0.148, 0.181, 0.329, 0.328)),
    (-168, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T0/T1/T2')) + _t('Angel'), 0.587, 0.342, 0.439, 0.39)),
    (-169, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('Concord'), 0.324, 0.016, 0.369, 0.372)),
    (-170, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('Sansha'), 0.148, 0.14, 0.329, 0.328)),
    (-171, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T3 (Some T5 Rooms)')) + _t('Angel'), 0.587, 0.241, 0.439, 0.39)),
    (-172, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5/T6')) + _t('Concord'), 0.324, 0.004, 0.369, 0.372)),
    (-173, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5/T6')) + _t('Sansha'), 0.148, 0.106, 0.329, 0.328)),
    (-174, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Firestorm T4/T5/T6')) + _t('Angel'), 0.587, 0.172, 0.439, 0.39)),
    (-175, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T0/T1/T2')) + _t('Concord'), 0.324, 0.318, 0.18, 0.372)),
    (-176, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T0/T1/T2')) + _t('Sansha'), 0.137, 0.331, 0.166, 0.322)),
    (-177, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T0/T1/T2')) + _t('Angel'), 0.582, 0.508, 0.295, 0.416)),
    (-178, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('Concord'), 0.324, 0.318, 0.089, 0.372)),
    (-179, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('Sansha'), 0.137, 0.331, 0.108, 0.322)),
    (-180, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T3 (Some T5 Rooms)')) + _t('Angel'), 0.582, 0.508, 0.203, 0.416)),
    (-181, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5/T6')) + _t('Concord'), 0.324, 0.318, 0.068, 0.372)),
    (-182, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5/T6')) + _t('Sansha'), 0.137, 0.331, 0.073, 0.322)),
    (-183, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Exotic T4/T5/T6')) + _t('Angel'), 0.582, 0.508, 0.14, 0.416)),
    (-184, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T0/T1/T2')) + _t('Concord'), 0.324, 0.318, 0.369, 0.203)),
    (-185, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T0/T1/T2')) + _t('Sansha'), 0.137, 0.355, 0.352, 0.16)),
    (-186, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T0/T1/T2')) + _t('Angel'), 0.59, 0.528, 0.477, 0.286)),
    (-187, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('Concord'), 0.324, 0.318, 0.369, 0.112)),
    (-188, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('Sansha'), 0.137, 0.355, 0.352, 0.05)),
    (-189, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T3 (Some T5 Rooms)')) + _t('Angel'), 0.59, 0.528, 0.477, 0.197)),
    (-190, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5/T6')) + _t('Concord'), 0.324, 0.318, 0.369, 0.086)),
    (-191, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5/T6')) + _t('Sansha'), 0.137, 0.355, 0.352, 0)),
    (-192, (_c(_t('NPC')) + _c(_t('Abyssal')) + _c(_t('Gamma T4/T5/T6')) + _t('Angel'), 0.59, 0.528, 0.477, 0.126)),
    (-193, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Drifter Entities'), 0.128, 0.375, 0.383, 0.383)),
    (-194, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Rogue Drone Entities'), 0.104, 0.147, 0.147, 0.102)),
    (-195, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Sleeper Entities'), 0.563, 0.563, 0.563, 0.563))])


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
