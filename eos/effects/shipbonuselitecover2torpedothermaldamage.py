# shipBonusEliteCover2TorpedoThermalDamage
#
# Used by:
# Ship: Nemesis
# Ship: Virtuoso
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "thermalDamage", ship.getModifiedItemAttr("eliteBonusCovertOps2"),
                                    skill="Covert Ops")
