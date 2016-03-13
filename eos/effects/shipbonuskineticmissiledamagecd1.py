# shipBonusKineticMissileDamageCD1
#
# Used by:
# Ship: Stork
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "kineticDamage", src.getModifiedItemAttr("shipBonusCD1"), skill="Caldari Destroyer")
