# Used by:
# Ship: Blackbird
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Cruiser").level
    for type in ("Gravimetric", "Magnetometric", "Ladar", "Radar"):
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                      "scan{0}StrengthBonus".format(type), ship.getModifiedItemAttr("shipBonusCC") * level)
