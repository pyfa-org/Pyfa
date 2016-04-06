# shipBonusDreadnoughtC3ReloadBonus
#
# Used by:
# Ship: Phoenix
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"), "reloadTime", src.getModifiedItemAttr("shipBonusDreadnoughtC3"), skill="Caldari Dreadnought")
