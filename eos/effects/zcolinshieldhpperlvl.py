# Used by:
# Ship: Bustard
# Ship: Mastodon
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Transport Ships").level
    fit.ship.boostItemAttr("shieldCapacity", ship.getModifiedItemAttr("shipBonusHPExtender1") * level)
