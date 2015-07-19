# titanCaldariMissileKineticDmg2
#
# Used by:
# Ship: Leviathan
type = "passive"
def handler(fit, ship, context):
    groups = ("Citadel Torpedo", "Citadel Cruise")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in groups,
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusCT1"), skill="Caldari Titan")
