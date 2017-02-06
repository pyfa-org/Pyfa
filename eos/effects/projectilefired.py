# projectileFired
#
# Used by:
# Modules from group: Hybrid Weapon (221 of 221)
# Modules from group: Projectile Weapon (165 of 165)
type = 'active'


def handler(fit, module, context):
    rt = module.getModifiedItemAttr("reloadTime")
    if not rt:
        # Set reload time to 10 seconds
        module.reloadTime = 10000
    else:
        module.reloadTime = rt
