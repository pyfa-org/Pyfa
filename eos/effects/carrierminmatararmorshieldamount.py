# carrierMinmatarArmor&ShieldAmount
#
# Used by:
# Ship: Hel
# Ship: Nidhoggur
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Shield Booster",
                                  "shieldBonus", ship.getModifiedItemAttr("carrierMinmatarBonus2"), skill="Minmatar Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "armorDamageAmount", ship.getModifiedItemAttr("carrierMinmatarBonus2"), skill="Minmatar Carrier")
