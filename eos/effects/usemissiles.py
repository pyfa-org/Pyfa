# useMissiles
#
# Used by:
# Modules from group: Missile Launcher Heavy (12 of 12)
# Modules from group: Missile Launcher Rocket (15 of 15)
# Modules named like: Launcher (151 of 151)
type = 'active'


def handler(fit, module, context):
    # Set reload time to 10 seconds
    module.reloadTime = 10000
