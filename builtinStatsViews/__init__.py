__all__ = ["resourcesViewFull", "resistancesViewFull",
           "rechargeViewFull", "firepowerViewFull", "capacitorViewFull",
           "targetingmiscViewFull", "priceViewFull"]

columns = {}
def registerView(column):
    columns[column.name] = column

def getView(name):
    return columns[name]
