# Used by:
# Implants named like: Low grade Centurion (5 of 6)
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Sensor Damper",
                                  "maxRange", implant.getModifiedItemAttr("rangeSkillBonus"))