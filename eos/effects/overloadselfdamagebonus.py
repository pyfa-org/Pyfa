# overloadSelfDamageBonus
#
# Used by:
# Modules from group: Energy Weapon (101 of 214)
# Modules from group: Hybrid Weapon (105 of 221)
# Modules from group: Projectile Weapon (99 of 165)
type = "overheat"


def handler(fit, module, context):
    module.boostItemAttr("damageMultiplier", module.getModifiedItemAttr("overloadDamageModifier"))
