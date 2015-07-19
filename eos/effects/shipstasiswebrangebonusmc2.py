# shipStasisWebRangeBonusMC2
#
# Used by:
# Ship: Ashimmu
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")
