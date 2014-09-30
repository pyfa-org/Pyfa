# zColinOrcaForemanModBonus
#
# Used by:
# Ships from group: Industrial Command Ship (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Industrial Command Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Director"),
                                  "commandBonus", ship.getModifiedItemAttr("shipOrcaForemanBonus") * level)
