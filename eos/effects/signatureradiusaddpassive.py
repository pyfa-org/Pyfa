# signatureRadiusAddPassive
#
# Used by:
# Subsystems from group: Defensive Systems (8 of 12)
# Subsystems named like: Propulsion Interdiction Nullifier (4 of 4)
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadius"))
