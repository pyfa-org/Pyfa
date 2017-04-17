# shipMETCDamageBonusAC
#
# Used by:
# Ship: Augoror Navy Issue
# Ship: Enforcer
# Ship: Maller
# Ship: Omen Navy Issue
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
