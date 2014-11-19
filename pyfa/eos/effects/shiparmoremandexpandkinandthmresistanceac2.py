# shipArmorEMAndExpAndkinAndThmResistanceAC2
#
# Used by:
# Ships named like: Stratios (2 of 2)
# Ship: Sacrilege
# Ship: Vangel
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Cruiser").level
    damageTypes = ("Em", "Explosive", "Kinetic", "Thermal")
    for damageType in damageTypes:
        fit.ship.boostItemAttr("armor{0}DamageResonance".format(damageType), ship.getModifiedItemAttr("shipBonusAC2") * level)
