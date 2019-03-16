# shipBonusTDOptimalBonusAF1
#
# Used by:
# Ship: Crucifier
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
