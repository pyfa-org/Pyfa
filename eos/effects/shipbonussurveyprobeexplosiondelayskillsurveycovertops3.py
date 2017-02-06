# shipBonusSurveyProbeExplosionDelaySkillSurveyCovertOps3
#
# Used by:
# Ships from group: Covert Ops (4 of 6)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Survey Probe",
                                    "explosionDelay", ship.getModifiedItemAttr("eliteBonusCoverOps3"),
                                    skill="Covert Ops")
