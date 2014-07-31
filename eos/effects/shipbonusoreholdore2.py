# Used by:
# Variations of ship: Retriever (2 of 2)
# Ship: Mackinaw ORE Development Edition
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Mining Barge").level
    fit.ship.boostItemAttr("specialOreHoldCapacity", ship.getModifiedItemAttr("shipBonusORE2") * level)