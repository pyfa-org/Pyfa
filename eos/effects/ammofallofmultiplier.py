# Used by:
# Charges from group: Advanced Artillery Ammo (6 of 6)
# Charges from group: Advanced Autocannon Ammo (6 of 6)
# Charges from group: Advanced Beam Laser Crystal (6 of 6)
# Charges from group: Advanced Blaster Charge (6 of 6)
# Charges from group: Advanced Pulse Laser Crystal (6 of 6)
# Charges from group: Advanced Railgun Charge (6 of 6)
type = "passive"
def handler(fit, module, context):
    module.multiplyItemAttr("falloff", module.getModifiedChargeAttr("fallofMultiplier") or 1)
