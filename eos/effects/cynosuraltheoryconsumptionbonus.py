# cynosuralTheoryConsumptionBonus
#
# Used by:
# Ships from group: Force Recon Ship (7 of 8)
# Skill: Cynosural Field Theory
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Cynosural Field",
                                  "consumptionQuantity",
                                  container.getModifiedItemAttr("consumptionQuantityBonusPercentage") * level)
