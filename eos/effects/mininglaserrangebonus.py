# Used by:
# Implant: Low-grade Harvest Alpha
# Implant: Low-grade Harvest Beta
# Implant: Low-grade Harvest Delta
# Implant: Low-grade Harvest Epsilon
# Implant: Low-grade Harvest Gamma
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Mining Laser",
                                  "maxRange", implant.getModifiedItemAttr("maxRangeBonus"))