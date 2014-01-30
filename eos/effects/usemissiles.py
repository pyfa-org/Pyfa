# Used by:
# Modules from group: Missile Launcher Bomb (2 of 2)
# Modules from group: Scan Probe Launcher (7 of 7)
# Modules from group: Survey Probe Launcher (2 of 2)
# Items from market group: Ship Equipment > Turrets & Bays > Missile Launchers (126 of 126)
# Module: Civilian Light Missile Launcher
# Module: Festival Launcher
# Module: Interdiction Sphere Launcher I
# Module: Khanid Navy Torpedo Launcher
type = 'active'
def handler(fit, module, context):
    # Set reload time to 10 seconds
    module.reloadTime = 10000
