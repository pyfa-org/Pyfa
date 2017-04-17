# shipBonusRole5RemoteArmorRepairPowergridBonus
#
# Used by:
# Ships from group: Logistics (3 of 6)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "power",
                                  src.getModifiedItemAttr("shipBonusRole5"))
