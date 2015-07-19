# shipBonusStasisMF2
#
# Used by:
# Ship: Cruor
# Ship: Freki
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")
