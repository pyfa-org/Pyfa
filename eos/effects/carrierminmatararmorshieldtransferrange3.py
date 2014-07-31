# Used by:
# Ship: Hel
# Ship: Nidhoggur
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Carrier").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "shieldTransferRange", ship.getModifiedItemAttr("carrierMinmatarBonus3") * level)
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Armor Repair Systems"),
                                  "maxRange", ship.getModifiedItemAttr("carrierMinmatarBonus3") * level)
