# targetAttack
#
# Used by:
# Drones from group: Combat Drone (74 of 74)
# Drones from group: Fighter Drone (4 of 4)
# Modules from group: Energy Weapon (186 of 186)
type = 'active'
def handler(fit, module, context):
    # Set reload time to 1 second
    module.reloadTime = 1000
