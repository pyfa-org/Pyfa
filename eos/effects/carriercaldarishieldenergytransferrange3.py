# carrierCaldariShield&EnergyTransferRange3
#
# Used by:
# Ship: Chimera
# Ship: Revenant
# Ship: Wyvern
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "maxRange", ship.getModifiedItemAttr("carrierCaldariBonus3"), skill="Caldari Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Capacitor Emission Systems"),
                                  "maxRange", ship.getModifiedItemAttr("carrierCaldariBonus3"), skill="Caldari Carrier")
