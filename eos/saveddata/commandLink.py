# ===============================================================================
# Copyright (C) 2010 Diego Duclos
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

# Generic ("virtual") command links: warfare links carried by a fit at a chosen
# strength instead of a full booster fit with command burst modules and charges.
# Applied during calc by injecting the buffs into the fit's command bonuses, same
# path real command fits use (Fit.addCommandBonus / Fit.__runCommandBoosts).
# Buff base values and the strength multiplier mirror live command burst data
# (eve.db); see WARFARE_LINK_BASE_VALUES and getLinkMultiplier.

from logbook import Logger


pyfalog = Logger(__name__)


# Max Command Specialist skills (commandStrengthBonus 10%/level, level V) -> x1.5
SKILL_MULTIPLIER = 1.5

# T2 command burst tech factor (module warfareBuffXValue 1.25 vs 1.0 for T1)
TECH_MULTIPLIER = 1.25

# Warfare mindlink (mindlinkBonus 25 in eve.db) -> x1.25
MINDLINK_MULTIPLIER = 1.25

# Ship command bonus options shown in UI: % per level, level V assumed (0-5% -> x1.0-1.25)
STRENGTHS = (5, 4, 3, 2, 1, 0)


# linkType -> (display label, category key or None, [warfareBuffIDs])
# Base values for each buff id are in WARFARE_LINK_BASE_VALUES below.
COMMAND_LINK_DEFS = {
    # Shield
    'shield_all':            ('All Shield Links', 'shield', [10, 11, 12]),
    'shield_harmonizing':    ('Shield Harmonizing', 'shield', [10]),
    'shield_active':         ('Active Shielding', 'shield', [11]),
    'shield_extension':      ('Shield Extension', 'shield', [12]),
    # Armor
    'armor_all':             ('All Armor Links', 'armor', [13, 14, 15]),
    'armor_energizing':      ('Armor Energizing', 'armor', [13]),
    'armor_rapid':           ('Rapid Repair', 'armor', [14]),
    'armor_reinforcement':   ('Armor Reinforcement', 'armor', [15]),
    # Skirmish
    'skirmish_all':          ('All Skirmish Links', 'skirmish', [20, 60, 21, 22]),
    'skirmish_evasive':      ('Evasive Maneuvers', 'skirmish', [20, 60]),
    'skirmish_interdiction': ('Interdiction Maneuvers', 'skirmish', [21]),
    'skirmish_rapid':        ('Rapid Deployment', 'skirmish', [22]),
    # Information
    'information_all':       ('All Information Links', 'information', [16, 26, 17, 18, 19]),
    'info_sensor':           ('Sensor Optimization', 'information', [16, 26]),
    'info_superiority':      ('Electronic Superiority', 'information', [17]),
    'info_hardening':        ('Electronic Hardening', 'information', [18, 19]),
    # Expedition
    'expedition_all':        ('All Expedition Links', 'expedition', [2464, 2465, 2466, 2468, 2481]),
    'expedition_pinpointing': ('Expedition Pinpointing', 'expedition', [2466, 2481]),
    'expedition_reach':      ('Expedition Reach', 'expedition', [2465]),
    'expedition_strength':   ('Expedition Strength', 'expedition', [2464, 2468]),
    # Mining
    'mining_all':            ('All Mining Links', 'mining', [23, 24, 25]),
    'mining_field':          ('Mining Laser Field Enhancement', 'mining', [23]),
    'mining_optimization':   ('Mining Laser Optimization', 'mining', [24]),
    'mining_preservation':   ('Mining Equipment Preservation', 'mining', [25]),
}

# Order/labels for the per-category submenus.
CATEGORY_ORDER = ['shield', 'armor', 'skirmish', 'information', 'expedition', 'mining']
CATEGORY_LABELS = {
    'shield': 'Shield',
    'armor': 'Armor',
    'skirmish': 'Skirmish',
    'information': 'Information',
    'expedition': 'Expedition',
    'mining': 'Mining',
}
# linkType keys shown inside each category submenu, "All <category>" first.
CATEGORY_LINKS = {cat: [] for cat in CATEGORY_ORDER}
for _lt, (_lbl, _cat, _ids) in COMMAND_LINK_DEFS.items():
    if _cat in CATEGORY_LINKS:
        CATEGORY_LINKS[_cat].append(_lt)
for _cat in CATEGORY_LINKS:
    # "All <cat>" entries are named '<cat>_all' (or 'information_all'); keep them on top.
    CATEGORY_LINKS[_cat].sort(key=lambda lt: (not lt.endswith('_all'), lt))

