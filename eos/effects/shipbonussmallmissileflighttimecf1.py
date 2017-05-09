# shipBonusSmallMissileFlightTimeCF1
#
# Used by:
# Ship: Pacifier
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                    "explosionDelay", src.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                    "explosionDelay", src.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")
