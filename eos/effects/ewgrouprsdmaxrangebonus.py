# Used by:
# Implant: Low-grade Centurion Alpha
# Implant: Low-grade Centurion Beta
# Implant: Low-grade Centurion Delta
# Implant: Low-grade Centurion Epsilon
# Implant: Low-grade Centurion Gamma
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Sensor Damper",
                                  "maxRange", implant.getModifiedItemAttr("rangeSkillBonus"))