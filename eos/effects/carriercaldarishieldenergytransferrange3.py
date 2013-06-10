# Used by:
# Ship: Chimera
# Ship: Revenant
# Ship: Wyvern
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Carrier").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "shieldTransferRange", ship.getModifiedItemAttr("carrierCaldariBonus3") * level)
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Emission Systems"),
                                  "powerTransferRange", ship.getModifiedItemAttr("carrierCaldariBonus3") * level)
