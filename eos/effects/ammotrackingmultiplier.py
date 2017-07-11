# ammoTrackingMultiplier
#
# Used by:
# Charges from group: Advanced Artillery Ammo (8 of 8)
# Charges from group: Advanced Autocannon Ammo (8 of 8)
# Charges from group: Advanced Beam Laser Crystal (8 of 8)
# Charges from group: Advanced Blaster Charge (8 of 8)
# Charges from group: Advanced Pulse Laser Crystal (8 of 8)
# Charges from group: Advanced Railgun Charge (8 of 8)
# Charges from group: Projectile Ammo (128 of 128)
type = "passive"


def handler(fit, module, context):
    module.multiplyItemAttr("trackingSpeed", module.getModifiedChargeAttr("trackingSpeedMultiplier"))
