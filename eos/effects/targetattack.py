# targetAttack
#
# Used by:
# Drones from group: Combat Drone (75 of 75)
# Modules from group: Energy Weapon (212 of 214)
type = 'active'


def handler(fit, module, context):
    # Set reload time to 1 second
    module.reloadTime = 1000
