# moduleBonusWarfareLinkArmor
#
# Used by:
# Variations of module: Armor Command Burst I (2 of 2)
type = "active"
runTime = "early"

def handler(fit, module, context):
    for x in xrange(1, 4):
        value = module.getModifiedItemAttr("warfareBuff{}Value".format(x))
        module.multiplyChargeAttr("warfareBuff{}Multiplier".format(x), value)
