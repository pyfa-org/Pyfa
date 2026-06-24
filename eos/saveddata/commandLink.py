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

"""
Generic ("virtual") command links.

Instead of building a full booster fit with command burst modules and charges, a
fit can carry abstract warfare links at a chosen strength. A CommandLink describes
one such selection (which link or group of links, at which per-level strength, with
or without a mindlink) and is applied during fit calculation by injecting the
relevant warfare buffs straight into the boosted fit's command bonuses - reusing
the exact same machinery (Fit.addCommandBonus / Fit.__runCommandBoosts) that real
command fits use.

The numbers below mirror live EVE command burst data (see eve.db):
  - base value of a buff = the command burst CHARGE's warfareBuffXMultiplier
    (the module's warfareBuffXValue is just a 1.0 T1 / 1.25 T2 tech factor; we
    assume a T2 burst, i.e. x1.25).
  - command bursts are scaled by four independent, multiplicative factors:
      * Command Specialist skills: commandStrengthBonus = 10%/level. We ALWAYS
        assume maximum skills (level V), i.e. x1.5.
      * T2 command burst module tech factor, i.e. x1.25.
      * Ship command bonus: 0% to 5% per level (level V assumed), i.e. x1.0 to
        x1.25. This is the user-chosen strength.
      * Warfare Mindlink: mindlinkBonus = 25%, i.e. x1.25 (optional).
    In pyfa these are applied as separate boosts to the charge's
    warfareBuffXMultiplier, so they stack multiplicatively (see eos.effects).
"""

from logbook import Logger


pyfalog = Logger(__name__)


# Maximum Command Specialist skills: commandStrengthBonus = 10%/level, level V
# assumed -> +50% -> x1.5. Generic links always assume max skills.
SKILL_MULTIPLIER = 1.5

# T2 command burst module: the module's warfareBuffXValue tech factor is 1.25
# (vs 1.0 for T1). Generic links assume a T2 burst.
TECH_MULTIPLIER = 1.25

# Warfare mindlink: mindlinkBonus = 25 in eve.db -> x1.25.
MINDLINK_MULTIPLIER = 1.25

# Per-level ship command bonus options offered in the UI (percent per level, level
# V assumed): 0% (no bonus) up to 5%/level (a command ship, -> x1.25).
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
    """Total strength multiplier applied to a link's base (no-bonus) value.

    Generic links always assume maximum Command Specialist skills (x1.5) and a T2
    command burst (x1.25). The chosen strength is the ship's command bonus per
    level (0-5%, level V assumed, so x1.0 to x1.25) and a warfare mindlink adds
    another x1.25. These factors stack multiplicatively, matching how real
    command bursts are calculated.
    """
    shipMultiplier = 1.0 + (strength / 100.0) * 5
    mindlinkMultiplier = MINDLINK_MULTIPLIER if mindlink else 1.0
    return SKILL_MULTIPLIER * TECH_MULTIPLIER * shipMultiplier * mindlinkMultiplier


class _GangEffect:
    """Minimal stand-in so Fit.__runCommandBoosts recognises generic-link bonuses as gang effects."""

    def isType(self, type):
        return type == "gang"


_GANG_EFFECT = _GangEffect()

# Cache of representative burst Module instances keyed by category.
_afflictorCache = {}


def _getAfflictor(category):
    """Return a (cached) real command burst Module to attribute the bonus to in 'Affected by'."""
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
    """Inject a generic command link's warfare buffs into the fit's command bonuses."""
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
    """Lightweight item shim so the command view's columns can render a CommandLink row."""

    def __init__(self, name):
        self.name = name
        self.iconID = None


class CommandLink:
    """A generic command link selection stored on a fit. Mapped in eos.db.saveddata.fit."""

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
