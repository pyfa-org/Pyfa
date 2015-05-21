# probeLauncherCPUPercentBonusTacticalDestroyer
#
# Used by:
# Ships from group: Tactical Destroyer (3 of 3)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Astrometrics"),
                                     "cpu", ship.getModifiedItemAttr("roleBonusTacticalDestroyer1"))
