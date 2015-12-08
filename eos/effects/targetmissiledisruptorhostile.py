# targetMissileDisruptorHostile
#  Modifier 1:
#  #  state: active
#  #  scope: projected
#  #  srcattr: explosionDelayBonus 596
#  #  operator: post_percent 8
#  #  tgtattr: explosionDelay (penalized) 281
#  #  location: ship
#  #  filter type: skill
#  #  filter value: Missile Launcher Operation
#  Modifier 2:
#  #  state: active
#  #  scope: projected
#  #  srcattr: aoeVelocityBonus 847
#  #  operator: post_percent 8
#  #  tgtattr: aoeVelocity (penalized) 653
#  #  location: ship
#  #  filter type: skill
#  #  filter value: Missile Launcher Operation
#  Modifier 3:
#  #  state: active
#  #  scope: projected
#  #  srcattr: aoeCloudSizeBonus 848
#  #  operator: post_percent 8
#  #  tgtattr: aoeCloudSize (penalized) 654
#  #  location: ship
#  #  filter type: skill
#  #  filter value: Missile Launcher Operation
#  Modifier 4:
#  #  state: active
#  #  scope: projected
#  #  srcattr: missileVelocityBonus 547
#  #  operator: post_percent 8
#  #  tgtattr: maxVelocity (penalized) 37
#  #  location: ship
#  #  filter type: skill
#  #  filter value: Missile Launcher Operation
#
type = "active", "projected"

def handler(fit, src, context):
    if "projected" in context:
        for srcAttr, tgtAttr in (
            ("aoeCloudSizeBonus", "aoeCloudSize"),
            ("aoeVelocityBonus", "aoeVelocity"),
            ("missileVelocityBonus", "maxVelocity"),
            ("explosionDelayBonus", "explosionDelay"),
        ):
            fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        tgtAttr, src.getModifiedItemAttr(srcAttr),
                                        stackingPenalties=True)
