# shipBonusEnergyNosOptimalAC1
#
# Used by:
# Ship: Vangel
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "maxRange", src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
