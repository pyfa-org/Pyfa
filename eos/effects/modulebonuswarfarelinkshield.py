
type = "active", "gang"
def handler(fit, module, context, **kwargs):
    print "submitting command bonuses to registrar"

    for x in xrange(1, 4):
        if module.getModifiedChargeAttr("warfareBuff{}ID".format(x)):
            value = module.getModifiedItemAttr("warfareBuff{}Value".format(x))
            id = module.getModifiedChargeAttr("warfareBuff{}ID".format(x))

            if id:
                fit.addCommandBonus(id, value, module, kwargs['effect'])