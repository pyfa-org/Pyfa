# Used by:
# Ship: Leviathan
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Titan").level
    groups = ("Citadel Torpedo", "Citadel Cruise")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in groups,
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusCT1") * level)
