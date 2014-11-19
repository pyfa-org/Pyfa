# projectileFired
#
# Used by:
# Modules from group: Hybrid Weapon (202 of 202)
# Modules from group: Projectile Weapon (146 of 146)
type = 'active'
def handler(fit, module, context):
    rt = module.getModifiedItemAttr("reloadTime")
    if not rt:
        # Set reload time to 10 seconds
        module.reloadTime = 10000
    else:
        module.reloadTime = rt
