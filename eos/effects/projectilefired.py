# Used by:
# Modules from group: Hybrid Weapon (199 of 199)
# Modules from group: Projectile Weapon (143 of 143)
type = 'active'
def handler(fit, module, context):
    rt = module.getModifiedItemAttr("reloadTime")
    if not rt:
        # Set reload time to 10 seconds
        module.reloadTime = 10000
    else:
        module.reloadTime = rt
