# shipBonusShieldTransferCapNeedMF
#
# Used by:
# Ship: Burst
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")
