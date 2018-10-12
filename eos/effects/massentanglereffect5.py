type = "active"


def handler(fit, src, context):
    fit.ship.increaseItemAttr("warpScrambleStatus", src.getModifiedItemAttr("warpScrambleStrength"))
    fit.ship.boostItemAttr("mass", src.getModifiedItemAttr("massBonusPercentage"), stackingPenalties=True)
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"), "speedFactor",
                                  src.getModifiedItemAttr("speedFactorBonus"), stackingPenalties=True)
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"), "speedBoostFactor",
                                  src.getModifiedItemAttr("speedBoostFactorBonus"))
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"), "activationBlocked",
                                     src.getModifiedItemAttr("activationBlockedStrenght"))
    fit.ship.boostItemAttr("maxVelocity", src.getModifiedItemAttr("maxVelocityBonus"), stackingPenalties=True)
