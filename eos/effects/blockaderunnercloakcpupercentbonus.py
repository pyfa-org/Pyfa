# Used by:
# Ships from group: Blockade Runner (4 of 4)
type = "passive"
runTime = "early"
def handler(fit, ship, context):
    level = fit.character.getSkill("Transport Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Cloaking Device",
                                  "cpu", ship.getModifiedItemAttr("eliteIndustrialCovertCloakBonus") * level)
