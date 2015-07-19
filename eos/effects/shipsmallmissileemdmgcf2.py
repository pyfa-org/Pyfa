# shipSmallMissileEMDmgCF2
#
# Used by:
# Ship: Kestrel
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
                                    "emDamage", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")
