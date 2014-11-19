# overloadRofBonus
#
# Used by:
# Modules from group: Energy Weapon (100 of 186)
# Modules from group: Hybrid Weapon (110 of 202)
# Modules from group: Missile Launcher Citadel (4 of 4)
# Modules from group: Missile Launcher Heavy (12 of 12)
# Modules from group: Missile Launcher Rocket (15 of 15)
# Modules from group: Projectile Weapon (60 of 146)
# Modules named like: Launcher (125 of 138)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("speed", module.getModifiedItemAttr("overloadRofBonus"))
