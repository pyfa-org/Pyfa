# shipBonusTitanRole3TorpdeoVelocityBonus
#
# Used by:
# Ship: Leviathan
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"), "maxVelocity",
                                    src.getModifiedItemAttr("shipBonusRole3"))
