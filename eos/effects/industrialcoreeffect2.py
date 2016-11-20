# industrialCoreEffect2
#
# Used by:
# Module: Industrial Core I
type = "active"
runTime = "early"


def handler(fit, module, context):
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
                                     "warfareBuff4Value",
                                     src.getModifiedItemAttr("shipBonusORECapital3"),
                                     skill="Capital Industrial Ships",
                                     )
