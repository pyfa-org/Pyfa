# projectileWeaponSpeedMultiplyPassive
#
# Used by:
# Modules named like: Projectile Burst Aerator (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Projectile Weapon",
                                     "speed", module.getModifiedItemAttr("speedMultiplier"),
                                     stackingPenalties = True)