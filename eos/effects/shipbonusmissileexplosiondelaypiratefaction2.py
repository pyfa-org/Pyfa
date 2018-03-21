# shipBonusMissileExplosionDelayPirateFaction2
#
# Used by:
# Ship: Barghest
# Ship: Garmur
# Ship: Orthrus
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "explosionDelay", ship.getModifiedItemAttr("shipBonusRole8"))
