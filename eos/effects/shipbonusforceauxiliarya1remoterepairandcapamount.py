# shipBonusForceAuxiliaryA1RemoteRepairAndCapAmount
#
# Used by:
# Ship: Apostle
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: (mod.item.requiresSkill("Capacitor Emission Systems") or
                                               mod.item.requiresSkill("Capital Capacitor Emission Systems")),
                                  "powerTransferAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryA1"),
                                  skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: (mod.item.requiresSkill("Remote Armor Repair Systems") or
                                               mod.item.requiresSkill("Capital Remote Armor Repair Systems")),
                                  "armorDamageAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryA1"),
                                  skill="Amarr Carrier")
