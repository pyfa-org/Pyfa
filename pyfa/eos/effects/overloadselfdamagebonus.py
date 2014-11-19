# overloadSelfDamageBonus
#
# Used by:
# Modules from group: Energy Weapon (86 of 186)
# Modules from group: Hybrid Weapon (92 of 202)
# Modules from group: Projectile Weapon (86 of 146)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("damageMultiplier", module.getModifiedItemAttr("overloadDamageModifier"))