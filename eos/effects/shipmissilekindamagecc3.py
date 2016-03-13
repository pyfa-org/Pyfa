# shipMissileKinDamageCC3
#
# Used by:
# Ship: Osprey Navy Issue

type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "kineticDamage", src.getModifiedItemAttr("shipBonusCC3"), skill="Caldari Cruiser")