# projectileWeaponSpeedMultiply
#
# Used by:
# Modules from group: Gyrostabilizer (12 of 12)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Projectile Weapon",
                                     "speed", module.getModifiedItemAttr("speedMultiplier"),
                                     stackingPenalties = True)