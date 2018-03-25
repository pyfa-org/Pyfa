# overloadRofBonus
#
# Used by:
# Modules from group: Missile Launcher Torpedo (22 of 22)
# Items from market group: Ship Equipment > Turrets & Bays (429 of 863)
# Module: Interdiction Sphere Launcher I
type = "overheat"


def handler(fit, module, context):
    module.boostItemAttr("speed", module.getModifiedItemAttr("overloadRofBonus"))
