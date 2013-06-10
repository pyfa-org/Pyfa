# Used by:
# Implants named like: Eifyr and Co. 'Rogue' Acceleration Control AC (6 of 6)
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                  "speedFactor", implant.getModifiedItemAttr("speedFBonus"))