# Special top-level "All Links" selection (every buff from every category).
ALL_LINK_TYPE = 'all'
_all_ids = []
for _lt, (_lbl, _cat, _ids) in COMMAND_LINK_DEFS.items():
    if _lt.endswith('_all') or _lt == 'information_all':
        _all_ids.extend(_ids)
COMMAND_LINK_DEFS[ALL_LINK_TYPE] = ('All Links', None, sorted(set(_all_ids)))

# buffID -> base value (= live command burst charge warfareBuffXMultiplier).
WARFARE_LINK_BASE_VALUES = {
    10: -8.0, 11: -8.0, 12: 8.0,
    13: -8.0, 14: -8.0, 15: 8.0,
    20: -6.0, 60: -6.0, 21: 12.0, 22: 12.0,
    16: 9.0, 26: 18.0, 17: 9.0, 18: 18.0, 19: -9.0,
    2464: 8.0, 2465: 20.0, 2466: -8.0, 2468: 8.0, 2481: -8.0,
    23: 40.0, 24: -15.0, 25: -15.0,
}

# buffID -> category (used to pick a representative burst module as the bonus source).
_BUFF_CATEGORY = {}
for _lt, (_lbl, _cat, _ids) in COMMAND_LINK_DEFS.items():
    if _cat is None:
        continue
    for _id in _ids:
        _BUFF_CATEGORY.setdefault(_id, _cat)

# Representative T1 command burst module per category (for "Affected by" display).
_CATEGORY_MODULE_TYPE = {
    'shield': 42529,       # Shield Command Burst I
    'armor': 42526,        # Armor Command Burst I
    'skirmish': 42530,     # Skirmish Command Burst I
    'information': 42527,  # Information Command Burst I
    'expedition': 89608,   # Expedition Command Burst I
    'mining': 42528,       # Mining Foreman Burst I
}


def getLinkMultiplier(strength, mindlink):
    # Command burst factors stack multiplicatively: max skills * T2 burst *
    # ship bonus (strength %/lvl, level V) * mindlink
    shipMultiplier = 1.0 + (strength / 100.0) * 5
    mindlinkMultiplier = MINDLINK_MULTIPLIER if mindlink else 1.0
    return SKILL_MULTIPLIER * TECH_MULTIPLIER * shipMultiplier * mindlinkMultiplier


class _GangEffect:
    # Stand-in so __runCommandBoosts treats generic-link bonuses as gang effects
    def isType(self, type):
        return type == "gang"


_GANG_EFFECT = _GangEffect()

# Cache of representative burst Module instances keyed by category.
_afflictorCache = {}


def _getAfflictor(category):
    # Cached burst Module to attribute the bonus to in 'Affected by'
    if category not in _afflictorCache:
        import eos.db
        from eos.saveddata.module import Module
        afflictor = None
        typeID = _CATEGORY_MODULE_TYPE.get(category)
        if typeID is not None:
            try:
                item = eos.db.getItem(typeID)
                if item is not None:
                    afflictor = Module(item)
            except Exception:
                pyfalog.warning("Could not build command link afflictor for category {}", category)
        _afflictorCache[category] = afflictor
    return _afflictorCache[category]


def applyCommandLinkToFit(fit, link):
    # Inject the link's warfare buffs into the fit's command bonuses
    definition = COMMAND_LINK_DEFS.get(link.linkType)
    if definition is None:
        pyfalog.warning("Unknown command link type {}", link.linkType)
        return
    multiplier = getLinkMultiplier(link.strength, link.mindlink)
    for buffID in definition[2]:
        baseValue = WARFARE_LINK_BASE_VALUES.get(buffID)
        if baseValue is None:
            continue
        afflictor = _getAfflictor(_BUFF_CATEGORY.get(buffID))
        fit.addCommandBonus(buffID, baseValue * multiplier, afflictor, _GANG_EFFECT)


class _LinkItem:
    # Item shim so the command view's columns can render a CommandLink row
    def __init__(self, name):
        self.name = name
        self.iconID = None


class CommandLink:
    # Generic command link selection stored on a fit (mapped in eos.db.saveddata.fit)
    def __init__(self, linkType, strength, mindlink=False, active=True):
        self.linkType = linkType
        self.strength = strength
        self.mindlink = mindlink
        self.active = active

    @property
    def label(self):
        definition = COMMAND_LINK_DEFS.get(self.linkType)
        return definition[0] if definition else self.linkType

    @property
    def name(self):
        suffix = " + Mindlink" if self.mindlink else ""
        return "{} ({}%/lvl{})".format(self.label, self.strength, suffix)

    @property
    def item(self):
        return _LinkItem(self.name)

    def __repr__(self):
        return "CommandLink(linkType={}, strength={}, mindlink={}, active={}) at {}".format(
                self.linkType, self.strength, self.mindlink, self.active, hex(id(self)))
