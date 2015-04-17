# probeLauncherCPUPercentBonusTacticalDestroyer
#
# Used by:
# Ships from group: Tactical Destroyer (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Astrometrics"),
                                     "cpu", ship.getModifiedItemAttr("roleBonusTacticalDestroyer1"))
