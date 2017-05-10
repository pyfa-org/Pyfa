# shipBonusForceAuxiliaryM1RemoteDuration
#
# Used by:
# Ship: Lif
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems") or
                                              mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "duration", src.getModifiedItemAttr("shipBonusForceAuxiliaryM1"),
                                  skill="Minmatar Carrier")

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems") or
                                              mod.item.requiresSkill("Capital Remote Armor Repair Systems"),
                                  "duration", src.getModifiedItemAttr("shipBonusForceAuxiliaryM1"),
                                  skill="Minmatar Carrier")
