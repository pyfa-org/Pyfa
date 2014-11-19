# drawbackPowerNeedProjectiles
#
# Used by:
# Modules from group: Rig Projectile Weapon (40 of 40)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Projectile Weapon",
                                  "power", module.getModifiedItemAttr("drawback"))