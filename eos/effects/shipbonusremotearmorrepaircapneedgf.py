# shipBonusRemoteArmorRepairCapNeedGF
#
# Used by:
# Variations of ship: Navitas (2 of 2)
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed", src.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")
