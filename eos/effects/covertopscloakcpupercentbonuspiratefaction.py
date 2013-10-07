# Used by:
# Ship: Astero
type = "passive"
runTime = "early"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Cloaking"),
                                  "cpu", ship.getModifiedItemAttr("shipBonusPirateFaction"))
