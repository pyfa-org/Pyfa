# powerBooster
#
# Used by:
# Modules from group: Capacitor Booster (59 of 59)
type = "active"


def handler(fit, module, context):
    # Set reload time to 10 seconds
    module.reloadTime = 10000
    # Make so that reloads are always taken into account during clculations
    module.forceReload = True

    if module.charge is None:
        return
    capAmount = module.getModifiedChargeAttr("capacitorBonus") or 0
    module.itemModifiedAttributes["capacitorNeed"] = -capAmount
