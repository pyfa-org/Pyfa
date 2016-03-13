# shipRemoteSensorDampenerCapNeedGF
#
# Used by:
# Ship: Keres
# Ship: Maulus
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")
