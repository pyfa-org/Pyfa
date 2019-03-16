# miningLaserRangeBonus
#
# Used by:
# Implants named like: grade Harvest (10 of 12)
type = "passive"


def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mining Laser",
                                  "maxRange", implant.getModifiedItemAttr("maxRangeBonus"))
