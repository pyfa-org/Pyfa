# zColinOrcaForemanModBonus
#
# Used by:
# Ship: Orca
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Director"),
                                  "commandBonus", ship.getModifiedItemAttr("shipOrcaForemanBonus"),
                                  skill="Industrial Command Ships")
