# overloadRofBonus
#
# Used by:
# Modules from group: Missile Launcher Torpedo (22 of 22)
# Items from market group: Ship Equipment > Turrets & Bays (428 of 859)
# Module: Interdiction Sphere Launcher I
type = "overheat"


def handler(fit, module, context):
    module.boostItemAttr("speed", module.getModifiedItemAttr("overloadRofBonus"))
