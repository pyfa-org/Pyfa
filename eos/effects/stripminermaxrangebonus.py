# Used by:
# Implants named like: Low grade Harvest (5 of 6)
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Strip Miner",
                                  "maxRange", implant.getModifiedItemAttr("maxRangeBonus"))
