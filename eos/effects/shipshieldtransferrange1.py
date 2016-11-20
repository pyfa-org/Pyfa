# shipShieldTransferRange1
#
# Used by:
# Ship: Basilisk
# Ship: Etana
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Shield Booster",
                                  "shieldTransferRange", ship.getModifiedItemAttr("shipBonusCC"),
                                  skill="Caldari Cruiser")
