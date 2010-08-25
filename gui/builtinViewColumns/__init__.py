__all__ = ["moduleState", "moduleNameOrSlot", "attributeDisplay"]

columns = {}
def registerColumn(column):
    columns[column.name] = column

def getColumn(name):
    return columns[name]
