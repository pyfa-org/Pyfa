# We should probably have something a little less hacky in place, but time is money!


'''
Some documentation:
When the fit is calculated, we gather up all the gang effects and stick them onto the fit. We don't run the actual
effect yet, only give the fit details so that it can run the effect at a later time. We need to do this so that we can
only run the strongest effect. When we are done, one of the last things that we do with the fit is to loop through those
bonuses and actually run the effect. To do this, we have a special argument passed into the effect handler that tells it
which warfareBuffID to run (shouldn't need this right now, but better safe than sorry)
'''

type = "passive", "gang"
def handler(fit, module, context, **kwargs):
    print "In chargeBonusWarfareEffect, context: ", context

    def runEffect(id, value):
        print "RUN EFFECT: ", fit,
        if id == 21:  # Skirmish Burst: Interdiction Maneuvers: Tackle Range
            print "Tackle Range"
            return
            groups = ("Stasis Web", "Warp Scrambler")
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                              "maxRange", value,
                                          stackingPenalties=True)
        if id == 10:
            print "Shield Resists"

    print "Inside the CHARGE"

    for x in xrange(1, 4):
        if module.getModifiedChargeAttr("warfareBuff{}ID".format(x)):
            value = module.getModifiedChargeAttr("warfareBuff{}Value".format(x))
            id = module.getModifiedChargeAttr("warfareBuff{}ID".format(x))
            print "Buff ID: ",id," value: ",value
            if id:
                if 'commandRun' not in context:
                    print "Add buffID", id, " to ", fit
                    fit.addCommandBonus(id, value, module, kwargs['effect'])
                elif kwargs['warfareBuffID'] is not None and kwargs['warfareBuffID'] == id:
                    print "Running buffID ", kwargs['warfareBuffID'], " on ", fit
                    runEffect(kwargs['warfareBuffID'], value)

