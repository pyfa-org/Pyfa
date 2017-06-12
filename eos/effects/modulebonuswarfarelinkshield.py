# moduleBonusWarfareLinkShield
#
# Used by:
# Variations of module: Shield Command Burst I (2 of 2)

type = "active", "gang"


def handler(fit, module, context, **kwargs):
    for x in range(1, 5):
        if module.getModifiedChargeAttr("warfareBuff{}ID".format(x)):
            value = module.getModifiedItemAttr("warfareBuff{}Value".format(x))
            id = module.getModifiedChargeAttr("warfareBuff{}ID".format(x))

            if id:
                fit.addCommandBonus(id, value, module, kwargs['effect'])
