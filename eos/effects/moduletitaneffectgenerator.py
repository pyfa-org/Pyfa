# moduleTitanEffectGenerator
#
# Used by:
# Modules from group: Titan Phenomena Generator (4 of 4)
type = "active", "gang"


def handler(fit, module, context, **kwargs):
    for x in range(1, 5):
        if module.getModifiedItemAttr("warfareBuff{}ID".format(x)):
            value = module.getModifiedItemAttr("warfareBuff{}Value".format(x))
            id = module.getModifiedItemAttr("warfareBuff{}ID".format(x))

            if id:
                fit.addCommandBonus(id, value, module, kwargs['effect'])
