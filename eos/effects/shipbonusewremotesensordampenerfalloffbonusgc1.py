# Used by:
# Ship: Celestis
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Sensor Damper",
                                  "falloff", ship.getModifiedItemAttr("shipBonusGC") * level)
