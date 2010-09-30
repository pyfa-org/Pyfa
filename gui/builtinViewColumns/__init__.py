__all__ = ["moduleState", "moduleNameOrSlot", "attributeDisplay", "maxRange",
           "name", "droneDps", "droneNameAmount", "droneCheckbox", "moduleAmmo"]

columns = {}
def registerColumn(column):
    columns[column.name] = column

def getColumn(name):
    return columns[name]
