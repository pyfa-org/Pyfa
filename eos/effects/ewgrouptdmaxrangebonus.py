# ewGroupTdMaxRangeBonus
#
# Used by:
# Implants named like: grade Centurion (10 of 12)
type = "passive"


def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Weapon Disruptor",
                                  "maxRange", implant.getModifiedItemAttr("rangeSkillBonus"))
