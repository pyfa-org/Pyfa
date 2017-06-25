type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner") or mod.item.requiresSkill("High Speed Maneuvering"),
                                  "overloadSpeedFactorBonus", src.getModifiedItemAttr("subsystemBonusGallentePropulsion2"),
                                  skill="Gallente Propulsion Systems")
