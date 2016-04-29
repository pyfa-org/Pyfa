type = "gang"
gangBoost = "armorHP"
gangBonus = "shipBonusTitanG4"
runTime = "late"

def handler(fit, src, context):
    if "gang" not in context: return
    fit.ship.boostItemAttr(gangBoost, src.getModifiedItemAttr(gangBonus) * src.parent.character.getSkill("Gallente Titan").level)

