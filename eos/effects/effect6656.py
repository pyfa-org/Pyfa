# shipBonusRole3XLTorpdeoVelocityBonus
#
# Used by:
# Variations of ship: Leviathan (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "maxVelocity",
                                    src.getModifiedItemAttr("shipBonusRole3"))
