# oreCapitalShipShieldTransferRange
#
# Used by:
# Ship: Rorqual
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "shieldTransferRange", ship.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")
