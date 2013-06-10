# Used by:
# Ship: Augoror
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Repair Projector",
                                  "armorDamageAmount", ship.getModifiedItemAttr("shipBonusAC2") * level)
