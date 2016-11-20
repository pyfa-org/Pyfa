# armorWarfareArmorHpReplacer
#
# Used by:
# Implant: Armored Command Mindlink
# Implant: Federation Navy Warfare Mindlink
# Implant: Imperial Navy Warfare Mindlink
type = "gang", "active"
gangBonus = "armorHpBonus2"
gangBoost = "armorHP"


def handler(fit, module, context):
    if "gang" not in context:
        return
    fit.ship.boostItemAttr("armorHP", module.getModifiedItemAttr("armorHpBonus2"))
