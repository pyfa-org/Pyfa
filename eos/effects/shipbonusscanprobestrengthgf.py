# Used by:
# Ship: Imicus
# Ship: Inner Zone Shipping Imicus
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Frigate").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                    "baseSensorStrength", ship.getModifiedItemAttr("shipBonusGF2") * level)
