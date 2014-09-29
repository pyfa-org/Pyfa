# shipMETCDamageBonusAC
#
# Used by:
# Ship: Augoror Navy Issue
# Ship: Maller
# Ship: Omen Navy Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusAC") * level)
