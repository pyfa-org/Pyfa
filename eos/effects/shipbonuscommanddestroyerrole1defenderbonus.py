# shipBonusCommandDestroyerRole1DefenderBonus
#
# Used by:
# Ships from group: Command Destroyer (4 of 4)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Defender Missiles"),
                                  "moduleReactivationDelay", ship.getModifiedItemAttr("shipBonusRole1"))
