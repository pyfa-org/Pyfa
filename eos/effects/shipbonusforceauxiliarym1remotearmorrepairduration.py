# shipBonusForceAuxiliaryM1RemoteArmorRepairDuration
#
# Used by:
# Ship: Dagon
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "duration", src.getModifiedItemAttr("shipBonusForceAuxiliaryM1"), skill="Minmatar Carrier")
