# shipBonusDreadnoughtM3RepairTime
#
# Used by:
# Ship: Naglfar
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Operation"), "duration", src.getModifiedItemAttr("shipBonusDreadnoughtM2"), skill="Minmatar Dreadnought")
