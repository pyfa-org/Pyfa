def syncDiscordShareMenuVisibility(fitMenu, shareToDiscordId, optimizeFitPriceId, discordEnabled, menuText, menuHelp):
    existingItem = fitMenu.FindItemById(shareToDiscordId)

    if discordEnabled and existingItem is None:
        optimizeItem = fitMenu.FindItemById(optimizeFitPriceId)
        menuItems = fitMenu.GetMenuItems()
        insertPos = menuItems.index(optimizeItem) if optimizeItem in menuItems else len(menuItems)
        fitMenu.Insert(insertPos, shareToDiscordId, menuText, menuHelp)
    elif not discordEnabled and existingItem is not None:
        fitMenu.Remove(existingItem)
