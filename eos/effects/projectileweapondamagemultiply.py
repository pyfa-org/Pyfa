# projectileWeaponDamageMultiply
#
# Used by:
# Modules from group: Gyrostabilizer (20 of 20)
# Modules named like: QA Multiship Module Players (4 of 4)
# Module: QA Damage Module
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Projectile Weapon",
                                  "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                  stackingPenalties = True)