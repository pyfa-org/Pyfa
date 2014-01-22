# Used by:
# Modules named like: Reinforcer (32 of 32)
type = "passive"
def handler(fit, module, context):
    for type in ("kinetic", "thermal", "explosive", "em"):
        fit.ship.boostItemAttr("shield" + type.capitalize() + "DamageResonance",
                               module.getModifiedItemAttr(type + "DamageResistanceBonus") or 0,
                               stackingPenalties = True)
