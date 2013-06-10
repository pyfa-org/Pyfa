# Used by:
# Ships from group: Interdictor (4 of 4)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Interdictors").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Interdiction Sphere Launcher",
                                  "moduleReactivationDelay", ship.getModifiedItemAttr("eliteBonusInterdictors2") * level)
