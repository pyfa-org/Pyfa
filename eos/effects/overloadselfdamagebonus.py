# Used by:
# Items from market group: Ship Equipment > Turrets & Bays > Hybrid Turrets > Blasters (89 of 89)
# Items from market group: Ship Equipment > Turrets & Bays > Laser Turrets > Pulse Lasers (83 of 83)
# Items from market group: Ship Equipment > Turrets & Bays > Projectile Turrets > Autocannons (83 of 83)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("damageMultiplier", module.getModifiedItemAttr("overloadDamageModifier"))