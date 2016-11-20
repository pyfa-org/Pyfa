# carrierMinmatarArmor&ShieldTransferRange3
#
# Used by:
# Ship: Hel
# Ship: Nidhoggur
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "maxRange", ship.getModifiedItemAttr("carrierMinmatarBonus3"),
                                  skill="Minmatar Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Armor Repair Systems"),
                                  "maxRange", ship.getModifiedItemAttr("carrierMinmatarBonus3"),
                                  skill="Minmatar Carrier")
