# shipBonusShieldTransferCapNeedCF
#
# Used by:
# Variations of ship: Bantam (2 of 2)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")
