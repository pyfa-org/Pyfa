
'''
Some documentation:
When the fit is calculated, we gather up all the gang effects and stick them onto the fit. We don't run the actual
effect yet, only give the fit details so that it can run the effect at a later time. We need to do this so that we can
only run the strongest effect. When we are done, one of the last things that we do with the fit is to loop through those
bonuses and actually run the effect. To do this, we have a special argument passed into the effect handler that tells it
which warfareBuffID to run (shouldn't need this right now, but better safe than sorry)
'''

type = "active", "gang"
def handler(fit, module, context, **kwargs):
    print "submitting command bonuses to registrar"

    for x in xrange(1, 4):
        if module.getModifiedChargeAttr("warfareBuff{}ID".format(x)):
            value = module.getModifiedItemAttr("warfareBuff{}Value".format(x))
            id = module.getModifiedChargeAttr("warfareBuff{}ID".format(x))

            if id:
                fit.addCommandBonus(id, value, module, kwargs['effect'])


