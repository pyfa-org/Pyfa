# shipBonusShieldTransferCapneedMC1
#
# Used by:
# Ship: Scythe
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusMC"), skill="Minmatar Cruiser")
