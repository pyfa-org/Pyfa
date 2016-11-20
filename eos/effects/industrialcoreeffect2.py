# industrialCoreEffect2
#
# Used by:
# Variations of module: Industrial Core I (2 of 2)
type = "active"
runTime = "early"


def handler(fit, module, context):
    return

    # @todo: finish this
    fit.extraAttributes["siege"] = True
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("speedFactor"))
    fit.ship.multiplyItemAttr("mass", module.getModifiedItemAttr("siegeMassMultiplier"))


    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name in
                                                 (
                                                     "Command Burst",
                                                 ) and
                                                 mod.item.requiresSkill in
                                                 (
                                                     "Shield Command",
                                                 ),
                                     "warfareBuff4Modifier",
                                     module.getModifiedItemAttr("shipBonusORECapital3"),
                                     skill="Capital Industrial Ships",
                                     )
