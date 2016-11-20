# carrierGallenteArmor&ShieldTransferRange3
#
# Used by:
# Ship: Nyx
# Ship: Thanatos
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "maxRange", ship.getModifiedItemAttr("carrierGallenteBonus3"),
                                  skill="Gallente Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Armor Repair Systems"),
                                  "maxRange", ship.getModifiedItemAttr("carrierGallenteBonus3"),
                                  skill="Gallente Carrier")
