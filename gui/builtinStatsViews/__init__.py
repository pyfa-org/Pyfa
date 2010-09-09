__all__ = ["exampleView"]

columns = {}
def registerView(column):
    columns[column.name] = column

def getView(name):
    return columns[name]
