type = "active", "gang"
def handler(fit, module, context, **kwargs):
    for x in xrange(1, 5):
        if module.getModifiedItemAttr("warfareBuff{}ID".format(x)):
            value = module.getModifiedItemAttr("warfareBuff{}Value".format(x))
            id = module.getModifiedItemAttr("warfareBuff{}ID".format(x))

            if id:
                fit.addCommandBonus(id, value, module, kwargs['effect'])




