__all__ = []

menus = {}
def registerMenu(menu):
    menus[menu.name] = menu

def getMenu(name):
    return menus[name]
