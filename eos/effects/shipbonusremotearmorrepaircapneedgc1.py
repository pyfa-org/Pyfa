# Used by:
# Ship: Exequror
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Repair Projector",
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusGC") * level)
