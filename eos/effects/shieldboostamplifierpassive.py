# Used by:
# Implant: Crystal Alpha
# Implant: Crystal Beta
# Implant: Crystal Delta
# Implant: Crystal Epsilon
# Implant: Crystal Gamma
# Implant: Low-grade Crystal Alpha
# Implant: Low-grade Crystal Beta
# Implant: Low-grade Crystal Delta
# Implant: Low-grade Crystal Epsilon
# Implant: Low-grade Crystal Gamma
type = "passive"
def handler(fit, container, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", container.getModifiedItemAttr("shieldBoostMultiplier"))
