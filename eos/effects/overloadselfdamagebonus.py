# overloadSelfDamageBonus
#
# Used by:
# Modules from group: Energy Weapon (102 of 209)
# Modules from group: Hybrid Weapon (106 of 221)
# Modules from group: Projectile Weapon (100 of 165)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("damageMultiplier", module.getModifiedItemAttr("overloadDamageModifier"))