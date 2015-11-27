# shipSmallMissileKinDmgCF3
#  Modifier 1:
#  #  state: offline
#  #  scope: local
#  #  srcattr: shipBonus3CF 1624
#  #  operator: post_percent 8
#  #  tgtattr: kineticDamage (not penalized) 117
#  #  location: space
#  #  filter type: skill
#  #  filter value: Light Missiles
#  Modifier 2:
#  #  state: offline
#  #  scope: local
#  #  srcattr: shipBonus3CF 1624
#  #  operator: post_percent 8
#  #  tgtattr: kineticDamage (not penalized) 117
#  #  location: space
#  #  filter type: skill
#  #  filter value: Rockets

type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles") or mod.charge.requiresSkill("Rockets"), "kineticDamage", src.getModifiedItemAttr("shipBonus3CF"), skill="Caldari Frigate")