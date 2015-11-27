# shipMissileKinDamageCC3
#  Modifier 1:
#  #  state: offline
#  #  scope: local
#  #  srcattr: shipBonusCC3 1535
#  #  operator: post_percent 8
#  #  tgtattr: kineticDamage (not penalized) 117
#  #  location: space
#  #  filter type: skill
#  #  filter value: Missile Launcher Operation

type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"), "kineticDamage", src.getModifiedItemAttr("shipBonusCC3"), skill="Caldari Cruiser")