from collections import namedtuple

from eos.const import FittingModuleState


ModuleInfoCache = namedtuple('ModuleInfoCache', ['modPosition', 'itemID', 'state', 'charge', 'baseID', 'mutaplasmidID'])


def stateLimit(item):
    if {'moduleBonusAssaultDamageControl', 'moduleBonusIndustrialInvulnerability'}.intersection(item.effects):
        return FittingModuleState.ONLINE
    return FittingModuleState.ACTIVE
