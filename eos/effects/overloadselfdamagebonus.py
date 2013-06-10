# Used by:
# Modules from group: Energy Weapon (83 of 183)
# Modules from group: Hybrid Weapon (89 of 199)
# Modules from group: Projectile Weapon (83 of 143)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("damageMultiplier", module.getModifiedItemAttr("overloadDamageModifier"))