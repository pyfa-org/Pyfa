# Used by:
# Items from market group: Ship Equipment > Turrets & Bays > Hybrid Turrets > Railguns (110 of 110)
# Items from market group: Ship Equipment > Turrets & Bays > Laser Turrets > Beam Lasers (100 of 100)
# Items from market group: Ship Equipment > Turrets & Bays > Missile Launchers (126 of 126)
# Items from market group: Ship Equipment > Turrets & Bays > Projectile Turrets > Artillery Cannons (60 of 60)
# Module: Interdiction Sphere Launcher I
# Module: Khanid Navy Torpedo Launcher
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("speed", module.getModifiedItemAttr("overloadRofBonus"))
