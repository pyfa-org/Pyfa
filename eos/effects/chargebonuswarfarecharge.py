# We should probably have something a little less hacky in place, but time is money!
type = "passive"
def handler(fit, module, context):

    def runEffect(id, value):
        if id == 21:  # Skirmish Burst: Interdiction Maneuvers: Tackle Range
            groups = ("Stasis Web", "Warp Scrambler")
            fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                          "maxRange", value,
                                          stackingPenalties=True)

    print "Inside the CHARGE"
    for x in xrange(1, 4):
        if module.getModifiedChargeAttr("warfareBuff{}ID".format(x)):
            runEffect(module.getModifiedChargeAttr("warfareBuff{}ID".format(x)), module.getModifiedChargeAttr("warfareBuff{}Value".format(x)))

