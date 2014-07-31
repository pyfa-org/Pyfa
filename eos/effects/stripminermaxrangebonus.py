# Used by:
# Implants named like: grade Harvest (10 of 12)
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Strip Miner",
                                  "maxRange", implant.getModifiedItemAttr("maxRangeBonus"))
