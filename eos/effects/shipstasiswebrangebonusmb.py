# shipStasisWebRangeBonusMB
#
# Used by:
# Ship: Bhaalgorn
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")
