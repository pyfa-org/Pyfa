# Used by:
# Ship: Crucifier
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusAF") * level)
