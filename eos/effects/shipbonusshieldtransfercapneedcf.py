# shipBonusShieldTransferCapNeedCF
#
# Used by:
# Ship: Bantam
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")
