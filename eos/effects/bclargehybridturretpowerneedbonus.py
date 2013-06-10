# Used by:
# Ship: Naga
# Ship: Talos
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                     "power", ship.getModifiedItemAttr("bcLargeTurretPower"))
