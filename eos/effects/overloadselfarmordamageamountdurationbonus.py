# overloadSelfArmorDamageAmountDurationBonus
#
# Used by:
# Modules from group: Ancillary Armor Repairer (7 of 7)
# Modules from group: Armor Repair Unit (108 of 108)
type = "overheat"


def handler(fit, module, context):
    module.boostItemAttr("duration", module.getModifiedItemAttr("overloadSelfDurationBonus"))
    module.boostItemAttr("armorDamageAmount", module.getModifiedItemAttr("overloadArmorDamageAmount"),
                         stackingPenalties=True)
