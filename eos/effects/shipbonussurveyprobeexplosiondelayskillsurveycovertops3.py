# Used by:
# Ship: Anathema
# Ship: Buzzard
# Ship: Cheetah
# Ship: Helios
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Covert Ops").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Survey Probe",
                                    "explosionDelay", ship.getModifiedItemAttr("eliteBonusCoverOps3") * level)
