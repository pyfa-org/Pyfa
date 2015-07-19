# shipShieldTransferRange2
#
# Used by:
# Ship: Scimitar
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Shield Booster",
                                  "shieldTransferRange", ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")
