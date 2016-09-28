# skillStructureEngineeringSystemsCapNeedBonus
#
# Used by:
# Skill: Structure Engineering Systems
type = "passive", "structure"
def handler(fit, src, context):
    groups = ("Structure Energy Neutralizer", "Structure Area Denial Module")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                    "capacitorNeed", src.getModifiedItemAttr("capNeedBonus"), skill="Structure Engineering Systems")
