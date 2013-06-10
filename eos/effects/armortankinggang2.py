# Used by:
# Implant: Armored Warfare Mindlink
type = "gang", "active"
gangBonus = "armorHpBonus2"
gangBoost = "armorHP"
def handler(fit, module, context):
    if "gang" not in context: return
    fit.ship.boostItemAttr("armorHP", module.getModifiedItemAttr("armorHpBonus2"))
