# Used by:
# Ship: Scorpion
# Ship: Scorpion Ishukone Watch
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    for sensorType in ("Gravimetric", "Ladar", "Magnetometric", "Radar"):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "scan{0}StrengthBonus".format(sensorType),
                                      ship.getModifiedItemAttr("shipBonusCB") * level)
