# Used by:
# Ship: Absolution
# Ship: Astarte
# Ship: Damnation
# Ship: Eos
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Command Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Warfare Specialist"),
                                  "commandBonus", ship.getModifiedItemAttr("eliteBonusCommandShips3") * level)
