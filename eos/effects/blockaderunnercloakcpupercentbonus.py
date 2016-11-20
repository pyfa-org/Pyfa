# blockadeRunnerCloakCpuPercentBonus
#
# Used by:
# Ships from group: Blockade Runner (4 of 4)
type = "passive"
runTime = "early"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Cloaking Device",
                                  "cpu", ship.getModifiedItemAttr("eliteIndustrialCovertCloakBonus"),
                                  skill="Transport Ships")
