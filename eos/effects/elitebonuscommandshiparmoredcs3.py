# eliteBonusCommandShipArmoredCS3
#
# Used by:
# Ship: Absolution
# Ship: Astarte
# Ship: Damnation
# Ship: Eos
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Warfare Specialist"),
                                  "commandBonus", ship.getModifiedItemAttr("eliteBonusCommandShips3"), skill="Command Ships")
