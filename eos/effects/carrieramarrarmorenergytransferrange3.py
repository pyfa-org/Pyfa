# carrierAmarrArmor&EnergyTransferRange3
#
# Used by:
# Ship: Aeon
# Ship: Archon
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Armor Repair Systems"),
                                  "maxRange", ship.getModifiedItemAttr("carrierAmarrBonus3"), skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Capacitor Emission Systems"),
                                  "powerTransferRange", ship.getModifiedItemAttr("carrierAmarrBonus3"), skill="Amarr Carrier")
