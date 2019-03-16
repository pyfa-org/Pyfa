# eliteBonusHeavyGunshipHeavyAssaultMissileLaunhcerRof2
#
# Used by:
# Ship: Cerberus
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy Assault",
                                  "speed", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"),
                                  skill="Heavy Assault Cruisers")
