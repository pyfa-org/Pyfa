# modifyActiveArmorResonancePostPercent
#
# Used by:
# Modules from group: Armor Hardener (156 of 156)
# Modules from group: Flex Armor Hardener (4 of 4)
type = "active"


def handler(fit, module, context):
    for damageType in ("kinetic", "thermal", "explosive", "em"):
        fit.ship.boostItemAttr("armor%sDamageResonance" % damageType.capitalize(),
                               module.getModifiedItemAttr("%sDamageResistanceBonus" % damageType),
                               stackingPenalties=True)
