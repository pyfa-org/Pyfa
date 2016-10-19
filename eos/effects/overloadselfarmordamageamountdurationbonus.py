# overloadSelfArmorDamageAmountDurationBonus
#
# Used by:
# Modules from group: Ancillary Armor Repairer (4 of 4)
# Modules from group: Armor Repair Unit (105 of 105)
type = "overheat"


def handler(fit, module, context):
    module.boostItemAttr("duration", module.getModifiedItemAttr("overloadSelfDurationBonus"))
    module.boostItemAttr("armorDamageAmount", module.getModifiedItemAttr("overloadArmorDamageAmount"),
                         stackingPenalties=True)
