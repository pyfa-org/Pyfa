# shipSmallMissileKinDmgCF3
#
# Used by:
# Ship: Caldari Navy Hookbill

type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles") or mod.charge.requiresSkill("Rockets"), "kineticDamage", src.getModifiedItemAttr("shipBonus3CF"), skill="Caldari Frigate")