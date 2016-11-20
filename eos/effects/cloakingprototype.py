# cloakingPrototype
#
# Used by:
# Modules named like: Prototype Cloaking Device I (2 of 2)
type = "active"
runTime = "early"


# TODO: Rewrite this effect
def handler(fit, module, context):
    # Set flag which is used to determine if ship is cloaked or not
    # This is used to apply cloak-only bonuses, like Black Ops' speed bonus
    # Doesn't apply to covops cloaks
    fit.extraAttributes["cloaked"] = True
    # Apply speed penalty
    fit.ship.multiplyItemAttr("maxVelocity", module.getModifiedItemAttr("maxVelocityModifier"))
