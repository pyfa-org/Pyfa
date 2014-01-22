# Used by:
# Modules named like: Modified Cloaking Device (5 of 5)
# Module: Caldari Navy Cloaking Device
# Module: Dread Guristas Cloaking Device
# Module: Improved 'Guise' Cloaking Device II
# Module: Improved Cloaking Device II
# Module: Prototype 'Poncho' Cloaking Device I
# Module: Prototype Cloaking Device I
# Module: Syndicate Cloaking Device
type = "active"
runTime = "early"
#TODO: Rewrite this effect
def handler(fit, module, context):
    # Set flag which is used to determine if ship is cloaked or not
    # This is used to apply cloak-only bonuses, like Black Ops' speed bonus
    # Doesn't apply to covops cloaks
    fit.extraAttributes["cloaked"] = True
    # Apply speed penalty
    fit.ship.multiplyItemAttr("maxVelocity", module.getModifiedItemAttr("maxVelocityBonus"))
